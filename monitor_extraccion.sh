#!/bin/bash
# Script para monitorear el progreso de la extracción

echo "🔍 MONITOR DE EXTRACCIÓN - NATURGY-ADN DARWIN"
echo "=============================================="
echo ""

while true; do
    clear
    echo "🔍 MONITOR DE EXTRACCIÓN - NATURGY-ADN DARWIN"
    echo "=============================================="
    echo ""
    echo "⏰ Hora actual: $(date '+%H:%M:%S')"
    echo ""
    
    # Contar archivos .md
    count=$(ls -1 EXTRACCION_NATURGY_DAR/*.md 2>/dev/null | wc -l | tr -d ' ')
    echo "📊 Issues extraídos: $count"
    echo ""
    
    # Verificar si existe el resumen (indica que terminó)
    if [ -f "EXTRACCION_NATURGY_DAR/RESUMEN_EXTRACCION.md" ]; then
        echo "✅ ¡EXTRACCIÓN COMPLETADA!"
        echo ""
        cat EXTRACCION_NATURGY_DAR/RESUMEN_EXTRACCION.md
        break
    else
        echo "⏳ Extracción en progreso..."
        echo ""
        echo "Últimos 5 issues extraídos:"
        ls -t EXTRACCION_NATURGY_DAR/*.md 2>/dev/null | head -5 | xargs -n1 basename | sed 's/.md$//'
    fi
    
    echo ""
    echo "Presiona Ctrl+C para salir del monitor"
    echo "Actualizando en 5 segundos..."
    
    sleep 5
done