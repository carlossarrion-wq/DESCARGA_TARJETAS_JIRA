#!/usr/bin/env python3
"""
Descargador de Tareas JIRA - Versión Optimizada
Descarga todas las tareas de un proyecto JIRA a CSV de forma eficiente
"""

import requests
import csv
import json
from datetime import datetime
import sys
import time
from urllib.parse import quote

class JiraDownloader:
    def __init__(self, base_url, username, api_token):
        """
        Inicializa el descargador JIRA
        
        Args:
            base_url: URL base de JIRA (ej: https://company.atlassian.net)
            username: Email del usuario
            api_token: API Token de JIRA
        """
        # Asegurar que la URL tenga el protocolo https://
        if not base_url.startswith(('http://', 'https://')):
            base_url = 'https://' + base_url
        self.base_url = base_url.rstrip('/')
        self.auth = (username, api_token)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def test_connection(self):
        """Prueba la conexión a JIRA"""
        try:
            response = self.session.get(f"{self.base_url}/rest/api/3/myself")
            if response.status_code == 200:
                user_info = response.json()
                print(f"✓ Conectado como: {user_info.get('displayName', 'Usuario')}")
                return True
            else:
                print(f"✗ Error de autenticación: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error de conexión: {e}")
            return False
    
    def get_all_issues(self, project_key):
        """
        Obtiene todas las issues del proyecto de forma eficiente
        
        Args:
            project_key: Clave del proyecto (ej: GADEA)
        """
        print(f"Descargando issues del proyecto {project_key}...")
        
        all_issues = []
        start_at = 0
        max_results = 100  # Tamaño de página optimizado
        
        # Campos que queremos obtener (optimizado para reducir payload)
        fields = [
            'key', 'summary', 'description', 'status', 'issuetype',
            'priority', 'assignee', 'reporter', 'created', 'updated',
            'resolutiondate', 'resolution', 'labels', 'components',
            'fixVersions', 'comment'
        ]
        
        fields_param = ','.join(fields)
        
        while True:
            # JQL optimizado para el proyecto
            jql = f'project = "{project_key}" ORDER BY key ASC'
            
            params = {
                'jql': jql,
                'startAt': start_at,
                'maxResults': max_results,
                'fields': fields_param,
                'expand': 'changelog'  # Para obtener el histórico
            }
            
            try:
                response = self.session.get(
                    f"{self.base_url}/rest/api/3/search",
                    params=params
                )
                
                if response.status_code != 200:
                    print(f"Error en la consulta: {response.status_code} - {response.text}")
                    break
                
                data = response.json()
                issues = data.get('issues', [])
                
                if not issues:
                    break
                
                all_issues.extend(issues)
                print(f"Descargadas {len(all_issues)} de {data.get('total', '?')} issues...")
                
                # Si hemos obtenido todas las issues, salir
                if len(issues) < max_results:
                    break
                
                start_at += max_results
                
                # Pequeña pausa para no sobrecargar el servidor
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error descargando issues: {e}")
                break
        
        print(f"✓ Total descargadas: {len(all_issues)} issues")
        return all_issues
    
    def extract_issue_data(self, issue):
        """Extrae los datos relevantes de una issue"""
        fields = issue.get('fields', {})
        
        # Información básica
        data = {
            'Key': issue.get('key', ''),
            'Título': fields.get('summary', ''),
            'Descripción': self.clean_text(fields.get('description', '')),
            'Estado': fields.get('status', {}).get('name', '') if fields.get('status') else '',
            'Tipo': fields.get('issuetype', {}).get('name', '') if fields.get('issuetype') else '',
            'Prioridad': fields.get('priority', {}).get('name', '') if fields.get('priority') else '',
            'Asignado': fields.get('assignee', {}).get('displayName', '') if fields.get('assignee') else '',
            'Reportado por': fields.get('reporter', {}).get('displayName', '') if fields.get('reporter') else '',
            'Fecha Creación': self.format_date(fields.get('created')),
            'Fecha Actualización': self.format_date(fields.get('updated')),
            'Fecha Resolución': self.format_date(fields.get('resolutiondate')),
            'Resolución': fields.get('resolution', {}).get('name', '') if fields.get('resolution') else '',
            'Etiquetas': ', '.join(fields.get('labels', [])),
            'Componentes': ', '.join([c.get('name', '') for c in fields.get('components', [])]),
            'Versiones': ', '.join([v.get('name', '') for v in fields.get('fixVersions', [])])
        }
        
        # Comentarios (información clave para incidencias GADEA)
        comments = []
        comment_data = fields.get('comment', {})
        if comment_data and 'comments' in comment_data:
            for comment in comment_data['comments']:
                author = comment.get('author', {}).get('displayName', 'Usuario')
                created = self.format_date(comment.get('created'))
                body = self.clean_text(comment.get('body', ''))
                comments.append(f"[{created}] {author}: {body}")
        
        data['Comentarios'] = ' | '.join(comments)
        
        # Histórico de cambios (changelog)
        changelog_entries = []
        changelog = issue.get('changelog', {})
        if changelog and 'histories' in changelog:
            for history in changelog['histories']:
                author = history.get('author', {}).get('displayName', 'Sistema')
                created = self.format_date(history.get('created'))
                
                for item in history.get('items', []):
                    field = item.get('field', '')
                    from_val = item.get('fromString', '')
                    to_val = item.get('toString', '')
                    changelog_entries.append(f"[{created}] {author}: {field} cambió de '{from_val}' a '{to_val}'")
        
        data['Histórico'] = ' | '.join(changelog_entries)
        
        return data
    
    def clean_text(self, text):
        """Limpia el texto para CSV"""
        if not text:
            return ''
        
        # Si es un objeto (descripción en formato Atlassian Document Format)
        if isinstance(text, dict):
            return self.extract_text_from_adf(text)
        
        # Limpiar texto simple
        text = str(text).replace('\n', ' ').replace('\r', ' ')
        text = ' '.join(text.split())  # Normalizar espacios
        return text[:1000]  # Limitar longitud para CSV
    
    def extract_text_from_adf(self, adf_content):
        """Extrae texto plano de Atlassian Document Format"""
        if not isinstance(adf_content, dict):
            return str(adf_content)
        
        text_parts = []
        
        def extract_text(node):
            if isinstance(node, dict):
                if node.get('type') == 'text':
                    text_parts.append(node.get('text', ''))
                elif 'content' in node:
                    for child in node['content']:
                        extract_text(child)
            elif isinstance(node, list):
                for item in node:
                    extract_text(item)
        
        extract_text(adf_content)
        return ' '.join(text_parts)
    
    def format_date(self, date_str):
        """Formatea fechas de JIRA"""
        if not date_str:
            return ''
        
        try:
            # JIRA usa formato ISO 8601
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return date_str
    
    def export_to_csv(self, issues_data, filename):
        """Exporta los datos a CSV"""
        if not issues_data:
            print("No hay datos para exportar")
            return
        
        print(f"Exportando {len(issues_data)} issues a {filename}...")
        
        # Obtener todas las columnas
        fieldnames = issues_data[0].keys()
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(issues_data)
            
            print(f"✓ Archivo CSV creado: {filename}")
            
        except Exception as e:
            print(f"Error creando CSV: {e}")

def main():
    """Función principal"""
    print("=== Descargador de Tareas JIRA ===\n")
    
    # Configuración (puedes modificar estos valores)
    JIRA_URL = input("URL de JIRA (ej: https://company.atlassian.net): ").strip()
    USERNAME = input("Email/Usuario: ").strip()
    API_TOKEN = input("API Token: ").strip()
    PROJECT_KEY = input("Clave del Proyecto (ej: GADEA): ").strip().upper()
    
    if not all([JIRA_URL, USERNAME, API_TOKEN, PROJECT_KEY]):
        print("Error: Todos los campos son obligatorios")
        return
    
    # Crear descargador
    downloader = JiraDownloader(JIRA_URL, USERNAME, API_TOKEN)
    
    # Probar conexión
    if not downloader.test_connection():
        return
    
    # Descargar issues
    start_time = time.time()
    issues = downloader.get_all_issues(PROJECT_KEY)
    
    if not issues:
        print("No se encontraron issues en el proyecto")
        return
    
    # Procesar datos
    print("Procesando datos...")
    issues_data = []
    for i, issue in enumerate(issues, 1):
        if i % 50 == 0:  # Mostrar progreso cada 50 issues
            print(f"Procesando issue {i}/{len(issues)}...")
        
        issue_data = downloader.extract_issue_data(issue)
        issues_data.append(issue_data)
    
    # Exportar a CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{PROJECT_KEY}_issues_{timestamp}.csv"
    downloader.export_to_csv(issues_data, filename)
    
    elapsed_time = time.time() - start_time
    print(f"\n✓ Proceso completado en {elapsed_time:.2f} segundos")
    print(f"✓ Archivo generado: {filename}")

if __name__ == "__main__":
    main()
