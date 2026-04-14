# 🚀 Cómo Ejecutar la Extracción - Naturgy-ADN Darwin

## ✅ Estado Actual

**Todo está configurado y listo para usar:**

- ✅ Credenciales configuradas correctamente
- ✅ Conexión a Jira verificada
- ✅ Acceso al proyecto Darwin (DAR) confirmado
- ✅ Tipo de issue identificado: **"Incidencia"**
- ✅ Issue de ejemplo encontrado: DAR-5694

## 📊 Información del Proyecto

- **Proyecto**: Darwin (DAR)
- **URL**: https://naturgy-adn.atlassian.net
- **Usuario**: CARLOS SARRION (carlos.sarrion@es.ibm.com)
- **Tipos de issues disponibles**:
  - Incidencia
  - Defecto
  - Soporte sin PaP
  - Tarea
  - Subtarea

## 🎯 Opciones de Extracción

### Opción 1: Extraer solo "Incidencias" (Configuración actual)

```bash
python3 main_naturgy.py
```

Esto extraerá todos los issues de tipo "Incidencia" del proyecto DAR.

### Opción 2: Extraer "Incidencias" y "Defectos"

Si quieres extraer tanto Incidencias como Defectos, edita `config_naturgy_local.py` y cambia:

```python
ISSUE_TYPE = "Incidencia"
```

Por una consulta JQL más amplia. O mejor aún, modifica directamente el JQL en `main_naturgy.py` línea 60:

```python
# Cambiar esto:
jql = f'project = {PROJECT_KEY} AND issuetype = "{ISSUE_TYPE}" ORDER BY created DESC'

# Por esto:
jql = f'project = {PROJECT_KEY} AND issuetype IN ("Incidencia", "Defecto") ORDER BY created DESC'
```

### Opción 3: Extraer TODOS los issues del proyecto

Para extraer todos los tipos de issues:

```python
# En main_naturgy.py línea 60:
jql = f'project = {PROJECT_KEY} ORDER BY created DESC'
```

## 🚀 Ejecutar la Extracción

### Paso 1: Verificar la conexión (Opcional pero recomendado)

```bash
python3 test_naturgy_connection.py
```

Deberías ver:
```
✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE
```

### Paso 2: Ejecutar la extracción

```bash
python3 main_naturgy.py
```

### Paso 3: Esperar a que termine

El script mostrará el progreso en tiempo real:

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
📊 Total de issues encontrados: XXX
📄 Procesando 100 issues de esta página...

📋 Procesando: DAR-5694
  💬 0 comentarios
  📎 0 adjuntos
  ✅ Guardado: DAR-5694.md
  ✅ Guardado JSON: DAR-5694.json
...
```

## 📁 Resultados

Los archivos se guardarán en:

```
EXTRACCION_NATURGY_DAR/
├── RESUMEN_EXTRACCION.md       # Resumen de la extracción
├── DAR-5694.md                 # Issue en Markdown
├── DAR-5694.json               # Issue en JSON
├── DAR-5693.md
├── DAR-5693.json
└── attachments/                # Adjuntos (si hay)
    ├── DAR-5694/
    └── DAR-5693/
```

## ⚙️ Configuración Avanzada

### Desactivar descarga de adjuntos

Si solo quieres los metadatos sin descargar archivos, edita `config_naturgy_local.py`:

```python
DOWNLOAD_ATTACHMENTS = False
```

### Cambiar tamaño máximo de adjuntos

```python
MAX_ATTACHMENT_SIZE_MB = 100  # Aumentar a 100 MB
```

### Continuar una extracción interrumpida

Si la extracción se interrumpe, puedes continuar desde donde quedó:

```python
START_AT = 500  # Continuar desde el issue 500
```

## 📊 Tiempo Estimado

- **Sin adjuntos**: ~5-10 minutos para cientos de issues
- **Con adjuntos**: Depende del tamaño y cantidad de archivos

## 🐛 Solución de Problemas

### Error: "No se encontró config_naturgy_local.py"
**Solución**: El archivo ya existe, verifica que estés en el directorio correcto.

### Error de autenticación
**Solución**: Las credenciales ya están configuradas y funcionan correctamente.

### No se encuentran issues
**Solución**: Ya verificamos que hay issues disponibles. Si no aparecen, verifica el tipo de issue en la configuración.

## 📞 Scripts Útiles

- `test_naturgy_connection.py` - Verifica la conexión
- `discover_issue_types.py` - Muestra todos los tipos de issues disponibles
- `check_permissions.py` - Verifica permisos y muestra issues de ejemplo

## 🎉 ¡Listo para Usar!

Todo está configurado correctamente. Solo ejecuta:

```bash
python3 main_naturgy.py
```

Y el script comenzará a extraer todos los issues del proyecto Darwin.

---

**Última verificación**: 14/04/2026 15:41
**Estado**: ✅ Operativo
**Issue de prueba**: DAR-5694 encontrado correctamente