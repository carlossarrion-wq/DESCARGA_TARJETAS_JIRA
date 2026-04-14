#!/usr/bin/env python3
"""
Script para extraer issues de tipo "Incidencia" del proyecto Darwin (DAR) en Jira Naturgy-ADN
Basado en el script original de extracción de Jira
"""

import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import time
from pathlib import Path

# Intentar importar la configuración local, si no existe usar la de ejemplo
try:
    from config_naturgy_local import *
except ImportError:
    print("⚠️  No se encontró config_naturgy_local.py")
    print("📝 Por favor, copia config_naturgy.py a config_naturgy_local.py y configura tus credenciales")
    sys.exit(1)


class NaturgyJiraExtractor:
    """Extractor de issues de Jira para Naturgy-ADN"""
    
    def __init__(self):
        self.base_url = JIRA_URL
        self.auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.output_dir = Path(OUTPUT_DIR)
        self.attachments_dir = self.output_dir / "attachments"
        
        # Crear directorios si no existen
        self.output_dir.mkdir(exist_ok=True)
        if DOWNLOAD_ATTACHMENTS:
            self.attachments_dir.mkdir(exist_ok=True)
    
    def search_issues(self, start_at=0, max_results=100):
        """
        Busca issues de tipo Incidencia en el proyecto DAR
        """
        url = f"{self.base_url}/rest/api/3/search/jql"
        
        # JQL para buscar incidencias en el proyecto DAR
        jql = f'project = {PROJECT_KEY} AND issuetype = "{ISSUE_TYPE}" ORDER BY created DESC'
        
        params = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
            "fields": "*all",  # Obtener todos los campos
            "expand": "renderedFields,names,schema,transitions,operations,changelog"
        }
        
        print(f"🔍 Buscando issues con JQL: {jql}")
        print(f"📄 Página: {start_at // max_results + 1} (desde {start_at})")
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                auth=self.auth,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error al buscar issues: {e}")
            if hasattr(e.response, 'text'):
                print(f"Respuesta del servidor: {e.response.text}")
            return None
    
    def download_attachment(self, attachment_url, attachment_name, issue_key):
        """
        Descarga un adjunto de Jira
        """
        if not DOWNLOAD_ATTACHMENTS:
            return None
        
        try:
            # Crear directorio para el issue
            issue_attachments_dir = self.attachments_dir / issue_key
            issue_attachments_dir.mkdir(exist_ok=True)
            
            # Descargar el archivo
            response = requests.get(
                attachment_url,
                auth=self.auth,
                stream=True,
                timeout=60
            )
            response.raise_for_status()
            
            # Verificar tamaño
            content_length = int(response.headers.get('content-length', 0))
            size_mb = content_length / (1024 * 1024)
            
            if size_mb > MAX_ATTACHMENT_SIZE_MB:
                print(f"  ⚠️  Adjunto {attachment_name} demasiado grande ({size_mb:.2f} MB), omitiendo...")
                return None
            
            # Guardar archivo
            file_path = issue_attachments_dir / attachment_name
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"  ✅ Descargado: {attachment_name} ({size_mb:.2f} MB)")
            return str(file_path.relative_to(self.output_dir))
        
        except Exception as e:
            print(f"  ❌ Error descargando {attachment_name}: {e}")
            return None
    
    def format_user(self, user_data):
        """Formatea información de usuario"""
        if not user_data:
            return "No asignado"
        return f"{user_data.get('displayName', 'Desconocido')} ({user_data.get('emailAddress', 'sin email')})"
    
    def format_date(self, date_str):
        """Formatea una fecha ISO a formato legible"""
        if not date_str:
            return "N/A"
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%d/%m/%Y %H:%M:%S")
        except:
            return date_str
    
    def extract_issue_data(self, issue):
        """
        Extrae los datos relevantes de un issue
        """
        fields = issue.get('fields', {})
        key = issue.get('key', 'UNKNOWN')
        
        print(f"\n📋 Procesando: {key}")
        
        # Datos básicos
        data = {
            'key': key,
            'url': f"{self.base_url}/browse/{key}",
            'summary': fields.get('summary', 'Sin título'),
            'description': fields.get('description', 'Sin descripción'),
            'status': fields.get('status', {}).get('name', 'Desconocido'),
            'priority': fields.get('priority', {}).get('name', 'Sin prioridad'),
            'assignee': self.format_user(fields.get('assignee')),
            'reporter': self.format_user(fields.get('reporter')),
            'created': self.format_date(fields.get('created')),
            'updated': self.format_date(fields.get('updated')),
            'resolutiondate': self.format_date(fields.get('resolutiondate')),
        }
        
        # Etiquetas
        data['labels'] = fields.get('labels', [])
        
        # Componentes
        components = fields.get('components', [])
        data['components'] = [c.get('name', '') for c in components]
        
        # Comentarios
        comments_data = fields.get('comment', {})
        comments = comments_data.get('comments', [])
        data['comments'] = []
        
        for comment in comments:
            comment_info = {
                'author': self.format_user(comment.get('author')),
                'created': self.format_date(comment.get('created')),
                'body': comment.get('body', '')
            }
            data['comments'].append(comment_info)
        
        print(f"  💬 {len(comments)} comentarios")
        
        # Adjuntos
        attachments = fields.get('attachment', [])
        data['attachments'] = []
        
        print(f"  📎 {len(attachments)} adjuntos")
        
        for attachment in attachments:
            attachment_info = {
                'filename': attachment.get('filename', 'unknown'),
                'size': attachment.get('size', 0),
                'mimeType': attachment.get('mimeType', 'unknown'),
                'created': self.format_date(attachment.get('created')),
                'author': self.format_user(attachment.get('author')),
                'url': attachment.get('content', '')
            }
            
            # Descargar adjunto si está habilitado
            if DOWNLOAD_ATTACHMENTS and attachment_info['url']:
                local_path = self.download_attachment(
                    attachment_info['url'],
                    attachment_info['filename'],
                    key
                )
                attachment_info['local_path'] = local_path
            
            data['attachments'].append(attachment_info)
        
        # Campos personalizados (custom fields)
        data['custom_fields'] = {}
        for field_key, field_value in fields.items():
            if field_key.startswith('customfield_'):
                if field_value is not None:
                    data['custom_fields'][field_key] = field_value
        
        return data
    
    def save_issue_markdown(self, issue_data):
        """
        Guarda un issue en formato Markdown
        """
        key = issue_data['key']
        filename = self.output_dir / f"{key}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write(f"# {key}: {issue_data['summary']}\n\n")
            f.write(f"**URL:** {issue_data['url']}\n\n")
            
            # Detalles clave
            f.write("## 📊 Detalles Clave\n\n")
            f.write(f"- **Estado:** {issue_data['status']}\n")
            f.write(f"- **Prioridad:** {issue_data['priority']}\n")
            f.write(f"- **Asignado a:** {issue_data['assignee']}\n")
            f.write(f"- **Reportado por:** {issue_data['reporter']}\n")
            f.write(f"- **Creado:** {issue_data['created']}\n")
            f.write(f"- **Actualizado:** {issue_data['updated']}\n")
            f.write(f"- **Resuelto:** {issue_data['resolutiondate']}\n")
            
            # Etiquetas
            if issue_data['labels']:
                f.write(f"- **Etiquetas:** {', '.join(issue_data['labels'])}\n")
            
            # Componentes
            if issue_data['components']:
                f.write(f"- **Componentes:** {', '.join(issue_data['components'])}\n")
            
            # Descripción
            f.write("\n## 📝 Descripción\n\n")
            if issue_data['description']:
                f.write(f"{issue_data['description']}\n\n")
            else:
                f.write("*Sin descripción*\n\n")
            
            # Comentarios
            if issue_data['comments']:
                f.write(f"## 💬 Comentarios ({len(issue_data['comments'])})\n\n")
                for i, comment in enumerate(issue_data['comments'], 1):
                    f.write(f"### Comentario {i}\n\n")
                    f.write(f"**Autor:** {comment['author']}\n")
                    f.write(f"**Fecha:** {comment['created']}\n\n")
                    f.write(f"{comment['body']}\n\n")
                    f.write("---\n\n")
            
            # Adjuntos
            if issue_data['attachments']:
                f.write(f"## 📎 Adjuntos ({len(issue_data['attachments'])})\n\n")
                for attachment in issue_data['attachments']:
                    f.write(f"### {attachment['filename']}\n\n")
                    f.write(f"- **Tamaño:** {attachment['size']} bytes\n")
                    f.write(f"- **Tipo:** {attachment['mimeType']}\n")
                    f.write(f"- **Subido por:** {attachment['author']}\n")
                    f.write(f"- **Fecha:** {attachment['created']}\n")
                    if attachment.get('local_path'):
                        f.write(f"- **Archivo local:** `{attachment['local_path']}`\n")
                    f.write(f"- **URL:** {attachment['url']}\n\n")
            
            # Campos personalizados
            if issue_data['custom_fields']:
                f.write("## 🔧 Campos Personalizados\n\n")
                for field_key, field_value in issue_data['custom_fields'].items():
                    f.write(f"- **{field_key}:** {field_value}\n")
                f.write("\n")
        
        print(f"  ✅ Guardado: {filename.name}")
    
    def save_issue_json(self, issue_data):
        """
        Guarda un issue en formato JSON
        """
        key = issue_data['key']
        filename = self.output_dir / f"{key}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(issue_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Guardado JSON: {filename.name}")
    
    def extract_all_issues(self):
        """
        Extrae todos los issues del proyecto
        """
        print("=" * 80)
        print("🚀 EXTRACTOR DE INCIDENCIAS - NATURGY-ADN DARWIN (DAR)")
        print("=" * 80)
        print(f"📍 Proyecto: {PROJECT_KEY}")
        print(f"📋 Tipo de issue: {ISSUE_TYPE}")
        print(f"📁 Directorio de salida: {self.output_dir}")
        print(f"📎 Descargar adjuntos: {'Sí' if DOWNLOAD_ATTACHMENTS else 'No'}")
        print("=" * 80)
        
        start_at = START_AT
        max_results = MAX_RESULTS
        total_extracted = 0
        
        while True:
            # Buscar issues
            result = self.search_issues(start_at, max_results)
            
            if not result:
                print("❌ Error al buscar issues. Abortando.")
                break
            
            total = result.get('total', 0)
            issues = result.get('issues', [])
            
            if not issues:
                print("✅ No hay más issues para procesar")
                break
            
            print(f"\n📊 Total de issues encontrados: {total}")
            print(f"📄 Procesando {len(issues)} issues de esta página...")
            
            # Procesar cada issue
            for issue in issues:
                try:
                    issue_data = self.extract_issue_data(issue)
                    self.save_issue_markdown(issue_data)
                    self.save_issue_json(issue_data)
                    total_extracted += 1
                    
                    # Pequeña pausa para no saturar la API
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"❌ Error procesando issue: {e}")
                    continue
            
            # Verificar si hay más páginas
            start_at += len(issues)
            if start_at >= total:
                break
            
            print(f"\n⏳ Esperando 2 segundos antes de la siguiente página...")
            time.sleep(2)
        
        # Resumen final
        print("\n" + "=" * 80)
        print("✅ EXTRACCIÓN COMPLETADA")
        print("=" * 80)
        print(f"📊 Total de issues extraídos: {total_extracted}")
        print(f"📁 Archivos guardados en: {self.output_dir}")
        if DOWNLOAD_ATTACHMENTS:
            print(f"📎 Adjuntos guardados en: {self.attachments_dir}")
        print("=" * 80)
        
        # Crear archivo de resumen
        self.create_summary(total_extracted)
    
    def create_summary(self, total_extracted):
        """
        Crea un archivo de resumen de la extracción
        """
        summary_file = self.output_dir / "RESUMEN_EXTRACCION.md"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# Resumen de Extracción - Naturgy-ADN Darwin\n\n")
            f.write(f"**Fecha de extracción:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            f.write(f"**Proyecto:** {PROJECT_KEY}\n")
            f.write(f"**Tipo de issue:** {ISSUE_TYPE}\n")
            f.write(f"**Total de issues extraídos:** {total_extracted}\n\n")
            f.write("## Archivos generados\n\n")
            f.write("- Un archivo `.md` (Markdown) por cada issue\n")
            f.write("- Un archivo `.json` por cada issue\n")
            if DOWNLOAD_ATTACHMENTS:
                f.write("- Adjuntos descargados en la carpeta `attachments/`\n")
            f.write("\n## Estructura de archivos\n\n")
            f.write("```\n")
            f.write(f"{OUTPUT_DIR}/\n")
            f.write("├── RESUMEN_EXTRACCION.md\n")
            f.write("├── DAR-XXX.md\n")
            f.write("├── DAR-XXX.json\n")
            if DOWNLOAD_ATTACHMENTS:
                f.write("└── attachments/\n")
                f.write("    └── DAR-XXX/\n")
                f.write("        └── archivo_adjunto.ext\n")
            f.write("```\n")
        
        print(f"📄 Resumen guardado en: {summary_file}")


def main():
    """Función principal"""
    try:
        extractor = NaturgyJiraExtractor()
        extractor.extract_all_issues()
    except KeyboardInterrupt:
        print("\n\n⚠️  Extracción interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()