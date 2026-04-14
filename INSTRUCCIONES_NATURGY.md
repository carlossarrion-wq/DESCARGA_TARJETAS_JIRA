# 📋 Extracción de Incidencias de Jira Naturgy-ADN Darwin

Este documento explica cómo usar el script de extracción para obtener las incidencias del proyecto Darwin (DAR) en Jira de Naturgy-ADN.

## 🎯 Objetivo

Extraer las **896 incidencias** del proyecto Darwin (DAR) de Jira Naturgy-ADN, incluyendo:
- ✅ Título
- ✅ Detalles clave (estado, prioridad, asignado, fechas, etc.)
- ✅ Descripción completa
- ✅ Comentarios
- ✅ Adjuntos (con opción de descarga)
- ✅ Campos personalizados

## 📦 Requisitos Previos

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

Las dependencias necesarias son:
- `requests`: Para hacer peticiones HTTP a la API de Jira
- `python-dateutil`: Para manejo de fechas

### 2. Obtener credenciales de Jira

Para acceder a la API de Jira necesitas:

1. **Email de Atlassian**: Tu email con el que accedes a Jira
2. **API Token**: Token de autenticación

#### Cómo obtener el API Token:

1. Ve a: https://id.atlassian.com/manage-profile/security/api-tokens
2. Haz clic en "Create API token"
3. Dale un nombre descriptivo (ej: "Extracción Darwin")
4. Copia el token generado (¡guárdalo en un lugar seguro!)

## ⚙️ Configuración

### 1. Crear archivo de configuración local

```bash
cp config_naturgy.py config_naturgy_local.py
```

### 2. Editar `config_naturgy_local.py`

Abre el archivo y completa tus credenciales:

```python
# URL base de Jira (sin barra final)
JIRA_URL = "https://naturgy-adn.atlassian.net"

# Credenciales de autenticación
JIRA_EMAIL = "tu_email@naturgy.com"  # Tu email de Atlassian
JIRA_API_TOKEN = "tu_token_aqui"     # El token que generaste

# Configuración del proyecto
PROJECT_KEY = "DAR"  # Proyecto Darwin
ISSUE_TYPE = "Incidencia"  # Tipo de issue a extraer

# Configuración de extracción
MAX_RESULTS = 100  # Número de resultados por página (máximo 100)
START_AT = 0  # Índice de inicio

# Directorio de salida
OUTPUT_DIR = "EXTRACCION_NATURGY_DAR"

# Configuración de descarga de adjuntos
DOWNLOAD_ATTACHMENTS = True  # Cambiar a False si no quieres descargar adjuntos
MAX_ATTACHMENT_SIZE_MB = 50  # Tamaño máximo de adjunto a descargar
```

### 3. Ajustar configuración según necesites

**Opciones importantes:**

- `DOWNLOAD_ATTACHMENTS`: 
  - `True`: Descarga todos los archivos adjuntos
  - `False`: Solo guarda la información de los adjuntos sin descargarlos
  
- `MAX_ATTACHMENT_SIZE_MB`: Límite de tamaño para descargar adjuntos (en MB)

- `MAX_RESULTS`: Número de issues a procesar por página (máximo 100)

## 🚀 Ejecución

### Ejecutar la extracción completa

```bash
python main_naturgy.py
```

El script:
1. Se conectará a Jira usando tus credenciales
2. Buscará todas las incidencias del proyecto DAR
3. Extraerá la información de cada issue
4. Descargará los adjuntos (si está habilitado)
5. Guardará todo en archivos Markdown y JSON

### Salida esperada

```
================================================================================
🚀 EXTRACTOR DE INCIDENCIAS - NATURGY-ADN DARWIN (DAR)
================================================================================
📍 Proyecto: DAR
📋 Tipo de issue: Incidencia
📁 Directorio de salida: EXTRACCION_NATURGY_DAR
📎 Descargar adjuntos: Sí
================================================================================
🔍 Buscando issues con JQL: project = DAR AND issuetype = "Incidencia" ORDER BY created DESC
📄 Página: 1 (desde 0)

📊 Total de issues encontrados: 896
📄 Procesando 100 issues de esta página...

📋 Procesando: DAR-1234
  💬 5 comentarios
  📎 3 adjuntos
  ✅ Descargado: documento.pdf (2.34 MB)
  ✅ Descargado: imagen.png (0.45 MB)
  ✅ Descargado: log.txt (0.01 MB)
  ✅ Guardado: DAR-1234.md
  ✅ Guardado JSON: DAR-1234.json
...
```

## 📁 Estructura de Archivos Generados

```
EXTRACCION_NATURGY_DAR/
├── RESUMEN_EXTRACCION.md       # Resumen de la extracción
├── DAR-1.md                    # Issue en formato Markdown
├── DAR-1.json                  # Issue en formato JSON
├── DAR-2.md
├── DAR-2.json
├── ...
├── DAR-896.md
├── DAR-896.json
└── attachments/                # Carpeta de adjuntos
    ├── DAR-1/
    │   ├── documento.pdf
    │   └── imagen.png
    ├── DAR-2/
    │   └── archivo.xlsx
    └── ...
```

## 📄 Formato de los Archivos

### Archivo Markdown (.md)

Cada issue se guarda en un archivo Markdown con la siguiente estructura:

```markdown
# DAR-1234: Título del Issue

**URL:** https://naturgy-adn.atlassian.net/browse/DAR-1234

## 📊 Detalles Clave

- **Estado:** En Progreso
- **Prioridad:** Alta
- **Asignado a:** Juan Pérez (juan.perez@naturgy.com)
- **Reportado por:** María García (maria.garcia@naturgy.com)
- **Creado:** 15/01/2024 10:30:00
- **Actualizado:** 20/01/2024 14:45:00
- **Resuelto:** N/A
- **Etiquetas:** bug, urgente
- **Componentes:** Backend, API

## 📝 Descripción

[Descripción completa del issue]

## 💬 Comentarios (5)

### Comentario 1

**Autor:** Juan Pérez (juan.perez@naturgy.com)
**Fecha:** 16/01/2024 09:15:00

[Contenido del comentario]

---

[Más comentarios...]

## 📎 Adjuntos (3)

### documento.pdf

- **Tamaño:** 2456789 bytes
- **Tipo:** application/pdf
- **Subido por:** María García (maria.garcia@naturgy.com)
- **Fecha:** 15/01/2024 10:35:00
- **Archivo local:** `attachments/DAR-1234/documento.pdf`
- **URL:** https://naturgy-adn.atlassian.net/...

[Más adjuntos...]

## 🔧 Campos Personalizados

- **customfield