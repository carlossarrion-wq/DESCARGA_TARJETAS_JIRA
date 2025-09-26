# Descargador de Tareas JIRA

Programa optimizado para descargar todas las tareas de un proyecto JIRA a formato CSV de forma eficiente.

## Características

- **Eficiente**: Maneja cientos de tareas con paginación optimizada
- **Completo**: Extrae todos los campos relevantes incluyendo comentarios e histórico
- **Rápido**: Procesamiento optimizado con indicadores de progreso
- **Fácil de usar**: Interfaz interactiva por consola

## Campos Exportados

El CSV incluye las siguientes columnas:

- **Key**: Identificador único de la tarea
- **Título**: Resumen de la tarea
- **Descripción**: Descripción completa (texto plano)
- **Estado**: Estado actual de la tarea
- **Tipo**: Tipo de issue (Bug, Story, Task, etc.)
- **Prioridad**: Prioridad asignada
- **Asignado**: Persona asignada a la tarea
- **Reportado por**: Quien reportó la tarea
- **Fecha Creación**: Cuándo se creó la tarea
- **Fecha Actualización**: Última actualización
- **Fecha Resolución**: Cuándo se resolvió (si aplica)
- **Resolución**: Tipo de resolución
- **Etiquetas**: Labels asignadas
- **Componentes**: Componentes del proyecto
- **Versiones**: Versiones de corrección
- **Comentarios**: Todos los comentarios con fecha y autor
- **Histórico**: Registro completo de cambios

## Requisitos

- Python 3.7 o superior
- Acceso a JIRA con API Token

## Instalación

1. Clona o descarga los archivos
2. Instala las dependencias:

```bash
pip3 install -r requirements.txt
```

## Configuración de JIRA

### Obtener API Token

1. Ve a tu perfil de JIRA (Atlassian Account)
2. Selecciona "Security" → "Create and manage API tokens"
3. Crea un nuevo token y guárdalo de forma segura

### URL de JIRA

- Para JIRA Cloud: `https://tuempresa.atlassian.net`
- Para JIRA Server: `https://jira.tuempresa.com`

## Uso

Ejecuta el programa:

```bash
python3 main.py
```

El programa te pedirá:

1. **URL de JIRA**: La URL base de tu instancia JIRA
2. **Email/Usuario**: Tu email de usuario de JIRA
3. **API Token**: El token generado anteriormente
4. **Clave del Proyecto**: El identificador del proyecto (ej: GADEA)

### Ejemplo de Ejecución

```
=== Descargador de Tareas JIRA ===

URL de JIRA (ej: https://company.atlassian.net): https://miempresa.atlassian.net
Email/Usuario: usuario@empresa.com
API Token: ATBBxxxxxxxxxxxxxxxxxxx
Clave del Proyecto (ej: GADEA): GADEA

✓ Conectado como: Juan Pérez
Descargando issues del proyecto GADEA...
Descargadas 100 de 247 issues...
Descargadas 200 de 247 issues...
Descargadas 247 de 247 issues...
✓ Total descargadas: 247 issues
Procesando datos...
Procesando issue 50/247...
Procesando issue 100/247...
Procesando issue 150/247...
Procesando issue 200/247...
Exportando 247 issues a GADEA_issues_20231223_143052.csv...
✓ Archivo CSV creado: GADEA_issues_20231223_143052.csv

✓ Proceso completado en 45.32 segundos
✓ Archivo generado: GADEA_issues_20231223_143052.csv
```

## Optimizaciones para Grandes Volúmenes

El programa está optimizado para manejar proyectos con cientos de tareas:

- **Paginación**: Descarga en lotes de 100 tareas
- **Campos selectivos**: Solo obtiene los campos necesarios
- **Procesamiento eficiente**: Muestra progreso cada 50 tareas
- **Manejo de memoria**: Procesa las tareas de forma secuencial
- **Rate limiting**: Pausa breve entre requests para no sobrecargar el servidor

## Formato del Archivo CSV

- **Nombre**: `{PROYECTO}_issues_{YYYYMMDD_HHMMSS}.csv`
- **Codificación**: UTF-8
- **Separador**: Coma (,)
- **Texto**: Entrecomillado cuando contiene comas o saltos de línea

## Solución de Problemas

### Error de Autenticación
- Verifica que el email y API token sean correctos
- Asegúrate de que el token no haya expirado
- Confirma que tienes permisos para acceder al proyecto

### Error de Conexión
- Verifica la URL de JIRA
- Comprueba tu conexión a internet
- Asegúrate de que JIRA esté accesible

### Proyecto No Encontrado
- Verifica que la clave del proyecto sea correcta
- Confirma que tienes permisos para ver el proyecto
- El proyecto debe existir y estar activo

### Rendimiento Lento
- El tiempo depende del número de tareas y comentarios
- Para proyectos muy grandes (>1000 tareas), considera ejecutar en horarios de menor carga
- La primera descarga puede ser más lenta debido a la carga del histórico completo

## Limitaciones

- Descripción y comentarios limitados a 1000 caracteres por campo para optimizar el CSV
- Requiere permisos de lectura en el proyecto JIRA
- Funciona con JIRA Cloud y Server (API v3)

## Soporte

Para incidencias del sistema GADEA, este programa captura toda la información relevante incluyendo:
- Comentarios completos del proceso de resolución
- Histórico detallado de cambios de estado
- Información de asignación y fechas clave
- Componentes y versiones relacionadas
