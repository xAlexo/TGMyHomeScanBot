# Repository guidance

- This Telegram bot requests scans through SANE (`scanimage`) and uses Telethon. `run.py` starts the client via `main.factory`; scan behavior is under `use_cases/` and command handlers under `commands/`.
- The authoritative Docker Compose definition is `compose.yaml`. It requires Telegram configuration, scanner selection, and an allowlist of user IDs. The image also configures SANE and discovery services. The legacy systemd deployment is described in `README.md` and `tg_my_home_scan_bot.service`.
- Dependencies are split between `requirements/production.txt` and `requirements/test.txt`. CI installs test requirements, runs the configured flake8 error subset and `pytest tests/`, and checks the Docker image. Do not run these locally because tests/build paths may execute project code; never start the bot or scanner integration.
- Preserve the `ALLOW_IDS` access restriction, scanner selection behavior, and host networking needed for scanner discovery. Dokploy variables supply runtime configuration. The Dokploy deploy command must use `--pull always` because Compose references `:latest`. The Telethon session is stored in `/app/bot_data`; keep that directory mounted persistently.
- Treat Telegram credentials, IDs, `.env`, session files, and scanner output as sensitive. `.env` is ignored; use `.env.example` as a template and never commit live configuration.
