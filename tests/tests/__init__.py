# tests/__init__.py
"""
认知黑匣子测试套件
包含Kevin案例专项测试、诊断准确性测试和用户体验测试
"""

from .test_kevin_case import TestKevinCase, run_kevin_tests
from .test_diagnosis_accuracy import TestDiagnosisAccuracy, run_diagnosis_accuracy_tests
from .test_user_experience import TestUserExperience, run_user_experience_tests

__all__ = [
    'TestKevinCase',
    'TestDiagnosisAccuracy', 
    'TestUserExperience',
    'run_kevin_tests',
    'run_diagnosis_accuracy_tests',
    'run_user_experience_tests'
]

# ===== run_all_tests.py =====
#!/usr/bin/env python3
"""
综合测试运行器 - 运行所有测试套件
"""

import sys
import os
from pathlib import Path
import unittest
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入所有测试模块
from tests.test_kevin_case import run_kevin_tests
from tests.test_diagnosis_accuracy import run_diagnosis_accuracy_tests
from tests.test_user_experience import run_user_experience_tests

def print_test_header():
    """打印测试开始信息"""
    print("🧠 认知黑匣子 - 完整测试套件")
    print("=" * 80)
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python版本: {sys.version}")
    print(f"📂 项目路径: {project_root}")
    print("=" * 80)

def print_test_summary(results):
    """打印测试总结"""
    print("\n" + "=" * 80)
    print("📊 测试总结报告")
    print("=" * 80)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print(f"📈 总测试套件数: {total_tests}")
    print(f"✅ 通过测试套件: {passed_tests}")
    print(f"❌ 失败测试套件: {failed_tests}")
    
    print("\n📋 详细结果:")
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        priority = "🔥 CRITICAL" if test_name == "Kevin案例测试" else "🎯 重要"
        print(f"  {status} {test_name} ({priority})")
    
    if all(results.values()):
        print("\n🎉🎉🎉 所有测试通过！产品已具备商业化条件！🎉🎉🎉")
        print("✨ 核心功能验证: Kevin案例处理完美")
        print("✨ 系统质量验证: 诊断准确性达标")  
        print("✨ 用户体验验证: 界面交互友好")
        print("🚀 Ready for Prime Time!")
    else:
        print("\n⚠️⚠️⚠️ 存在测试失败，需要立即修复！⚠️⚠️⚠️")
        if not results.get("Kevin案例测试", True):
            print("🚨 CRITICAL: Kevin案例测试失败直接影响产品核心价值！")
        print("🔧 请根据上述测试结果进行针对性修复")

def run_quick_tests():
    """运行快速测试（仅Kevin案例）"""
    print("⚡ 快速测试模式 - 仅Kevin案例核心验证")
    print("-" * 50)
    
    kevin_result = run_kevin_tests()
    
    if kevin_result:
        print("\n✅ 快速测试通过！核心功能正常")
        return True
    else:
        print("\n❌ 快速测试失败！需要修复Kevin案例问题")
        return False

def run_comprehensive_tests():
    """运行综合测试（所有测试套件）"""
    print("🎯 综合测试模式 - 完整质量验证")
    print("-" * 50)
    
    results = {}
    
    # 1. Kevin案例专项测试（最高优先级）
    print("\n🔥 第一阶段：Kevin案例专项测试（产品价值试金石）")
    print("-" * 50)
    results["Kevin案例测试"] = run_kevin_tests()
    
    # 如果Kevin案例测试失败，询问是否继续
    if not results["Kevin案例测试"]:
        print("\n⚠️ Kevin案例测试失败！")
        continue_test = input("是否继续其他测试？(y/N): ").lower().strip()
        if continue_test != 'y':
            print("测试中止。请先修复Kevin案例问题。")
            return results
    
    # 2. 诊断准确性测试
    print("\n🎯 第二阶段：诊断准确性测试（系统质量验证）")
    print("-" * 50)
    results["诊断准确性测试"] = run_diagnosis_accuracy_tests()
    
    # 3. 用户体验测试
    print("\n🎨 第三阶段：用户体验测试（产品易用性验证）")
    print("-" * 50)
    results["用户体验测试"] = run_user_experience_tests()
    
    return results

def main():
    """主测试函数"""
    print_test_header()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        print("请选择测试模式:")
        print("1. quick  - 快速测试（仅Kevin案例）")
        print("2. full   - 完整测试（所有测试套件）")
        choice = input("\n请输入选择 (1/2): ").strip()
        mode = "quick" if choice == "1" else "full"
    
    if mode == "quick":
        success = run_quick_tests()
        exit_code = 0 if success else 1
    else:
        results = run_comprehensive_tests()
        print_test_summary(results)
        
        # 确定退出码
        if all(results.values()):
            exit_code = 0
        elif results.get("Kevin案例测试", False):
            exit_code = 1  # Kevin通过但其他失败
        else:
            exit_code = 2  # Kevin失败（最严重）
    
    print(f"\n🏁 测试完成，退出码: {exit_code}")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()

# ===== pytest_config.py =====
"""
Pytest配置文件（如果使用pytest的话）
"""

import pytest
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(scope="session")
def diagnosis_engine():
    """诊断引擎fixture"""
    from utils.diagnosis_engine import DiagnosisEngine
    return DiagnosisEngine()

@pytest.fixture(scope="session") 
def demo_manager():
    """Demo案例管理器fixture"""
    from utils.demo_case_manager import DemoCaseManager
    return DemoCaseManager()

@pytest.fixture(scope="session")
def prescription_loader():
    """药方加载器fixture"""
    from utils.prescription_loader import PrescriptionLoader
    return PrescriptionLoader()

# Pytest配置
def pytest_configure(config):
    """Pytest配置"""
    config.addinivalue_line(
        "markers", "kevin: Kevin案例专项测试"
    )
    config.addinivalue_line(
        "markers", "accuracy: 诊断准确性测试"
    )
    config.addinivalue_line(
        "markers", "ux: 用户体验测试"
    )

def pytest_collection_modifyitems(config, items):
    """修改测试项目收集"""
    # 为Kevin案例测试添加最高优先级标记
    for item in items:
        if "kevin" in item.nodeid.lower():
            item.add_marker(pytest.mark.kevin)
        elif "accuracy" in item.nodeid.lower():
            item.add_marker(pytest.mark.accuracy)
        elif "experience" in item.nodeid.lower():
            item.add_marker(pytest.mark.ux)

# ===== Makefile 风格的测试命令 =====
"""
可以创建一个简单的测试脚本 test.sh:

#!/bin/bash
# 测试脚本

case "$1" in
    "kevin")
        echo "🔥 运行Kevin案例专项测试"
        python -m tests.test_kevin_case
        ;;
    "accuracy") 
        echo "🎯 运行诊断准确性测试"
        python -m tests.test_diagnosis_accuracy
        ;;
    "ux")
        echo "🎨 运行用户体验测试"  
        python -m tests.test_user_experience
        ;;
    "all"|"")
        echo "🧠 运行所有测试"
        python tests/run_all_tests.py full
        ;;
    "quick")
        echo "⚡ 运行快速测试"
        python tests/run_all_tests.py quick
        ;;
    *)
        echo "用法: $0 {kevin|accuracy|ux|all|quick}"
        exit 1
        ;;
esac
"""
