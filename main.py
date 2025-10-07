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
import os
from urllib.parse import quote
from pathlib import Path
import configparser

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
    
    def get_all_issues(self, project_key, max_issues=None):
        """
        Obtiene todas las issues del proyecto usando estrategia de rangos numéricos
        
        Args:
            project_key: Clave del proyecto (ej: NC)
            max_issues: Número máximo de issues a descargar (None = sin límite)
        """
        if max_issues:
            print(f"Descargando issues del proyecto {project_key} (máximo {max_issues})...")
        else:
            print(f"Descargando todas las issues del proyecto {project_key}...")
        
        all_issues = []
        existing_keys = set()
        
        # Campos que queremos obtener (optimizado para reducir payload)
        fields = [
            'key', 'summary', 'description', 'status', 'issuetype',
            'priority', 'assignee', 'reporter', 'created', 'updated',
            'resolutiondate', 'resolution', 'labels', 'components',
            'fixVersions', 'comment', 'attachment'
        ]
        
        fields_param = ','.join(fields)
        
        # Estrategia: descargar en lotes de 100 números
        # Empezar desde 1 para capturar todas las issues
        batch_size = 100
        current_start = 1
        consecutive_empty_batches = 0
        max_empty_batches = 5  # Si encontramos 5 lotes vacíos consecutivos, paramos
        
        while True:
            current_end = current_start + batch_size - 1
            
            # JQL para buscar issues en un rango numérico específico
            jql = f'project = {project_key} AND key >= {project_key}-{current_start} AND key <= {project_key}-{current_end} ORDER BY key ASC'
            
            params = {
                'jql': jql,
                'startAt': 0,
                'maxResults': batch_size,
                'fields': fields_param,
                'expand': 'changelog'
            }
            
            try:
                response = self.session.get(
                    f"{self.base_url}/rest/api/3/search/jql",
                    params=params
                )
                
                if response.status_code != 200:
                    print(f"Error en la consulta: {response.status_code}")
                    break
                
                data = response.json()
                issues = data.get('issues', [])
                
                if not issues:
                    consecutive_empty_batches += 1
                    if consecutive_empty_batches >= max_empty_batches:
                        print(f"No se encontraron más issues después de {max_empty_batches} lotes vacíos")
                        break
                    # Continuar buscando en el siguiente rango
                    current_start = current_end + 1
                    time.sleep(0.1)
                    continue
                
                # Resetear contador de lotes vacíos
                consecutive_empty_batches = 0
                
                # Añadir solo issues únicas
                new_issues_count = 0
                for issue in issues:
                    issue_key = issue.get('key', '')
                    if issue_key and issue_key not in existing_keys:
                        all_issues.append(issue)
                        existing_keys.add(issue_key)
                        new_issues_count += 1
                
                # Mostrar progreso
                total = data.get('total', 0)
                print(f"Rango {project_key}-{current_start} a {project_key}-{current_end}: {new_issues_count} nuevas issues (Total: {len(all_issues)})")
                
                # Si hemos alcanzado el límite máximo (si existe), salir
                if max_issues and len(all_issues) >= max_issues:
                    print(f"✓ Límite de {max_issues} issues alcanzado")
                    all_issues = all_issues[:max_issues]
                    break
                
                # Avanzar al siguiente lote
                current_start = current_end + 1
                
                # Pequeña pausa para no sobrecargar el servidor
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error descargando issues: {e}")
                break
        
        print(f"✓ Total descargadas: {len(all_issues)} issues únicas")
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
            'Versiones': ', '.join([v.get('name', '') for v in fields.get('fixVersions', [])]),
            'Adjuntos': str(len(fields.get('attachment', [])))
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
    
    def get_attachments(self, issue):
        """
        Obtiene la lista de adjuntos de una issue
        
        Args:
            issue: Objeto issue de JIRA
            
        Returns:
            Lista de diccionarios con información de los adjuntos
        """
        fields = issue.get('fields', {})
        attachments = fields.get('attachment', [])
        
        attachment_list = []
        for attachment in attachments:
            attachment_info = {
                'id': attachment.get('id', ''),
                'filename': attachment.get('filename', ''),
                'size': attachment.get('size', 0),
                'mimeType': attachment.get('mimeType', ''),
                'content': attachment.get('content', ''),
                'created': attachment.get('created', ''),
                'author': attachment.get('author', {}).get('displayName', 'Desconocido')
            }
            attachment_list.append(attachment_info)
        
        return attachment_list
    
    def download_attachment(self, attachment_url, output_path):
        """
        Descarga un archivo adjunto
        
        Args:
            attachment_url: URL del adjunto
            output_path: Ruta donde guardar el archivo
            
        Returns:
            True si se descargó correctamente, False en caso contrario
        """
        try:
            response = self.session.get(attachment_url, stream=True)
            
            if response.status_code == 200:
                # Crear directorio si no existe
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Guardar archivo
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return True
            else:
                print(f"  ✗ Error descargando adjunto: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ✗ Error descargando adjunto: {e}")
            return False
    
    def download_all_attachments(self, issues, base_output_dir):
        """
        Descarga todos los adjuntos de las issues
        
        Args:
            issues: Lista de issues
            base_output_dir: Directorio base donde guardar los adjuntos
        """
        print(f"\nDescargando adjuntos...")
        
        total_attachments = 0
        downloaded_attachments = 0
        
        for issue in issues:
            issue_key = issue.get('key', '')
            attachments = self.get_attachments(issue)
            
            if not attachments:
                continue
            
            total_attachments += len(attachments)
            
            # Crear directorio para esta issue
            issue_dir = os.path.join(base_output_dir, issue_key)
            
            print(f"\n{issue_key}: {len(attachments)} adjunto(s)")
            
            for attachment in attachments:
                filename = attachment['filename']
                attachment_url = attachment['content']
                
                # Sanitizar nombre de archivo y añadir prefijo con el ID de la tarjeta
                safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
                prefixed_filename = f"{issue_key}_{safe_filename}"
                output_path = os.path.join(issue_dir, prefixed_filename)
                
                # Verificar si ya existe
                if os.path.exists(output_path):
                    print(f"  ⊙ {prefixed_filename} (ya existe)")
                    downloaded_attachments += 1
                    continue
                
                print(f"  ↓ Descargando: {filename} → {prefixed_filename} ({attachment['size']} bytes)...")
                
                if self.download_attachment(attachment_url, output_path):
                    print(f"  ✓ {prefixed_filename}")
                    downloaded_attachments += 1
                else:
                    print(f"  ✗ Error con {prefixed_filename}")
                
                # Pequeña pausa para no sobrecargar
                time.sleep(0.1)
        
        print(f"\n✓ Adjuntos descargados: {downloaded_attachments}/{total_attachments}")
        
        if downloaded_attachments > 0:
            print(f"✓ Adjuntos guardados en: {base_output_dir}")

def load_config():
    """Carga la configuración desde el archivo config.ini"""
    config = configparser.ConfigParser()
    config_file = 'jira_config.ini'
    
    # Valores por defecto
    defaults = {
        'jira_url': 'https://naturgy-adn.atlassian.net',
        'username': 'carlos.sarrion@es.ibm.com',
        'api_token': '',
        'project_key': 'NC'
    }
    
    # Intentar cargar configuración existente
    if os.path.exists(config_file):
        config.read(config_file)
        if 'JIRA' in config:
            defaults.update(dict(config['JIRA']))
    
    return defaults, config_file

def save_config(jira_url, username, api_token, project_key, config_file):
    """Guarda la configuración en el archivo config.ini"""
    config = configparser.ConfigParser()
    config['JIRA'] = {
        'jira_url': jira_url,
        'username': username,
        'api_token': api_token,
        'project_key': project_key
    }
    
    with open(config_file, 'w') as f:
        config.write(f)
    print(f"✓ Configuración guardada en {config_file}")

def main():
    """Función principal"""
    print("=== Descargador de Tareas JIRA ===\n")
    
    # Cargar configuración
    defaults, config_file = load_config()
    
    # Solicitar configuración con valores por defecto
    print("Presiona Enter para usar el valor por defecto entre corchetes\n")
    
    jira_url = input(f"URL de JIRA [{defaults['jira_url']}]: ").strip()
    if not jira_url:
        jira_url = defaults['jira_url']
    
    username = input(f"Email/Usuario [{defaults['username']}]: ").strip()
    if not username:
        username = defaults['username']
    
    api_token = input(f"API Token [{defaults['api_token'][:20]}...]: ").strip()
    if not api_token:
        api_token = defaults['api_token']
    
    project_key = input(f"Clave del Proyecto [{defaults['project_key']}]: ").strip().upper()
    if not project_key:
        project_key = defaults['project_key']
    
    if not all([jira_url, username, api_token, project_key]):
        print("Error: Todos los campos son obligatorios")
        return
    
    # Guardar configuración
    save_config(jira_url, username, api_token, project_key, config_file)
    print()
    
    # Crear descargador
    downloader = JiraDownloader(jira_url, username, api_token)
    
    # Probar conexión
    if not downloader.test_connection():
        return
    
    # Descargar issues (sin límite)
    start_time = time.time()
    issues = downloader.get_all_issues(project_key)
    
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
    filename = f"{project_key}_issues_{timestamp}.csv"
    downloader.export_to_csv(issues_data, filename)
    
    # Preguntar si desea descargar adjuntos
    download_attachments = input("\n¿Descargar archivos adjuntos? (s/n): ").strip().lower()
    
    if download_attachments == 's':
        attachments_dir = f"{project_key}_attachments_{timestamp}"
        downloader.download_all_attachments(issues, attachments_dir)
    
    elapsed_time = time.time() - start_time
    print(f"\n✓ Proceso completado en {elapsed_time:.2f} segundos")
    print(f"✓ Archivo CSV generado: {filename}")

if __name__ == "__main__":
    main()
