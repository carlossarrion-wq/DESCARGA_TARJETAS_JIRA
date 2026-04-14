#!/usr/bin/env python3
"""
Script para descubrir los tipos de issues disponibles en el proyecto Darwin
"""

import sys
import requests
from requests.auth import HTTPBasicAuth
import json

try:
    from config_naturgy_local import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, PROJECT_KEY
except ImportError:
    print("❌ Error: No se encontró config_naturgy_local.py")
    sys.exit(1)

print("=" * 80)
print("🔍 DESCUBRIENDO TIPOS DE ISSUES EN EL PROYECTO DARWIN")
print("=" * 80)

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Obtener información del proyecto incluyendo tipos de issues
print(f"\n📋 Obteniendo tipos de issues del proyecto {PROJECT_KEY}...\n")

try:
    response = requests.get(
        f"{JIRA_URL}/rest/api/3/project/{PROJECT_KEY}",
        headers=headers,
        auth=auth,
        timeout=10
    )
    
    if response.status_code == 200:
        project_data = response.json()
        issue_types = project_data.get('issueTypes', [])
        
        print(f"✅ Tipos de issues disponibles en {PROJECT_KEY}:\n")
        print("-" * 80)
        
        for issue_type in issue_types:
            name = issue_type.get('name', 'Desconocido')
            description = issue_type.get('description', 'Sin descripción')
            id = issue_type.get('id', 'N/A')
            
            print(f"📌 Nombre: {name}")
            print(f"   ID: {id}")
            print(f"   Descripción: {description}")
            print("-" * 80)
        
        # Intentar buscar issues con cada tipo
        print("\n🔍 Contando issues por tipo:\n")
        
        for issue_type in issue_types:
            name = issue_type.get('name', '')
            jql = f'project = {PROJECT_KEY} AND issuetype = "{name}"'
            
            params = {
                "jql": jql,
                "maxResults": 1,
                "fields": "key"
            }
            
            try:
                search_response = requests.get(
                    f"{JIRA_URL}/rest/api/3/search/jql",
                    headers=headers,
                    auth=auth,
                    params=params,
                    timeout=10
                )
                
                if search_response.status_code == 200:
                    data = search_response.json()
                    total = data.get('total', 0)
                    print(f"   📊 {name}: {total} issues")
                else:
                    print(f"   ❌ {name}: Error {search_response.status_code}")
            except Exception as e:
                print(f"   ❌ {name}: Error - {e}")
        
        print("\n" + "=" * 80)
        print("✅ ANÁLISIS COMPLETADO")
        print("=" * 80)
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Respuesta: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()