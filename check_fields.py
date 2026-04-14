#!/usr/bin/env python3
import requests
from configparser import ConfigParser
import json

config = ConfigParser()
config.read('jira_config.ini')
jira_url = config['JIRA']['jira_url']
username = config['JIRA']['username']
api_token = config['JIRA']['api_token']

auth = (username, api_token)

# Obtener una issue de ejemplo para ver todos los campos disponibles
params = {
    'jql': 'project = NC ORDER BY key ASC',
    'maxResults': 1,
    'fields': '*all'
}

response = requests.get(f'{jira_url}/rest/api/3/search/jql', auth=auth, params=params)
if response.status_code == 200:
    data = response.json()
    if data.get('issues'):
        issue = data['issues'][0]
        fields = issue.get('fields', {})
        
        print('Campos personalizados encontrados:')
        print('=' * 80)
        
        # Buscar campos que contengan las palabras clave
        keywords = ['responsable', 'dominio', 'sistema', 'agrupacion', 'jefe', 'proyecto']
        
        for field_key, field_value in sorted(fields.items()):
            if field_key.startswith('customfield_'):
                field_str = str(field_value).lower()
                # Mostrar el campo si contiene alguna palabra clave o tiene valor
                if any(kw in field_str for kw in keywords) or field_value:
                    print(f'\n{field_key}:')
                    if isinstance(field_value, (dict, list)):
                        print(json.dumps(field_value, indent=2, ensure_ascii=False)[:500])
                    else:
                        print(f'  {field_value}')
