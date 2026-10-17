# TGMyHomeScanBot — Docker и Dokploy

Основное Compose-описание — [`compose.yaml`](compose.yaml). Оно использует сеть хоста для поиска SANE-сканера и хранит Telethon-сессию и временные файлы в `/srv/docker/tg_my_home_scan/`.

## Локальный запуск

Скопируйте `.env.example` в `.env`, укажите Telegram credentials, сканер и разрешённые Telegram ID, затем выполните:

```bash
docker compose up -d
```

`.env` исключён из Git. Не коммитьте credentials, разрешённые ID или файлы сессии.

## Dokploy

Создайте Compose-приложение из этого репозитория. Передайте `TG_APP_ID`, `TG_API_HASH`, `TG_BOT_API_TOKEN`, `SCANNER` и `ALLOW_IDS` как переменные приложения. `TG_APP_TITLE` необязателен, по умолчанию используется `MyHomeScan`. На хосте должны существовать каталоги `/srv/docker/tg_my_home_scan/bot_data` и `/srv/docker/tg_my_home_scan/tmp`. Для поиска сканера приложению нужна сеть хоста. В настройке Dokploy проверьте, что сгенерированная команда deploy использует `--pull always`, чтобы `:latest` обновлялся перед перезапуском.

GitHub Actions выполняет CI и публикацию образа на hosted runners. Новый semantic release публикует `ghcr.io/xalexo/tgmyhomescanbot:<version>` и `:latest`, затем запускает deploy Dokploy на выделенном runner с label `tg-my-home-scan`. Настройте переменные репозитория `DOKPLOY_URL`, `DOKPLOY_COMPOSE_ID` и secret `DOKPLOY_API_KEY`.

## Переменные конфигурации

| Переменная | Описание | Обязательная |
|---|---|---|
| `TG_APP_ID` | Telegram API ID | Да |
| `TG_API_HASH` | Telegram API hash | Да |
| `TG_BOT_API_TOKEN` | Токен бота | Да |
| `TG_APP_TITLE` | Имя Telethon-сессии | Нет |
| `SCANNER` | Устройство SANE | Да |
| `ALLOW_IDS` | Разрешённые Telegram ID через запятую | Да |
