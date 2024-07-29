import requests
import json
from typing import Dict, Union, List, Any
import os
from dotenv import load_dotenv

load_dotenv('./services/.env')

username = os.getenv('GRAFANA_USER') # Вставить user, с помощью которого логинимся в web
password = os.getenv('GRAFANA_PASS') # Вставить pass, с помощью которого логинимся в web
path_dashboard_json = 'dashboard.json' # Путь к файлу с дашбородом

print(f'grafana user: {username}')
print(f'grafana password: {password}')
# URL для Grafana API c user-password авторизацией
url = "http://{username}:{password}@localhost:3000/api/datasources/1"

# Получаем данные о prometheus datasource
auth_response = requests.get(url.format(username=username, password=password))
# Привер ответа:
# {"id":1,"uid":"edn9q01pibn5sd","orgId":1,"name":"prometheus","type":"prometheus","typeLogoUrl":"public/app/plugins/datasource/prometheus/img/prometheus_logo.svg","access":"proxy","url":"http://prometheus:9090/","user":"","database":"","basicAuth":false,"basicAuthUser":"","withCredentials":false,"isDefault":true,"jsonData":{"httpMethod":"POST"},"secureJsonFields":{},"version":4,"readOnly":false}
prom_datasource = auth_response.json()
# Получаем uid подключенного datasource 
current_uid = prom_datasource['uid']

# Загружаем дашборд в виде словаря
with open(path_dashboard_json, 'r') as fd:
    dashboard = json.load(fd)
print('current uid: {}'.format(current_uid))


def substitution_datasource_uid(
    dashboard: Union[List[Any], Dict[str, Any], Any], 
    current_uid
    ) -> None:
    '''
    Рекурсивная замена в словаре uid datasource prometheus
    '''
    
    if isinstance(dashboard, dict):
        for k, v in dashboard.items():
            if k == "datasource":
                if v["type"] == "prometheus":
                    v["uid"] = current_uid
            else:
                substitution_datasource_uid(v, current_uid)
    elif isinstance(dashboard, list):
        for elem in dashboard:
            substitution_datasource_uid(elem, current_uid)
    else:
        return 

# Заменяем uid
substitution_datasource_uid(dashboard, current_uid)
print("Fix uid done")

# Перезаписываем файл с дашбордом
with open(path_dashboard_json, 'w') as fd:
    json.dump(dashboard, fd, indent=2)

