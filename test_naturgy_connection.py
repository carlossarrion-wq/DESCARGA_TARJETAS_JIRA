#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con Jira Naturgy-ADN
y obtener información sobre el proyecto Darwin
"""

import sys
import requests
from requests.auth import HTTPBasicAuth

# Intentar importar la configuración local
try:
    from config_naturgy_local import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, PROJECT_KEY, ISSUE_TYPE
except ImportError:
    print("❌ Error: No se encontró config_naturgy_local.py")
    print("📝 Por favor, copia config_naturgy.py a config_naturgy_local.py y configura tus credenciales")
    sys.exit(1)


def test_connection():
    """Prueba la conexión básica a Jira"""
    print("=" * 80)
    print("🔍 PRUEBA DE CONEXIÓN - JIRA NATURGY-ADN")
    print("=" * 80)
    
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Test 1: Verificar autenticación
    print("\n1️⃣ Verificando autenticación...")
    try:
        response = requests.get(
            f"{JIRA_URL}/rest/api/3/myself",
            headers=headers,
            auth=auth,
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✅ Autenticación exitosa")
            print(f"   👤 Usuario: {user_data.get('displayName', 'Desconocido')}")
            print(f"   📧 Email: {user_data.get('emailAddress', 'Desconocido')}")
        else:
            print(f"   ❌ Error de autenticación: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False
    
    # Test 2: Verificar acceso al proyecto
    print(f"\n2️⃣ Verificando acceso al proyecto {PROJECT_KEY}...")
    try:
        response = requests.get(
            f"{JIRA_URL}/rest/api/3/project/{PROJECT_KEY}",
            headers=headers,
            auth=auth,
            timeout=10
        )
        
        if response.status_code == 200:
            project_data = response.json()
            print(f"   ✅ Acceso al proyecto confirmado")
            print(f"   📁 Nombre: {project_data.get('name', 'Desconocido')}")
            print(f"   🔑 Key: {project_data.get('key', 'Desconocido')}")
        else:
            print(f"   ❌ Error accediendo al proyecto: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Contar incidencias
    print(f"\n3️⃣ Contando incidencias de tipo '{ISSUE_TYPE}'...")
    try:
        jql = f'project = {PROJECT_KEY} AND issuetype = "{ISSUE_TYPE}"'
        params = {
            "jql": jql,
            "maxResults": 1,  # Mínimo permitido
            "fields": "key"
        }
        
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
            print(f"   ✅ Consulta exitosa")
            print(f"   📊 Total de incidencias encontradas: {total}")
            
            if total == 0:
                print(f"   ⚠️  No se encontraron incidencias. Verifica:")
                print(f"      - Que el tipo de issue '{ISSUE_TYPE}' existe en el proyecto")
                print(f"      - Que tienes permisos para ver las incidencias")
        else:
            print(f"   ❌ Error en la consulta: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 4: Obtener una incidencia de ejemplo
    print(f"\n4️⃣ Obteniendo una incidencia de ejemplo...")
    try:
        jql = f'project = {PROJECT_KEY} AND issuetype = "{ISSUE_TYPE}" ORDER BY created DESC'
        params = {
            "jql": jql,
            "maxResults": 1,
            "fields": "key,summary,status,priority,created,comment,attachment"
        }
        
        response = requests.get(
            f"{JIRA_URL}/rest/api/3/search/jql",
            headers=headers,
            auth=auth,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            issues = data.get('issues', [])
            
            if issues:
                issue = issues[0]
                fields = issue.get('fields', {})
                key = issue.get('key', 'UNKNOWN')
                
                print(f"   ✅ Incidencia de ejemplo obtenida")
                print(f"   🔑 Key: {key}")
                print(f"   📝 Título: {fields.get('summary', 'Sin título')}")
                print(f"   📊 Estado: {fields.get('status', {}).get('name', 'Desconocido')}")
                print(f"   ⚡ Prioridad: {fields.get('priority', {}).get('name', 'Sin prioridad')}")
                
                # Comentarios
                comments = fields.get('comment', {}).get('comments', [])
                print(f"   💬 Comentarios: {len(comments)}")
                
                # Adjuntos
                attachments = fields.get('attachment', [])
                print(f"   📎 Adjuntos: {len(attachments)}")
                
                print(f"\n   🔗 URL: {JIRA_URL}/browse/{key}")
            else:
                print(f"   ⚠️  No se encontraron incidencias para mostrar")
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Resumen final
    print("\n" + "=" * 80)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 80)
    print("\n🚀 Puedes ejecutar el script principal con:")
    print("   python main_naturgy.py")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    try:
        success = test_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)