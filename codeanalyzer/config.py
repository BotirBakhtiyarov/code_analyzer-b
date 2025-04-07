import os
import configparser


class Config:
    _config = configparser.ConfigParser()
    _config.read(os.path.expanduser("~/.code_analyzer/config.ini"))

    try:
        DEEPSEEK_API_KEY = _config.get("DEEPSEEK", "API_KEY")
    except (configparser.NoSectionError, configparser.NoOptionError):
        DEEPSEEK_API_KEY = None

    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    MAX_FILE_SIZE = 5000000  # 5MB
    SUPPORTED_EXTENSIONS = {
        '.py', '.js', '.java', '.c', '.cpp', '.h', '.hpp',
        '.html', '.css', '.php', '.rb', '.go', '.rs'
    }
    REQUEST_TIMEOUT = 30