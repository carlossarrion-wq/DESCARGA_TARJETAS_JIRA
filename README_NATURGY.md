# 🚀 Extractor de Incidencias Jira - Naturgy-ADN Darwin

Script especializado para extraer las **896 incidencias** del proyecto Darwin (DAR) de Jira Naturgy-ADN.

## ✨ Características

- ✅ Extracción completa de incidencias del proyecto DAR
- ✅ Descarga de comentarios con autor y fecha
- ✅ Descarga automática de archivos adjuntos
- ✅ Exportación en formato Markdown y JSON
- ✅ Campos personalizados incluidos
- ✅ Manejo de paginación automático
- ✅ Progreso en tiempo real

## 📋 Campos Extraídos

Cada incidencia incluye:

### Información Básica
- **Key**: Identificador único (DAR-XXX)
- **Título**: Resumen de la incidencia
- **Descripción**: Descripción completa
- **Estado**: Estado actual
- **Prioridad**: Nivel de prioridad
- **Asignado**: Persona asignada
- **Reportado por**: Quien reportó la incidencia

### Fechas
- **Fecha de Creación**
- **Fecha de Actualización**
- **Fecha de Resolución**

### Información Adicional
- **Etiquetas**: Labels asignadas
- **Componentes**: Componentes del proyecto
- **Comentarios**: Todos los comentarios con autor y fecha
- **Adjuntos**: Archivos adjuntos con opción de descarga
- **Campos Personalizados**: Todos los custom fields

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar credenciales

```bash
# Copiar archivo de configuración
cp config_naturgy.py config_naturgy_local.py

# Editar con tus credenciales
nano config_naturgy_local.py
```

### 3. Ejecutar extracción

```bash
python main_naturgy.py
```

## 📖 Documentación Completa

Para instrucciones detalladas, consulta: [INSTRUCCIONES_NATURGY.md](INSTRUCCIONES_NATURGY.md)

## 📁 Estructura del Proyecto

```
DESCARGA_TARJETAS_JIRA/
├── main_naturgy.py              # Script principal de extracción
├── config_naturgy.py            # Configuración de ejemplo
├── config_naturgy_local.py      # Tu configuración (no se sube a git)
├── INSTRUCCIONES_NATURGY.md     # Instrucciones detalladas
├── README_NATURGY.md            # Este archivo
└── EXTRACCION_NATURGY_DAR/      # Directorio de salida (se crea al ejecutar)
    ├── RESUMEN_EXTRACCION.md
    ├── DAR-1.md
    ├── DAR-1.json
    ├── DAR-2.md
    ├── DAR-2.json
    └── attachments/
        ├── DAR-1/
        └── DAR-2/
```

## 🔐 Seguridad

- El archivo `config_naturgy_local.py` está en `.gitignore`
- Nunca compartas tu API Token
- Los tokens pueden revocarse en cualquier momento desde tu perfil de Atlassian

## 🎯 Diferencias con el Script Original

Este script está optimizado específicamente para:

1. **Proyecto Darwin (DAR)** en lugar de proyectos genéricos
2. **Tipo "Incidencia"** específicamente
3. **896 issues** conocidas de antemano
4. **Formato Markdown** además de JSON para mejor legibilidad
5. **Estructura organizada** con carpetas por issue para adjuntos

## 💡 Consejos

- La primera ejecución puede tardar varios minutos (896 issues)
- Si se interrumpe, puedes ajustar `START_AT` en la configuración para continuar
- Los adjuntos grandes pueden tardar más en descargarse
- Usa `DOWNLOAD_ATTACHMENTS = False` si solo necesitas los metadatos

## 🐛 Solución de Problemas

### Error de autenticación
```
⚠️  No se encontró config_naturgy_local.py
```
**Solución**: Copia `config_naturgy.py` a `config_naturgy_local.py` y configura tus credenciales

### Error de conexión
```
❌ Error al buscar issues
```
**Solución**: Verifica tu conexión a internet y que la URL de Jira sea correcta

### Límite de API
Si recibes errores de límite de API, el script automáticamente espera entre peticiones.

## 📊 Ejemplo de Salida

```
================================================================================
🚀 EXTRACTOR DE INCIDENCIAS - NATURGY-ADN DARWIN (DAR)
================================================================================
📍 Proyecto: DAR
📋 Tipo de issue: Incidencia
📁 Directorio de salida: EXTRACCION_NATURGY_DAR
📎 Descargar adjuntos: Sí
================================================================================

🔍 Buscando issues con JQL: project = DAR AND issuetype = "Incidencia"
📊 Total de issues encontrados: 896
📄 Procesando 100 issues de esta página...

📋 Procesando: DAR-1
  💬 3 comentarios
  📎 2 adjuntos
  ✅ Descargado: screenshot.png (0.45 MB)
  ✅ Descargado: log.txt (0.01 MB)
  ✅ Guardado: DAR-1.md
  ✅ Guardado JSON: DAR-1.json

...

================================================================================
✅ EXTRACCIÓN COMPLETADA
================================================================================
📊 Total de issues extraídos: 896
📁 Archivos guardados en: EXTRACCION_NATURGY_DAR
📎 Adjuntos guardados en: EXTRACCION_NATURGY_DAR/attachments
================================================================================
```

## 🤝 Basado en

Este script está basado en el proyecto original de extracción de Jira, adaptado específicamente para las necesidades del proyecto Darwin de Naturgy-ADN.

## 📝 Licencia

Uso interno - Naturgy-ADN

---

**Última actualización**: Enero 2025