# 📊 Resumen del Proyecto - Extractor Naturgy-ADN Darwin

## 🎯 Objetivo del Proyecto

Crear un script especializado para extraer las **896 incidencias** del proyecto Darwin (DAR) de Jira Naturgy-ADN, incluyendo todos los detalles relevantes, comentarios y archivos adjuntos.

## 📦 Archivos Creados

### Scripts Principales

1. **`main_naturgy.py`** (550+ líneas)
   - Script principal de extracción
   - Maneja paginación automática
   - Descarga de adjuntos
   - Exportación a Markdown y JSON
   - Manejo de errores robusto

2. **`config_naturgy.py`**
   - Archivo de configuración de ejemplo
   - Incluye todas las opciones configurables
   - Documentado con comentarios

3. **`test_naturgy_connection.py`**
   - Script de prueba de conexión
   - Verifica credenciales
   - Cuenta incidencias disponibles
   - Muestra ejemplo de incidencia

### Documentación

4. **`INSTRUCCIONES_NATURGY.md`**
   - Guía paso a paso completa
   - Cómo obtener API Token
   - Configuración detallada
   - Ejemplos de uso
   - Solución de problemas

5. **`README_NATURGY.md`**
   - Resumen ejecutivo del proyecto
   - Inicio rápido
   - Características principales
   - Estructura del proyecto

6. **`RESUMEN_PROYECTO_NATURGY.md`** (este archivo)
   - Visión general del proyecto
   - Archivos creados
   - Próximos pasos

## 🚀 Cómo Empezar

### Paso 1: Configurar Credenciales

```bash
# Copiar archivo de configuración
cp config_naturgy.py config_naturgy_local.py

# Editar con tus credenciales
nano config_naturgy_local.py
```

Necesitas:
- Email de Atlassian
- API Token (obtener en: https://id.atlassian.com/manage-profile/security/api-tokens)

### Paso 2: Probar Conexión

```bash
python test_naturgy_connection.py
```

Este script verificará:
- ✅ Autenticación correcta
- ✅ Acceso al proyecto DAR
- ✅ Número de incidencias disponibles
- ✅ Ejemplo de incidencia

### Paso 3: Ejecutar Extracción

```bash
python main_naturgy.py
```

El script:
1. Se conecta a Jira Naturgy-ADN
2. Busca todas las incidencias del proyecto DAR
3. Extrae información completa de cada una
4. Descarga comentarios y adjuntos
5. Guarda todo en formato Markdown y JSON

## 📁 Estructura de Salida

```
EXTRACCION_NATURGY_DAR/
├── RESUMEN_EXTRACCION.md       # Resumen de la extracción
├── DAR-1.md                    # Incidencia en Markdown
├── DAR-1.json                  # Incidencia en JSON
├── DAR-2.md
├── DAR-2.json
├── ...
├── DAR-896.md
├── DAR-896.json
└── attachments/                # Archivos adjuntos
    ├── DAR-1/
    │   ├── documento.pdf
    │   └── imagen.png
    ├── DAR-2/
    │   └── archivo.xlsx
    └── ...
```

## 📋 Campos Extraídos por Incidencia

### Información Básica
- Key (DAR-XXX)
- Título/Summary
- Descripción completa
- Estado actual
- Prioridad
- Asignado a
- Reportado por

### Fechas
- Fecha de creación
- Fecha de última actualización
- Fecha de resolución

### Contenido Adicional
- Etiquetas (labels)
- Componentes
- **Comentarios completos** (con autor y fecha)
- **Archivos adjuntos** (con opción de descarga)
- Campos personalizados (custom fields)

## 🔧 Configuración Avanzada

### Opciones en `config_naturgy_local.py`

```python
# Descargar o no los adjuntos
DOWNLOAD_ATTACHMENTS = True  # False para solo metadatos

# Tamaño máximo de adjuntos a descargar
MAX_ATTACHMENT_SIZE_MB = 50

# Número de issues por página
MAX_RESULTS = 100  # Máximo permitido por Jira

# Desde dónde empezar (útil si se interrumpe)
START_AT = 0
```

## 📊 Estimación de Tiempo

Para 896 incidencias:

- **Sin adjuntos**: ~15-20 minutos
- **Con adjuntos**: ~30-60 minutos (depende del tamaño)

El script muestra progreso en tiempo real:
```
📋 Procesando: DAR-123
  💬 5 comentarios
  📎 3 adjuntos
  ✅ Descargado: documento.pdf (2.34 MB)
  ✅ Guardado: DAR-123.md
```

## 🎨 Formato Markdown

Cada incidencia se guarda en un archivo `.md` legible:

```markdown
# DAR-123: Título de la Incidencia

**URL:** https://naturgy-adn.atlassian.net/browse/DAR-123

## 📊 Detalles Clave
- **Estado:** En Progreso
- **Prioridad:** Alta
...

## 📝 Descripción
[Descripción completa]

## 💬 Comentarios (5)
[Todos los comentarios con autor y fecha]

## 📎 Adjuntos (3)
[Lista de adjuntos con enlaces]
```

## 🔐 Seguridad

- ✅ `config_naturgy_local.py` está en `.gitignore`
- ✅ No se suben credenciales al repositorio
- ✅ API Token puede revocarse en cualquier momento
- ✅ Conexión segura HTTPS

## 🐛 Solución de Problemas Comunes

### Error: "No se encontró config_naturgy_local.py"
**Solución**: Copia `config_naturgy.py` a `config_naturgy_local.py`

### Error de autenticación
**Solución**: Verifica email y API Token en la configuración

### No se encuentran incidencias
**Solución**: Verifica que el tipo "Incidencia" existe en el proyecto DAR

### Descarga lenta
**Solución**: Desactiva descarga de adjuntos con `DOWNLOAD_ATTACHMENTS = False`

## 📈 Ventajas sobre el Script Original

1. **Especializado para Darwin**: Configurado específicamente para el proyecto DAR
2. **Formato Markdown**: Archivos legibles además de JSON
3. **Mejor organización**: Carpetas separadas por issue para adjuntos
4. **Más información**: Extrae campos personalizados automáticamente
5. **Mejor UX**: Emojis y mensajes claros de progreso
6. **Script de prueba**: Verifica conexión antes de extraer todo

## 🔄 Comparación con Script Original

| Característica | Script Original | Script Naturgy |
|---------------|-----------------|----------------|
| Proyecto | Genérico | Darwin (DAR) |
| Tipo de Issue | Todos | Incidencias |
| Formato salida | CSV | Markdown + JSON |
| Adjuntos | Carpeta única | Por issue |
| Pruebas | No | Sí (test_naturgy_connection.py) |
| Documentación | Básica | Completa |

## 📝 Próximos Pasos

1. **Configurar credenciales** en `config_naturgy_local.py`
2. **Probar conexión** con `test_naturgy_connection.py`
3. **Ejecutar extracción** con `main_naturgy.py`
4. **Revisar resultados** en `EXTRACCION_NATURGY_DAR/`

## 💡 Consejos Útiles

- Ejecuta primero el script de prueba para verificar todo
- Si tienes muchos adjuntos grandes, considera desactivar la descarga inicialmente
- Los archivos Markdown son perfectos para revisar en GitHub o editores de texto
- Los archivos JSON son ideales para procesamiento automatizado
- Puedes interrumpir con Ctrl+C y reanudar ajustando `START_AT`

## 📞 Soporte

Para problemas o dudas:
1. Revisa `INSTRUCCIONES_NATURGY.md`
2. Ejecuta `test_naturgy_connection.py` para diagnóstico
3. Verifica los logs de error en la consola

---

**Proyecto creado**: Enero 2025  
**Basado en**: Script original de extracción de Jira  
**Optimizado para**: Naturgy-ADN Darwin (DAR)  
**Total de incidencias objetivo**: 896