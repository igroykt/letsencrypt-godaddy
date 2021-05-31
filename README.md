![GitHub Workflow Status](https://img.shields.io/github/workflow/status/igroykt/letsencrypt-godaddy/letsencrypt-godaddy%20build)
![GitHub](https://img.shields.io/github/license/igroykt/letsencrypt-godaddy)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/igroykt/letsencrypt-godaddy)

# LetsEncrypt GoDaddy
Приложение для выписки wildcard сертификатов посредством DNS challenge для Linux

## Зависимости
* Python 3.8
* Golang 1.16
* Certbot

## Unix
### Сборка и установка 
```
# установить certbot
# установить golang
go get gopkg.in/ini.v1
go env -w GO111MODULE=auto
pip3 install -r requirements.txt
mv config.sample.ini config.ini
# подправить config.ini и main.go
python setup.py build
mkdir /root/bin/letsencrypt-godaddy
mv build/* /root/bin/letsencrypt-godaddy
cp config.ini /root/bin/letsencrypt-godaddy
```

### Настройка
Про генерацию APIKEY и APISECRET читайте тут https://developer.godaddy.com/getstarted. Если сайт отображается некорректно, то попробуйте поменять язык браузера на английский (обычно помогает).

APIKEY и APISECRET прописать в main.go в "Configuration section".

**[GENERAL]**

| Function      | Description                                                            | Default value                    |
|---------------|------------------------------------------------------------------------|----------------------------------|
| ZONE          | Список доменных зон (разделенных запятыми)                             | None                             |
| ADMIN_EMAIL   | E-mail администратора certbot                                          | None                             |
| TTL           | Время жизни TXT записей                                                | 600                              |
| SLEEP         | Время ожидания пока TXT запись подхватится публичными DNS серверами    | 60                               |
| RETRIES       | Количество попыток при проверке TXT записи                             | 3                                |
| OS_SHELL      | Shell операционной системы                                             | /bin/bash                        |
| LE_CONFIG_DIR | Путь к директории для хранения конфигураций и сертификатов LetsEncrypt | /etc/letsencrypt                 |
| CERTBOT       | Путь к certbot                                                         | /usr/local/bin/certbot           |
| LE_LOG        | Путь к логу certbot                                                    | /var/log/letsencrypt/letsencrypt |

LE_CONFIG_DIR полезен в том случае, когда для некоторых ресурсов надо выписывать сертификаты по http challenge, а некоторые по dns challenge. В таком случае для dns challenge можно указать путь скажем /etc/letsencrypt-dns, тогда будет создана эта директория и аккаунты, конфиги, сертификаты для dns challenge будут храниться там.

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

### Конфиденциальность
Если это даже ключи от API все равно по возможности надо их скрыть (все таки DNS может сильно покосить процессы организации). Отсюда и компиляция Python скриптов в бинарники, чтобы нельзя было модифицировать просто так и основное приложение на Golang, чтобы скрыть учетные данные и также защитить от модификации.

### Тест
Тестовый запуск:
```
./main -v -t
```

### Очистка TXT
Godaddy API по-умолчанию удаляет все найденные (попадающие под критерий поиска) записи. Так что можно не беспокоиться, что где-то останется лишняя запись _acme-challenge.

### Cron
```
#m      #h      #dom    #mon    #dow    #command
0 	0 	1 	* 	* 	/path/to/letsencrypt-godaddy/main
```

## Windows
### Сборка и установка 
```
# установить certbot
# установить golang
go get gopkg.in/ini.v1
go env -w GO111MODULE=auto
pip install -r requirements.txt
move config.sample.ini config.ini
# подправить config.ini и main.go
python setup.py build
mkdir c:\godaddy
move build\* c:\godaddy
copy config.ini c:\godaddy
# в системную переменную Path добавить путь c:\godaddy
```

### Настройка
Certbot for windows: [https://dl.eff.org/certbot-beta-installer-win32.exe](https://dl.eff.org/certbot-beta-installer-win32.exe)

Пример настройки на Windows:

**[GENERAL]**

| Function      | Description                                                            | Value                                   |
|---------------|------------------------------------------------------------------------|-----------------------------------------|
| ZONE          | Список доменных зон (разделенных запятыми)                             | None                                    |
| ADMIN_EMAIL   | E-mail администратора certbot                                          | None                                    |
| TTL           | Время жизни TXT записей                                                | 600                                     |
| SLEEP         | Время ожидания пока TXT запись подхватится публичными DNS серверами    | 30                                      |
| RETRIES       | Количество попыток при проверке TXT записи                             | 3                                       |
| OS_SHELL      | Shell операционной системы                                             | cmd                                     |
| LE_CONFIG_DIR | Путь к директории для хранения конфигураций и сертификатов LetsEncrypt | c:\\\\letsencrypt                       |
| CERTBOT       | Путь к certbot                                                         | c:\\\\certbot\\\\bin\\\\certbot.exe     |
| LE_LOG        | Путь к логу certbot                                                    | c:\\\\certbot\\\\log\\\\letsencrypt.log |

**[WEBSERVER]**

| Function      | Description                                   | Default value                          |
|---------------|-----------------------------------------------|----------------------------------------|
| ENABLED       | Флаг активации опции                          | false                                  |
| TEST_CONFIG   | Команда тестирования конфигуарции веб-сервера | c:\\\\nginx\\\\sbin\\\\nginx -t        |
| RELOAD_CONFIG | Команда перезапуска веб-сервера               | c:\\\\nginx\\\\sbin\\\\nginx -s reload |

## Прекомпилированные бинарники
Добавлены прекомпилированные бинарники для auth и clean на всякий случай. Основное приложение main придется собирать вручную командой "go build" или "go build -tags win" на windows.