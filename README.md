![GitHub Workflow Status](https://img.shields.io/github/workflow/status/igroykt/letsencrypt-godaddy/letsencrypt-godaddy%20build)
![GitHub](https://img.shields.io/github/license/igroykt/letsencrypt-godaddy)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/igroykt/letsencrypt-godaddy)

# LetsEncrypt GoDaddy
Приложение для выписки wildcard сертификатов посредством DNS challenge для Linux

## Зависимости
* Python 3.8
* Golang 1.16
* Certbot 1.13

## Установка
```
pip3 install -r requirements.txt
go get gopkg.in/ini.v1
go env -w GO111MODULE=auto
mv config.sample.ini config.ini
# подправить config.ini
./compile.py
rm -f auth.py clean.py main.go
```

## Настройка
Про генерацию APIKEY и APISECRET читайте тут https://developer.godaddy.com/getstarted. Если сайт отображается некорректно, то попробуйте поменять язык браузера на английский (обычно помогает).

APIKEY и APISECRET прописать в main.go в "Configuration section".

**[GENERAL]**

| Function      | Description                                                            | Default value          |
|---------------|------------------------------------------------------------------------|------------------------|
| ZONE          | Список доменных зон (разделенных запятыми)                             | None                   |
| ADMIN_EMAIL   | E-mail администратора certbot                                          | None                   |
| TTL           | Время жизни TXT записей                                                | 600                    |
| SLEEP         | Время ожидания пока TXT запись подхватится публичными DNS серверами    | 120                    |
| OS_SHELL      | Shell операционной системы                                             | /bin/bash              |
| LE_CONFIG_DIR | Путь к директории для хранения конфигураций и сертификатов LetsEncrypt | /etc/letsencrypt       |
| PYTHON        | Путь к интерпретатору Python                                           | /usr/bin/python3       |
| CERTBOT       | Путь к certbot                                                         | /usr/local/bin/certbot |

LE_CONFIG_DIR полезен в том случае, когда для некоторых ресурсов надо выписывать сертификаты по http challenge, а некоторые по dns challenge. В таком случае для dns challenge можно указать путь скажем /etc/letsencrypt-dns, тогда будет создана эта директория и аккаунты, конфиги, сертификаты для dns challenge будут храниться там.

Путь к интерпретатору Python требуется, чтобы запускать бинарные файлы.

В TTL значение по-умолчанию установлено в 600. Это минимально допустимое значение.

**[WEBSERVER]**

| Function      | Description                                   | Default value             |
|---------------|-----------------------------------------------|---------------------------|
| ENABLED       | Флаг активации опции                          | false                     |
| TEST_CONFIG   | Команда тестирования конфигуарции веб-сервера | /usr/sbin/nginx -t        |
| RELOAD_CONFIG | Команда перезапуска веб-сервера               | /usr/sbin/nginx -s reload |

**[SMTP]**

| Function | Description                      | Default value |
|----------|----------------------------------|---------------|
| ENABLED  | Флаг активации опции             | false         |
| SERVER   | Адрес сервера                    | 127.0.0.1     |
| PORT     | Порт сервера                     | 25            |
| USERNAME | Логин                            | None          |
| PASSWORD | Пароль                           | None          |
| FROM     | Исходящий адрес почты            | None          |
| TO       | Реципиент (разделенные запятыми) | None          |

Если MTA без аутентификации, то оставьте пустыми значения USERNAME и PASSWORD.

**[POSTHOOK]**

| Function | Description                  | Default value |
|----------|------------------------------|---------------|
| ENABLED  | Флаг активации опции         | false         |
| SCRIPT   | Путь до исполняемого скрипта | None          |

POSTHOOK позволяет в конце запустить ваш скрипт. Может пригодится, если например захотите синхронизировать сертификаты на другие сервера.

## Сборка
Перед сборкой убедитесь, что в compile.py в строке shebang указан верный путь к интерпретатору (обычно должен совпадать с значением PYTHON в config.ini). Далее можно запустить ./compile.py.

## Конфиденциальность
Если это даже ключи от API все равно по возможности надо их скрыть (все таки DNS может сильно покосить процессы организации). Отсюда и компиляция Python скриптов в бинарники, чтобы нельзя было модифицировать просто так и основное приложение на Golang, чтобы скрыть учетные данные и также защитить от модификации.

## Тест
Тестовый запуск:
```
./main -v -t
```

## Очистка TXT
Godaddy API по-умолчанию удаляет все найденные (попадающие под критерий поиска) записи. Так что можно не беспокоиться, что где-то останется лишняя запись _acme-challenge.

## Cron
```
#m      #h      #dom    #mon    #dow    #command
0 	0 	1 	* 	* 	/path/to/letsencrypt-godaddy/main
```