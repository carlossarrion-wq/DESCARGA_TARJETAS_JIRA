#!/usr/bin/env python3
"""
Script para verificar permisos y buscar issues en el proyecto Darwin
"""

import sys
import requests
from requests.auth import HTTPBasicAuth

try:
    from config_naturgy_local import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, PROJECT_KEY
except ImportError:
    print("❌ Error: No se encontró config_naturgy_local.py")
    sys.exit(1)

print("=" * 80)
print("🔍 VERIFICANDO PERMISOS Y BUSCANDO ISSUES")
print("=" * 80)

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Test 1: Buscar TODOS los issues del proyecto sin filtro de tipo
print(f"\n1️⃣ Buscando TODOS los issues del proyecto {PROJECT_KEY}...\n")

jql = f'project = {PROJECT_KEY}'
params = {
    "jql": jql,
    "maxResults": 10,
    "fields": "key,summary,issuetype,status"
}

try:
    response = requests.get(
        f"{JIRA_URL}/rest/api/3/search/jql",
        headers=headers,
        auth=auth,
        params=params,
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        total = data.get('total', 0)
        issues = data.get('issues', [])
        
        print(f"✅ Total de issues en el proyecto: {total}\n")
        
        if issues:
            print("📋 Primeros 10 issues encontrados:\n")
            print("-" * 80)
            
            for issue in issues:
                key = issue.get('key', 'N/A')
                fields = issue.get('fields', {})
                summary = fields.get('summary', 'Sin título')
                issue_type = fields.get('issuetype', {}).get('name', 'Desconocido')
                status = fields.get('status', {}).get('name', 'Desconocido')
                
                print(f"🔑 {key}")
                print(f"   Tipo: {issue_type}")
                print(f"   Título: {summary[:60]}...")
                print(f"   Estado: {status}")
                print("-" * 80)
        else:
            print("⚠️  No se encontraron issues")
            
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Respuesta: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Contar por tipo de issue
print(f"\n2️⃣ Contando issues por tipo:\n")

issue_types = ["Tarea", "Subtarea", "Historia", "Fallo", "Épica"]

for issue_type in issue_types:
    jql = f'project = {PROJECT_KEY} AND issuetype = "{issue_type}"'
    params = {
        "jql": jql,
        "maxResults": 1,
        "fields": "key"
    }
    
    try:
        response = requests.get(
            f"{JIRA_URL}/rest/api/3/search/jql",
            headers=headers,
            auth=auth,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            print(f"   📊 {issue_type}: {total} issues")
        else:
            print(f"   ❌ {issue_type}: Error {response.status_code}")
    except Exception as e:
        print(f"   ❌ {issue_type}: Error - {e}")

print("\n" + "=" * 80)