"""
认知黑匣子配置文件 - Gemini版本
"""
import os
from pathlib import Path

# 基础配置
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
DEMO_CASES_DIR = BASE_DIR / "demo_cases"
PROMPTS_DIR = BASE_DIR / "prompts"

# Google Gemini API配置
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_MAX_OUTPUT_TOKENS = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "2000"))
GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))

# Gemini 安全设置
GEMINI_SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

# Gemini 生成配置
GEMINI_GENERATION_CONFIG = {
    "temperature": GEMINI_TEMPERATURE,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": GEMINI_MAX_OUTPUT_TOKENS,
    "response_mime_type": "text/plain",
}

# 应用配置
APP_TITLE = "🧠 认知黑匣子"
APP_SUBTITLE = "15分钟认知觉醒，从'我是对的'到'我原来想错了'"
MAX_INPUT_LENGTH = 2000
MIN_INPUT_LENGTH = 50

# 诊断配置
DIAGNOSIS_CONFIDENCE_THRESHOLD = 0.6
MAX_PRESCRIPTIONS_PER_DIAGNOSIS = 3
KEVIN_CASE_BOOST_FACTOR = 1.5

# 路径配置
DIAGNOSIS_RULES_PATH = KNOWLEDGE_BASE_DIR / "diagnosis_system" / "diagnosis_rules.json"
CASES_INDEX_PATH = DEMO_CASES_DIR / "cases_index.json"

# UI配置
SIDEBAR_WIDTH = 300
MAIN_CONTENT_WIDTH = 800
CARD_BORDER_RADIUS = "10px"
CARD_SHADOW = "0 2px 4px rgba(0,0,0,0.1)"

# 缓存配置
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"

# 调试配置
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
VERBOSE_LOGGING = os.getenv("VERBOSE_LOGGING", "false").lower() == "true"

# 验证配置
def validate_config():
    """验证配置是否完整"""
    errors = []
    
    if not GOOGLE_API_KEY:
        errors.append("GOOGLE_API_KEY 未设置")
    elif not GOOGLE_API_KEY.startswith("AIza"):
        errors.append("GOOGLE_API_KEY 格式不正确，应该以 'AIza' 开头")
    
    if not GEMINI_MODEL:
        errors.append("GEMINI_MODEL 未设置")
    
    if not KNOWLEDGE_BASE_DIR.exists():
        errors.append(f"知识库目录不存在: {KNOWLEDGE_BASE_DIR}")
    
    if not DEMO_CASES_DIR.exists():
        errors.append(f"Demo案例目录不存在: {DEMO_CASES_DIR}")
    
    return errors

# 在导入时验证配置
if __name__ != "__main__":  # 避免在直接运行时验证
    config_errors = validate_config()
    if config_errors and not DEBUG:
        import warnings
        for error in config_errors:
            warnings.warn(f"配置警告: {error}")

# 支持的语言模型列表
SUPPORTED_MODELS = [
    "gemini-2.5-flash",
    "gemini-pro",
    "gemini-pro-vision"
]

# API限流配置
API_RATE_LIMIT = {
    "requests_per_minute": 60,
    "requests_per_hour": 1000,
    "requests_per_day": 1500
}

# 错误重试配置
RETRY_CONFIG = {
    "max_retries": 3,
    "retry_delay": 1,  # 秒
    "exponential_backoff": True
}
