# Repository guidance

- This Telegram bot requests scans through SANE (`scanimage`) and uses Telethon. `run.py` starts the client via `main.factory`; scan behavior is under `use_cases/` and command handlers under `commands/`.
- The Docker setup is documented in `README-Docker.md`; it requires Telegram configuration, scanner selection, and an allowlist of user IDs. The image also configures SANE and discovery services. The legacy systemd deployment is described in `README.md` and `tg_my_home_scan_bot.service`.
- Dependencies are split between `requirements/production.txt` and `requirements/test.txt`. CI installs test requirements, runs the configured flake8 error subset and `pytest tests/`, and builds/checks the Docker image. Do not run these here because tests/build paths may execute project code; never start the bot or scanner integration.
- Preserve the `ALLOW_IDS` access restriction and scanner selection behavior. Treat Telegram credentials, IDs, and session files as sensitive; don't commit configuration or scanner output.
