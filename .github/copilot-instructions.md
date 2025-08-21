# TGMyHomeScanBot - GitHub Copilot Instructions

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

TGMyHomeScanBot is a Python Telegram bot that provides remote control of network and USB scanners via the SANE (Scanner Access Now Easy) library. The bot accepts scan commands through Telegram messages and returns scanned documents as files.

## Working Effectively

### Prerequisites and System Dependencies
- Install system dependencies first: `sudo apt-get update && sudo apt-get install -y sane-utils libsane1`
- Python 3.12+ is required and confirmed working
- Docker is optional but recommended for production deployment

### Bootstrap and Build Process
1. **Install Dependencies** (takes ~10 seconds total):
   ```bash
   pip install -r requirements/production.txt  # ~8 seconds
   pip install -r requirements/test.txt        # ~3 seconds  
   ```

2. **Create Configuration**:
   ```bash
   # Copy and edit with your actual values:
   cat > config.py << 'EOF'
   # Telegram API configuration (get from https://my.telegram.org)
   TG_APP_ID = 12345  # Your actual app ID
   TG_API_HASH = 'your_api_hash'
   TG_BOT_API_TOKEN = 'your_bot_token'  # From @BotFather
   TG_APP_TITLE = 'MyHomeScan'
   
   # Scanner configuration (use scanimage -L to find your scanner)
   SCANNER = 'epson2:net:192.168.1.3'  # Network scanner example
   # SCANNER = 'test:0'  # Use this for testing without physical scanner
   
   # Access control (Telegram user IDs allowed to use bot)
   ALLOW_IDS = frozenset([123456789, 987654321])
   EOF
   ```

### Testing
- **IMPORTANT**: Tests require config.py to exist (even with dummy values)
- Current pytest version has compatibility issues - tests can be validated by importing modules:
  ```bash
  python -c "from commands.default import default; print('Commands module OK')"
  python -c "from use_cases.scan import scan; print('Scan module OK')"
  python -c "from main import factory; print('Main module OK')"
  ```

### Running the Application

#### Native Python (Development)
```bash
python run.py  # Starts the bot (requires valid config.py)
```

#### Docker (Production - Recommended)
1. **Build Docker Image** - NEVER CANCEL: takes ~60 seconds:
   ```bash
   docker build -t tg-my-home-scan-bot . --timeout 120
   ```

2. **Run with Docker Compose**:
   ```bash
   # Edit docker-compose.yml environment variables first
   docker-compose up -d
   ```

3. **Run with Docker directly**:
   ```bash
   docker run -d \
     --name tg-my-home-scan-bot \
     -e TG_APP_ID=12345 \
     -e TG_API_HASH=your_hash \
     -e TG_BOT_API_TOKEN=your_token \
     -e SCANNER=epson2:net:192.168.1.3 \
     -e ALLOW_IDS=123456789,987654321 \
     tg-my-home-scan-bot
   ```

## Validation and Testing

### Scanner Functionality Validation
1. **Test scanner connectivity**:
   ```bash
   scanimage -L  # Lists available scanners
   ```

2. **Test scanning without bot** (validates scanner setup):
   ```bash
   # Test with real scanner:
   scanimage -d "epson2:net:192.168.1.3" --format png --output-file test.png --mode Color --resolution 150dpi
   
   # Test with test device (no physical scanner needed):
   scanimage -d "test:0" --format png --output-file test.png --mode Color --resolution 75dpi
   ```

3. **Verify scan files are created**: Check that PNG files are generated in expected location

### Application Validation Scenarios
1. **Module Import Test**:
   ```bash
   python -c "from main import factory; from commands.default import default; print('All core modules import successfully')"
   ```

2. **Bot Startup Test** (will fail auth with dummy config, but should start):
   ```bash
   timeout 5 python run.py || echo "Expected auth failure with test config"
   ```

3. **Docker Container Test**:
   ```bash
   # Start container and check logs
   docker run --rm -e TG_APP_ID=1 -e TG_API_HASH=test -e TG_BOT_API_TOKEN=test -e SCANNER=test:0 -e ALLOW_IDS=1 tg-my-home-scan-bot &
   sleep 3 && docker logs $(docker ps -q --filter ancestor=tg-my-home-scan-bot) && docker stop $(docker ps -q --filter ancestor=tg-my-home-scan-bot)
   ```

## Code Structure and Navigation

### Key Files and Directories
- **`run.py`** - Application entry point
- **`main.py`** - Telegram client factory and command registration
- **`commands/`** - Telegram command handlers
  - `commands/default.py` - Main scan command handler
  - `commands/start.py` - /start command handler
- **`use_cases/scan.py`** - Core scanning logic using scanimage
- **`contrib/`** - Utility modules
  - `contrib/scan_type.py` - Scan type enumeration (Gray/Color)
  - `contrib/default_buttons.py` - Telegram inline keyboard buttons
- **`tests/`** - Unit tests (pytest-based)
- **`requirements/`** - Python dependencies
  - `requirements/production.txt` - Runtime dependencies
  - `requirements/test.txt` - Testing dependencies
- **`config.py`** - Configuration file (gitignored, create manually)

### Common Development Patterns
- **Scanner Integration**: All scanner operations use the `scanimage` command via `use_cases/scan.py`
- **Telegram Handlers**: Commands are registered in `main.py` and implemented in `commands/`
- **Progress Reporting**: Scan progress is reported via Telegram message updates
- **File Management**: Scanned files are temporarily stored in `/tmp/` and sent as Telegram documents

## Important Notes and Gotchas

### Configuration Requirements
- **NEVER commit config.py** - contains sensitive API keys and tokens
- Use environment variables in Docker deployments (see docker-compose.yml)
- **Test scanner device**: Use `SCANNER = 'test:0'` for development without physical hardware

### Scanner-Specific Notes
- **Network scanners**: Use format like `epson2:net:192.168.1.3`
- **USB scanners**: May require additional Docker privileges (`--device /dev/bus/usb:/dev/bus/usb`)
- **Scanner discovery**: Always run `scanimage -L` to identify correct device strings

### Development Workflows
- **Configuration changes**: Always test both with test scanner and intended hardware
- **Docker changes**: Rebuild image after any code changes
- **Testing**: Validate modules import correctly before testing bot functionality

### Known Issues
- **pytest compatibility**: Current test setup has issues with Python 3.12 - validate manually with imports
- **Session files**: Bot creates session files that should not be committed (included in .gitignore)

## Timeline Expectations
- **Dependency installation**: ~10 seconds total
- **Docker build**: ~60 seconds (NEVER CANCEL)
- **Scanner test**: ~5 seconds for test device
- **App startup**: Immediate (fails gracefully with invalid credentials)

## CI/CD Considerations
Currently no CI/CD pipeline exists. If implementing:
- Ensure SANE utilities are installed in CI environment
- Use test scanner device for automated testing
- Mock Telegram API calls for unit tests
- Docker build should be validated but not deployed automatically due to credential requirements