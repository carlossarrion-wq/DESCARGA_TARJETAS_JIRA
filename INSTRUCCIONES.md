# Instrucciones de Uso - Descargador de Tareas JIRA

## Instalación Inicial

### 1. Crear Entorno Virtual (Recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate  # En Windows
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Configuración de JIRA

### Obtener API Token

1. Accede a tu cuenta de Atlassian: https://id.atlassian.com/manage-profile/security/api-tokens
2. Haz clic en "Create API token"
3. Dale un nombre descriptivo (ej: "Descargador JIRA")
4. Copia el token generado (guárdalo de forma segura)

### Información Necesaria

- **URL de JIRA**: La URL de tu instancia (ej: `https://tuempresa.atlassian.net`)
- **Email**: Tu email de usuario de JIRA
- **API Token**: El token que acabas de generar
- **Clave del Proyecto**: El identificador del proyecto (ej: `GADEA`, `PROJ`, etc.)

## Ejecución del Programa

### Activar el Entorno Virtual (si lo creaste)

```bash
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate  # En Windows
```

### Ejecutar el Script

```bash
python3 main.py
```

### Flujo de Ejecución

1. El programa te pedirá la URL de JIRA
2. Luego tu email/usuario
3. Después el API Token
4. Finalmente la clave del proyecto

5. El programa descargará todas las tarjetas y generará un archivo CSV

6. Te preguntará si deseas descargar los archivos adjuntos:
   - Responde `s` para descargar los adjuntos
   - Responde `n` para omitir la descarga

## Archivos Generados

### Archivo CSV
- **Nombre**: `{PROYECTO}_issues_{FECHA}_{HORA}.csv`
- **Ubicación**: Directorio actual
- **Contenido**: Todas las tarjetas con sus campos

### Archivos Adjuntos (si se descargan)
- **Directorio**: `{PROYECTO}_attachments_{FECHA}_{HORA}/`
- **Estructura**: 
  ```
  PROYECTO_attachments_20231223_143052/
  ├── PROYECTO-1/
  │   ├── PROYECTO-1_archivo1.pdf
  │   └── PROYECTO-1_imagen.png
  ├── PROYECTO-2/
  │   └── PROYECTO-2_documento.docx
  └── ...
  ```
- **Nota**: Los archivos se guardan con el prefijo del ID de la tarjeta para facilitar su identificación

## Ejemplo Completo

```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Ejecutar programa
python3 main.py

# 3. Introducir datos cuando se soliciten:
URL de JIRA (ej: https://company.atlassian.net): https://miempresa.atlassian.net
Email/Usuario: usuario@empresa.com
API Token: ATBBxxxxxxxxxxxxxxxxxxx
Clave del Proyecto (ej: GADEA): GADEA

# 4. Esperar a que descargue las tarjetas
✓ Conectado como: Juan Pérez
Descargando issues del proyecto GADEA...
✓ Total descargadas: 247 issues

# 5. Decidir sobre los adjuntos
¿Descargar archivos adjuntos? (s/n): s

# 6. Esperar a que termine
✓ Proceso completado en 52.18 segundos
✓ Archivo CSV generado: GADEA_issues_20231223_143052.csv
```

## Solución de Problemas

### Error: "externally-managed-environment"
- **Solución**: Usa un entorno virtual (ver sección "Crear Entorno Virtual")

### Error de Autenticación
- Verifica que el email y API token sean correctos
- Asegúrate de que el token no haya expirado
- Confirma que tienes permisos para acceder al proyecto

### Error de Conexión
- Verifica la URL de JIRA (debe incluir `https://`)
- Comprueba tu conexión a internet
- Asegúrate de que JIRA esté accesible

### Proyecto No Encontrado
- Verifica que la clave del proyecto sea correcta (distingue mayúsculas/minúsculas)
- Confirma que tienes permisos para ver el proyecto

## Desactivar Entorno Virtual

Cuando termines de usar el programa:

```bash
deactivate
```

## Notas Importantes

- El API Token es sensible, no lo compartas ni lo subas a repositorios públicos
- Los archivos CSV y directorios de adjuntos están excluidos del control de versiones (.gitignore)
- Para proyectos grandes, la descarga puede tardar varios minutos
- Los adjuntos se descargan con una pausa entre cada uno para no sobrecargar el servidor
