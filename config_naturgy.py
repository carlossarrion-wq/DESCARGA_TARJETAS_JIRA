# Configuración para Jira de Naturgy-ADN
# Copia este archivo y renómbralo a config_naturgy_local.py
# Luego completa los valores con tus credenciales

# URL base de Jira (sin barra final)
JIRA_URL = "https://naturgy-adn.atlassian.net"

# Credenciales de autenticación
# Puedes usar email + API token o usuario + contraseña
JIRA_EMAIL = "tu_email@ejemplo.com"  # Tu email de Atlassian
JIRA_API_TOKEN = "tu_api_token_aqui"  # Token de API de Atlassian

# Configuración del proyecto
PROJECT_KEY = "DAR"  # Proyecto Darwin
ISSUE_TYPE = "Fallo"  # Tipo de issue a extraer (Bug/Fallo - 895 issues)

# Configuración de extracción
MAX_RESULTS = 100  # Número máximo de resultados por página (máximo 100)
START_AT = 0  # Índice de inicio (0 para comenzar desde el principio)

# Directorio de salida
OUTPUT_DIR = "EXTRACCION_NATURGY_DAR"

# Campos a extraer (puedes personalizar según necesites)
FIELDS_TO_EXTRACT = [
    "summary",           # Título
    "description",       # Descripción
    "status",           # Estado
    "priority",         # Prioridad
    "assignee",         # Asignado
    "reporter",         # Reportador
    "created",          # Fecha de creación
    "updated",          # Fecha de actualización
    "resolutiondate",   # Fecha de resolución
    "labels",           # Etiquetas
    "components",       # Componentes
    "comment",          # Comentarios
    "attachment",       # Adjuntos
    "customfield_*",    # Todos los campos personalizados
]

# Configuración de descarga de adjuntos
DOWNLOAD_ATTACHMENTS = True  # Si descargar o no los archivos adjuntos
MAX_ATTACHMENT_SIZE_MB = 50  # Tamaño máximo de adjunto a descargar (en MB)