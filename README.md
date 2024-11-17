## Запуск и установка

Установите зависимости

```shell
pip -r install requirements.txt
```
Настройте файл **config.py**

```json
{
  "base_protocol": "http",
  "debug": false,
  "server_workers": 4,
  "host": "0.0.0.0",
  "port": "8000",
  "log_level": "info",
  "open_endpoints": [
    "/your/endpoint"
  ],
  "redirects": {
    "auth": {
      "hostname": "auth",
      "port": 8000
    },
    "your": {
      "hostname": "some-hostname",
      "port": 8000
    }
  },
  "protect_endpoints": [
    "/your/endpoint"
  ]
}
```
- base_protocol - протокол обмена (http/https)
- debug - режим отладки сервера Starlette *
- server_workers - количество workers uvicorn *
- host - host для Starlette
- port - порт для Starlette
- log_level - уровень информирование логов Starlette 
- open_endpoints - список конечных точек, **которые не проходят** авторизацию в сервисе auth
- protect_endpoints - список конечных точек, **которые проходят** авторизацию в сервисе auth
- redirects - состоит из адреса (hostname) и порта (port), куда нужно перенаправить конечную точку
> '*' - (работает только если запускать через исполняемый файл _**python main.py**_)

Запустить проект можно с помощью (dev/prod среда):

```shell
python main.py
```

Или используя **gunicorn** и **uvicorn-worker** (только prod среда)

```shell
gunicorn main:app -w 4 -k uvicorn_worker.UvicornWorker --bind=0.0.0.0:6100
```
