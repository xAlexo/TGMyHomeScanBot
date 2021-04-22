Бот для сканирования на домашнем сканере в телеграм.
Бот работает на linux системах с установленной scanimage 

Установка
1. Получить API ID и API HASH
    1. Авторизайтесь в любом телеграм клиенте
    2. Войдите на сайте https://my.telegram.org. 
    3. Перейдите на 'API development tools' и заполните поля
    4. Получите api_id и api_hash
2. Создайте телеграм бота
    1. Найдите в телеграм бота @BotFather
    2. Введите команду /newbot, создайте бота следую инструкции
    3. Получите TOKEN 
3. Скачайте исходники в папку /srv/http/TGMyHomeScanBot/src
4. Создайте python venv
   

        cd /srv/http/TGMyHomeScanBot && python -m venv .

5. Установите зависимости
   

        /srv/http/TGMyHomeScanBot/bin/python -m pip install -r src/requirements.txt
   
6. Скопируйте tg_my_home_scan_bot.service в /etc/systemd/system

   
        cp /srv/http/TGMyHomeScanBot/src/tg_my_home_scan_bot.service /etc/systemd/system

7. Создайте фаил config

   
        # APP API ID полученный от телеграм
        TG_APP_ID = 000000 
        # APP API HASH полученный от телеграм
        TG_API_HASH = 'HASH'
        # Токен полученный от @BotFather
        TG_BOT_API_TOKEN = 'Токен'
        # Любая строка
        TG_APP_TITLE = 'MyHomeScan'
        # Поле device нужного принтера из ответа scanimage --list-devices
        SCANNER = 'epson2:net:192.168.1.3'
        # Список ID которым разрешён доступ к боту через запятую
        ALLOW_IDS = frozenset([1,2,3])

8. Запустите бота
   

        sudo systemctl start tg_my_home_scan_bot
