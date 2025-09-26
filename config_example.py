#!/usr/bin/env python3
"""
Archivo de configuración de ejemplo para el Descargador de Tareas JIRA
Copia este archivo como 'config.py' y modifica los valores según tu entorno
"""

# Configuración de JIRA
JIRA_CONFIG = {
    # URL base de tu instancia JIRA
    'base_url': 'https://tuempresa.atlassian.net',
    
    # Tu email de usuario JIRA
    'username': 'tu.email@empresa.com',
    
    # Tu API Token de JIRA (genéralo en tu perfil de Atlassian)
    'api_token': 'ATBB_tu_api_token_aqui',
    
    # Clave del proyecto a descargar
    'project_key': 'GADEA'
}

# Configuración de exportación
EXPORT_CONFIG = {
    # Directorio donde guardar los archivos CSV
    'output_dir': './exports',
    
    # Prefijo para los nombres de archivo
    'filename_prefix': 'jira_export',
    
    # Incluir timestamp en el nombre del archivo
    'include_timestamp': True,
    
    # Límite de caracteres para campos de texto largo
    'text_limit': 1000
}

# Configuración de rendimiento
PERFORMANCE_CONFIG = {
    # Número de issues a descargar por página (máximo 100)
    'page_size': 100,
    
    # Pausa entre requests (segundos) para no sobrecargar el servidor
    'request_delay': 0.1,
    
    # Mostrar progreso cada N issues procesadas
    'progress_interval': 50
}

# Campos adicionales personalizados (opcional)
# Añade aquí campos personalizados de tu JIRA si los necesitas
CUSTOM_FIELDS = {
    # Ejemplo: 'customfield_10001': 'Story Points',
    # Ejemplo: 'customfield_10002': 'Epic Link',
}
