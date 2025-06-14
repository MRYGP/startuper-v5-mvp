cat > config.py << 'EOF'
"""
认知黑匣子配置文件
"""
import os
from pathlib import Path

# 基础配置
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
DEMO_CASES_DIR = BASE_DIR / "demo_cases"
PROMPTS_DIR = BASE_DIR / "prompts"

# OpenAI配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4"
OPENAI_MAX_TOKENS = 2000
OPENAI_TEMPERATURE = 0.7

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
EOF
