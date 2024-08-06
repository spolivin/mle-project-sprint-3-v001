# Инструкции по запуску микросервиса

## 1. FastAPI микросервис в виртуальном окружение

Для того чтобы запустить приложение, необходимо сначала подготовить виртуальное окружение, а потом запустить сервер `uvicorn` (команды вводить из корневой директории):

```bash
# Preparing virtual env
sudo apt-get update
sudo apt-get install python3.10-venv
python3.10 -m venv .venv_fastapi_app
source .venv_fastapi_app/bin/activate
pip install -r services/requirements.txt

# Changing working dir
cd services

# Launching uvicorn server on port 1702
sh run_uvicorn_server.sh 1702
```

После выполнение приведенных выше команд запустится сервер `uvicorn` по адресу http://localhost:1702, к которому уже можно посылать запросы. 

### Пример curl-запроса к микросервису

Тестовый запрос можно сделать, открыв новый терминал и запустив [*shell*-скрипт](services/send_test_request.sh) из директории `services`, который будет обращаться к серверу по порту 1702 для `flat_id=101` (при необходимости стоит сначала активировать виртуальное окружение через `source .venv_fastapi_app/bin/activate`):
```bash
cd services

sh send_test_request.sh 1702 101
```
Потребуется немного времени, чтобы все препроцессоры обработали входные данные, после чего можно будет видеть ответ сервера в терминале. 

> Remark: По завершении работы с сервером нажмите Ctrl+C, чтобы остановить работу приложения.

## 2. FastAPI микросервис в Docker-контейнере

Следующая последовательность команд из корневой директории позволит запустить сервис в docker-контейнере:
```bash
# Changing working dir
cd services

# Building the image
docker image build . --tag price-prediction-app --file Dockerfile_ml_service

# Running Docker container
docker container run --publish 4600:1702 --env-file .env price-prediction-app
```

Для того чтобы можно было получить доступ и к веб-интерфейсу, после выполнения `docker run` необходимо не забыть перенаправить порт с 1702 на 4600 и вручную во вкладке PORTS в VSCode. Сервис будет теперь доступен по адресу http://localhost:4600.

### Пример curl-запроса к микросервису

Чтобы отправить запрос к серверу, запущенному в контейнере, мы можем переиспользовать написанный скрипт `services/send_test_request.sh` с аргументом перенаправленного порта 1702 на 4600 и номером квартиры из нового терминала:
```bash
cd services

sh send_test_request.sh 4600 10900
```

> Remark: По завершению работы с контейнером рекомендуется выполнить команду `docker container stop <container-id>` для остановки. Так же во избежание ошибок стоит удалить порт из вкладки PORTS в VS Code.

## 3. Docker compose для микросервиса и системы моониторинга

Для запуска приложения вместе с системой мониторинга *Prometheus* и *Grafana*, необходимо выполнить следующие команды из корневой директории:

```bash
# Changing working dir
cd services

# Launching services via Docker Compose
docker compose up --build
```

### Пример curl-запроса к микросервису

Запрос делаем при помощи того же скрипта следующим образом:

```bash
cd services

sh send_test_request.sh 1702 109
```

> Remark: По завершению работы с сервисом рекомендуется выполнить команду `docker compose down` для остановки и последующего удаления контейнеров.

## 4. Скрипт симуляции нагрузки

Для симуляции нагрузки на сервер можно использовать скрипт [`services/simulate_server_load.py`](services/simulate_service_load.py), который генерирует 30 запросов, после каждого из которых делается пауза в 2 секунды, а также дополнительная пауза в 30 секунд после 15-ого послатого запроса. 

Скрипт запускается в отдельном терминале после следующих команд из корневой директории:
```bash
cd services
python simulate_service_load.py --port 1702
```

Адреса сервисов:
- микросервис: http://localhost:1702
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000


## 5. Загрузка готового дашборда

Для того чтобы загрузить уже готовый дашборд в *Grafana*, необходимо произвести следующие шаги после запуска сервиса через *Docker Compose*:

1. Убедиться, что порты 3000 и 9090 перенаправлены и доступны на вкладке PORTS в VS Code.
2. Перейти на http://localhost:3000 и войти в учетную запись *Grafana*, используя логин и пароль из `services/.env`.
3. Указать *Prometheus* в *Data sources* с адресом `http://prometheus:9090`.
4. Запустить скрипт при помощи команды `python fix_datasource_uid.py` из корневой директории для того чтобы скорректировать *UID* для текущей сессии *Grafana* и загрузки дашборда.
5. Перейти на вкладку *Dashboards* в *Grafana* и перейти на *New* -> *Import*. Там достаточно скопировать и вставить содержимое файла `dashboard.json` и нажать *Load*.
