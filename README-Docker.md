# TGMyHomeScanBot - Docker Setup

## Запуск с Docker

### Быстрый старт

1. Клонируйте репозиторий:
```bash
git clone https://github.com/xAlexo/TGMyHomeScanBot.git
cd TGMyHomeScanBot
```

2. Создайте файл `.env` с настройками:
```bash
# Telegram API configuration
TG_APP_ID=YOUR_APP_ID_HERE
TG_API_HASH=YOUR_API_HASH_HERE
TG_BOT_API_TOKEN=YOUR_BOT_TOKEN_HERE
TG_APP_TITLE=MyHomeScan

# Scanner configuration
SCANNER=YOUR_SCANNER_DEVICE_HERE

# Access control
ALLOW_IDS=YOUR_USER_ID_1,YOUR_USER_ID_2
```

3. Запустите с Docker Compose:
```bash
docker-compose up -d
```

### Использование готового образа из GitHub Container Registry

```bash
# Последняя версия
docker pull ghcr.io/xalexo/tgmyhomescanbot:latest

# Или конкретная версия (если есть тэги)
docker pull ghcr.io/xalexo/tgmyhomescanbot:v1.0.0
```

### Сборка Docker образа локально

```bash
docker build -t tg-my-home-scan-bot .
```

### Запуск контейнера

```bash
docker run -d \
  --name tg-my-home-scan-bot \
  -e TG_APP_ID=YOUR_APP_ID \
  -e TG_API_HASH=YOUR_API_HASH \
  -e TG_BOT_API_TOKEN=YOUR_TOKEN \
  -e SCANNER=epson2:net:192.168.1.3 \
  -e ALLOW_IDS=123456789,987654321 \
  ghcr.io/xalexo/tgmyhomescanbot:latest
```

Или если вы собрали образ локально:
```bash
docker run -d \
  --name tg-my-home-scan-bot \
  -e TG_APP_ID=YOUR_APP_ID \
  -e TG_API_HASH=YOUR_API_HASH \
  -e TG_BOT_API_TOKEN=YOUR_TOKEN \
  -e SCANNER=epson2:net:192.168.1.3 \
  -e ALLOW_IDS=123456789,987654321 \
  tg-my-home-scan-bot
```

### Конфигурация сканера

Для сетевых сканеров:
```bash
SCANNER=epson2:net:192.168.1.3
```

Для USB сканеров (добавьте доступ к устройствам):
```bash
docker run -d \
  --device /dev/bus/usb:/dev/bus/usb \
  -e SCANNER=epson2:libusb:001:002 \
  ...
```

### Получение ID сканера

Для получения списка доступных сканеров:
```bash
docker run --rm --device /dev/bus/usb:/dev/bus/usb tg-my-home-scan-bot scanimage -L
```

### Логи

```bash
docker logs tg-my-home-scan-bot
```

### Остановка

```bash
docker-compose down
# или
docker stop tg-my-home-scan-bot
```

## Переменные окружения

| Переменная | Описание | Обязательная |
|------------|----------|--------------|
| `TG_APP_ID` | API ID от Telegram | Да |
| `TG_API_HASH` | API Hash от Telegram | Да |
| `TG_BOT_API_TOKEN` | Токен бота от @BotFather | Да |
| `TG_APP_TITLE` | Название приложения | Нет (по умолчанию: MyHomeScan) |
| `SCANNER` | Устройство сканера | Да |
| `ALLOW_IDS` | Разрешенные ID пользователей (через запятую) | Да |

## Особенности Docker версии

- Автоматически генерирует config.py из переменных окружения
- Включает все необходимые системные зависимости (SANE)
- Поддерживает как сетевые, так и USB сканеры
- Не требует установки Python зависимостей на хост-системе
- Изолированная среда выполнения

## GitHub Actions и автоматическая сборка

Репозиторий настроен с GitHub Actions для автоматической сборки и публикации Docker образов:

- **CI Workflow**: Автоматически тестирует код и проверяет сборку Docker образа при каждом push/PR
- **Docker Publish Workflow**: Автоматически собирает и публикует Docker образы в GitHub Container Registry при:
  - Push в ветку `main` (тэг `latest`)
  - Создании тэга версии `v*` (тэги версий)

### Использование опубликованных образов

```bash
# Последняя версия
docker pull ghcr.io/xalexo/tgmyhomescanbot:latest

# Конкретная версия (если есть релизы)
docker pull ghcr.io/xalexo/tgmyhomescanbot:v1.0.0
```

Образы автоматически обновляются при изменениях в коде и доступны в [GitHub Container Registry](https://github.com/xAlexo/TGMyHomeScanBot/pkgs/container/tgmyhomescanbot).