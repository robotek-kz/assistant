# App

Для запуска приложения используйте следующие команды:

1. Активация виртуальной среды

```cmd

virtualenv venv
source venv\bin\activate # unix
export FLASK_APP=assistant.py

```

2. Подготовка базы данных

```cmd

flask db init
flask db migrate
flask db upgrade

```

3. Создайте папку `uploads` внутри папки `app`

4. Запустите приложение

```cmd

flask run # local
flask run --host=0.0.0.0 # wifi

```

# Front

Используйте v12.22.9 node. Вы можете установить её с помощью nvm. [https://github.com/nvm-sh/nvm]


1. Команда запуска клиента.

```cmd

nvm use 12
npm install
npm run serve

```

# Презентация приложения