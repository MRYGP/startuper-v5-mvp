#!/bin/bash

# 🚀 认知黑匣子15分钟觉醒之旅 - 一键部署脚本
# 自动化部署和测试流程

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

print_info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 命令未找到，请先安装"
        return 1
    fi
    return 0
}

# 检查环境变量
check_env_var() {
    if [ -z "${!1}" ]; then
        print_error "环境变量 $1 未设置"
        return 1
    fi
    print_info "$1 已设置: ${!1:0:20}..."
    return 0
}

# 主函数
main() {
    print_message "🧠 开始部署认知黑匣子15分钟觉醒之旅"
    echo "=============================================="
    
    # 步骤1: 环境检查
    print_message "📋 步骤1: 环境检查"
    
    # 检查必要命令
    print_info "检查必要命令..."
    check_command "python3" || exit 1
    check_command "pip" || exit 1
    check_command "git" || exit 1
    
    # 检查Python版本
    python_version=$(python3 --version | cut -d' ' -f2)
    print_info "Python版本: $python_version"
    
    # 检查环境变量
    print_info "检查环境变量..."
    if [ -f ".env" ]; then
        print_info "发现 .env 文件，加载环境变量..."
        export $(cat .env | grep -v '^#' | xargs)
    fi
    
    check_env_var "GOOGLE_API_KEY" || {
        print_error "请设置 GOOGLE_API_KEY 环境变量"
        print_info "可以创建 .env 文件或直接设置: export GOOGLE_API_KEY=your_key"
        exit 1
    }
    
    print_message "✅ 环境检查完成"
    
    # 步骤2: 依赖安装
    print_message "📦 步骤2: 安装依赖"
    
    if [ -f "requirements.txt" ]; then
        print_info "安装Python依赖..."
        pip install -r requirements.txt
        
        # 尝试安装可选依赖
        print_info "尝试安装可选依赖..."
        pip install streamlit-mermaid || print_warning "streamlit-mermaid 安装失败，将使用降级模式"
    else
        print_warning "requirements.txt 未找到，跳过依赖安装"
    fi
    
    print_message "✅ 依赖安装完成"
    
    # 步骤3: 文件检查
    print_message "📁 步骤3: 文件完整性检查"
    
    # 检查关键文件
    required_files=(
        "app.py"
        "config.py"
        "utils/journey_orchestrator.py"
        "utils/journey_components.py"
        "utils/diagnosis_engine.py"
        "utils/streamlit_components.py"
    )
    
    missing_files=()
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            print_info "✅ $file"
        else
            print_error "❌ $file 缺失"
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -ne 0 ]; then
        print_error "缺少关键文件，无法继续部署"
        for file in "${missing_files[@]}"; do
            print_error "  - $file"
        done
        exit 1
    fi
    
    # 检查提示词文件
    print_info "检查提示词文件..."
    if [ -d "prompts" ]; then
        prompt_count=$(find prompts -name "*.md" | wc -l)
        print_info "发现 $prompt_count 个提示词文件"
        
        # 检查关键提示词
        key_prompts=("P-H-02-v1.0.md" "P-I-01-v1.0.md" "P-M-01-v1.0.md" "P-A-03-v1.0.md")
        for prompt in "${key_prompts[@]}"; do
            if [ -f "prompts/$prompt" ]; then
                print_info "✅ prompts/$prompt"
            else
                print_warning "⚠️ prompts/$prompt 缺失"
            fi
        done
    else
        print_warning "prompts 目录不存在"
    fi
    
    # 检查Demo案例
    print_info "检查Demo案例..."
    if [ -f "demo_cases/case_02_team_conflict.json" ]; then
        print_info "✅ Kevin案例文件存在"
    else
        print_warning "⚠️ Kevin案例文件缺失，将使用默认数据"
    fi
    
    print_message "✅ 文件检查完成"
    
    # 步骤4: 功能测试
    print_message "🧪 步骤4: 功能测试"
    
    if [ -f "test_kevin_journey.py" ]; then
        print_info "运行Kevin案例测试..."
        if python3 test_kevin_journey.py; then
            print_message "✅ Kevin案例测试通过"
        else
            print_error "❌ Kevin案例测试失败"
            print_info "继续部署，但建议检查配置"
        fi
    else
        print_warning "测试脚本不存在，跳过功能测试"
    fi
    
    # 步骤5: 启动应用
    print_message "🚀 步骤5: 启动应用"
    
    print_info "准备启动Streamlit应用..."
    print_info "应用将在 http://localhost:8501 运行"
    print_info ""
    print_info "🎯 测试建议:"
    print_info "1. 访问 http://localhost:8501"
    print_info "2. 点击'15分钟觉醒之旅'"
    print_info "3. 体验Kevin案例的完整流程"
    print_info "4. 验证四个AI角色切换正常"
    print_info "5. 确认武器卡片生成成功"
    print_info ""
    
    read -p "按Enter启动应用 (Ctrl+C 取消): "
    
    # 启动Streamlit
    print_message "🎭 启动15分钟认知觉醒之旅..."
    streamlit run app.py --server.port 8501 --server.address localhost
}

# 清理函数
cleanup() {
    print_message "🧹 清理临时文件..."
    # 这里可以添加清理逻辑
}

# 错误处理
error_handler() {
    print_error "部署过程中发生错误"
    cleanup
    exit 1
}

# 设置错误处理
trap error_handler ERR
trap cleanup EXIT

# 检查是否在正确的目录
if [ ! -f "app.py" ]; then
    print_error "请在项目根目录运行此脚本"
    exit 1
fi

# 运行主函数
main "$@"
