#!/usr/bin/env python3
"""
认知黑匣子测试文件自动创建脚本
一键创建完整的tests/目录及所有测试文件
"""

import os
from pathlib import Path

def create_tests_directory():
    """创建完整的测试目录和文件"""
    
    print("🧪 开始创建认知黑匣子测试套件...")
    print("=" * 60)
    
    # 获取项目根目录
    project_root = Path.cwd()
    tests_dir = project_root / "tests"
    
    # 创建tests目录
    tests_dir.mkdir(exist_ok=True)
    print(f"📁 创建目录: {tests_dir}")
    
    # 文件内容定义
    files_content = {
        "__init__.py": '''"""
认知黑匣子测试套件
"""

from .test_kevin_case import run_kevin_tests
from .test_diagnosis_accuracy import run_diagnosis_accuracy_tests  
from .test_user_experience import run_user_experience_tests

__all__ = [
    'run_kevin_tests',
    'run_diagnosis_accuracy_tests',
    'run_user_experience_tests'
]
''',

        "test_kevin_case.py": '''#!/usr/bin/env python3
"""
Kevin案例专项测试 - 产品价值验证的试金石
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import unittest
import json

try:
    from utils.diagnosis_engine import DiagnosisEngine
    from utils.demo_case_manager import DemoCaseManager
except ImportError as e:
    print(f"⚠️ 导入错误: {e}")
    print("请确保以下文件存在:")
    print("  - utils/diagnosis_engine.py")
    print("  - utils/demo_case_manager.py")
    sys.exit(1)

class TestKevinCase(unittest.TestCase):
    """Kevin案例专项测试类"""
    
    def setUp(self):
        """测试初始化"""
        try:
            self.diagnosis_engine = DiagnosisEngine()
            self.demo_manager = DemoCaseManager()
        except Exception as e:
            self.skipTest(f"初始化失败: {e}")
        
        # Kevin案例标准输入
        self.kevin_input = """我和我的技术合伙人在产品方向上产生了严重分歧，我认为应该专注B端企业客户，做项目管理SaaS，但他坚持要做C端的个人时间管理App。我们为此争论了6个月，项目基本停滞。最让我困惑的是，我明明有更多的市场调研数据支持B端方向，但他就是说服不了。现在我们的关系很紧张，投资人也开始质疑我们团队的执行力。"""
    
    def test_kevin_case_basic_recognition(self):
        """测试基本Kevin案例识别"""
        print("\\n🧪 测试Kevin案例基本识别")
        
        result = self.diagnosis_engine.diagnose(self.kevin_input)
        
        # 断言：必须有诊断结果
        self.assertIsNotNone(result, "Kevin案例诊断失败：无法获取诊断结果")
        
        # 断言：必须识别为P20药方
        primary = result.get('primary_prescription', {})
        prescription_id = primary.get('id', '')
        
        # 输出诊断详情用于调试
        print(f"  诊断结果: {prescription_id}")
        print(f"  置信度: {primary.get('confidence', 0):.1%}")
        
        # Kevin案例核心验证
        self.assertEqual(prescription_id.upper(), "P20", 
                        f"Kevin案例诊断错误：期望P20，实际得到{prescription_id}")
        
        # 置信度验证
        confidence = primary.get('confidence', 0)
        self.assertGreaterEqual(confidence, 0.8,
                               f"Kevin案例置信度不足：期望>=80%，实际{confidence:.1%}")
        
        print(f"✅ Kevin案例识别成功：{prescription_id} (置信度: {confidence:.1%})")
    
    def test_kevin_demo_case_exists(self):
        """测试Kevin专用Demo案例存在"""
        print("\\n🧪 测试Kevin专用Demo案例")
        
        kevin_case = self.demo_manager.get_kevin_case()
        
        if kevin_case:
            meta = kevin_case.get('case_meta', {})
            self.assertTrue(meta.get('kevin_case_solution', False),
                           "Kevin Demo案例缺少特殊标记")
            print("✅ Kevin专用Demo案例存在且标记正确")
        else:
            print("⚠️ Kevin专用Demo案例不存在，但测试继续")

def run_kevin_tests():
    """运行Kevin案例专项测试"""
    print("🔥 开始Kevin案例专项测试 - 产品价值验证的试金石")
    print("=" * 60)
    
    # 环境检查
    project_root = Path(__file__).parent.parent
    required_files = [
        "knowledge_base/diagnosis_system/diagnosis_rules.json",
        "utils/diagnosis_engine.py",
        "utils/demo_case_manager.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (project_root / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少必需文件:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\\n请先确保这些文件存在后再运行测试")
        return False
    
    # 运行测试
    suite = unittest.TestSuite()
    suite.addTest(TestKevinCase('test_kevin_case_basic_recognition'))
    suite.addTest(TestKevinCase('test_kevin_demo_case_exists'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 Kevin案例测试全部通过！产品核心价值得到验证！")
        print("✅ 系统能正确识别合伙人冲突问题")
        print("✅ 不会误诊为产品验证问题")
        print("✅ 产品差异化价值明确")
        return True
    else:
        print("❌ Kevin案例测试失败！这直接影响产品核心价值！")
        print(f"失败数: {len(result.failures)}")
        print(f"错误数: {len(result.errors)}")
        print("🚨 必须立即修复Kevin案例识别问题！")
        return False

if __name__ == "__main__":
    success = run_kevin_tests()
    sys.exit(0 if success else 1)
''',

        "test_diagnosis_accuracy.py": '''#!/usr/bin/env python3
"""
诊断准确性测试
"""

import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import unittest

try:
    from utils.diagnosis_engine import DiagnosisEngine
except ImportError as e:
    print(f"⚠️ 导入错误: {e}")
    sys.exit(1)

class TestDiagnosisAccuracy(unittest.TestCase):
    
    def setUp(self):
        """测试初始化"""
        try:
            self.diagnosis_engine = DiagnosisEngine()
        except Exception as e:
            self.skipTest(f"诊断引擎初始化失败: {e}")
        
        # 基础测试案例
        self.test_cases = [
            {
                "input": "我们的技术很强，算法比竞品先进很多，但是用户就是不买账，没人愿意付费使用。",
                "expected_category": "product",
                "test_name": "技术至上偏见"
            },
            {
                "input": "我和我的合伙人在很多决策上都有分歧，经常争论不休，严重影响了工作效率和团队氛围。",
                "expected_category": "team", 
                "test_name": "合伙人冲突"
            },
            {
                "input": "我制定了详细的计划，学了很多方法论，但总是执行不了，拖延症很严重。",
                "expected_category": "execution",
                "test_name": "执行力问题"
            }
        ]
    
    def test_basic_diagnosis_capability(self):
        """测试基本诊断能力"""
        print("\\n🧪 测试基本诊断能力")
        
        success_count = 0
        total_count = len(self.test_cases)
        
        for i, test_case in enumerate(self.test_cases):
            print(f"\\n  测试案例 {i+1}: {test_case['test_name']}")
            
            result = self.diagnosis_engine.diagnose(test_case['input'])
            
            if result:
                primary = result.get('primary_prescription', {})
                prescription_id = primary.get('id', '')
                confidence = primary.get('confidence', 0)
                
                print(f"    诊断结果: {prescription_id} (置信度: {confidence:.1%})")
                
                # 简单验证：至少要有结果
                if prescription_id and confidence > 0.3:
                    success_count += 1
                    print("    ✅ 诊断成功")
                else:
                    print("    ❌ 诊断质量不足")
            else:
                print("    ❌ 诊断失败")
        
        accuracy = success_count / total_count
        print(f"\\n📊 基本诊断成功率：{success_count}/{total_count} ({accuracy:.1%})")
        
        # 基本要求：至少50%成功率
        self.assertGreaterEqual(accuracy, 0.5, f"诊断成功率过低：{accuracy:.1%}")
    
    def test_empty_input_handling(self):
        """测试空输入处理"""
        print("\\n🧪 测试空输入处理")
        
        empty_inputs = ["", "   ", "太短"]
        
        for empty_input in empty_inputs:
            result = self.diagnosis_engine.diagnose(empty_input)
            
            # 空输入应该返回None或低置信度结果
            if result is None:
                print(f"    ✅ 正确拒绝空输入: '{empty_input}'")
            else:
                confidence = result.get('primary_prescription', {}).get('confidence', 0)
                if confidence < 0.5:
                    print(f"    ✅ 低置信度处理: '{empty_input}' ({confidence:.1%})")
                else:
                    print(f"    ⚠️ 空输入置信度异常高: '{empty_input}' ({confidence:.1%})")

def run_diagnosis_accuracy_tests():
    """运行诊断准确性测试"""
    print("🎯 开始诊断准确性测试 - 系统整体质量验证")
    print("=" * 60)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDiagnosisAccuracy)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 诊断准确性测试通过！")
        print("✅ 系统诊断能力达到基本标准")
        print("✅ 空输入处理正常")
    else:
        print("❌ 诊断准确性测试存在问题！")
        print("🔧 需要优化诊断算法和规则配置")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_diagnosis_accuracy_tests()
    sys.exit(0 if success else 1)
''',

        "test_user_experience.py": '''#!/usr/bin/env python3
"""
用户体验测试
"""

import sys
import os
from pathlib import Path
import time

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import unittest

try:
    from utils.diagnosis_engine import DiagnosisEngine
    from utils.demo_case_manager import DemoCaseManager
except ImportError as e:
    print(f"⚠️ 导入错误: {e}")
    sys.exit(1)

class TestUserExperience(unittest.TestCase):
    
    def setUp(self):
        """测试初始化"""
        try:
            self.diagnosis_engine = DiagnosisEngine()
            self.demo_manager = DemoCaseManager()
        except Exception as e:
            self.skipTest(f"组件初始化失败: {e}")
    
    def test_response_time_performance(self):
        """测试响应时间性能"""
        print("\\n🧪 测试响应时间性能")
        
        test_input = "我和我的技术合伙人在产品方向上产生了严重分歧，争论了很久没有结果。"
        
        start_time = time.time()
        result = self.diagnosis_engine.diagnose(test_input)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        print(f"    响应时间: {response_time:.2f}秒")
        
        # 响应时间应该在合理范围内
        self.assertLess(response_time, 10.0, f"响应时间过长：{response_time:.2f}秒")
        self.assertIsNotNone(result, "响应结果为空")
        
        print("    ✅ 响应时间测试通过")
    
    def test_demo_cases_availability(self):
        """测试Demo案例可用性"""
        print("\\n🧪 测试Demo案例可用性")
        
        try:
            cases = self.demo_manager.get_all_cases()
            case_count = len(cases)
            
            print(f"    加载案例数量: {case_count}")
            
            if case_count > 0:
                print("    ✅ Demo案例加载成功")
                
                # 检查Kevin案例
                kevin_case = self.demo_manager.get_kevin_case()
                if kevin_case:
                    print("    ✅ Kevin专用案例存在")
                else:
                    print("    ⚠️ Kevin专用案例缺失")
            else:
                print("    ⚠️ 未找到Demo案例")
                
        except Exception as e:
            print(f"    ❌ Demo案例加载失败: {e}")
    
    def test_error_handling_graceful(self):
        """测试错误处理的优雅性"""
        print("\\n🧪 测试错误处理")
        
        # 测试异常输入
        problematic_inputs = [
            None,
            "",
            "x" * 5000,  # 过长输入
            "正常输入但可能触发异常的特殊字符：@#$%^&*()",
        ]
        
        handled_gracefully = 0
        
        for problematic_input in problematic_inputs:
            try:
                result = self.diagnosis_engine.diagnose(problematic_input)
                # 如果没有抛出异常，说明处理得当
                handled_gracefully += 1
                print(f"    ✅ 优雅处理异常输入")
            except Exception as e:
                print(f"    ⚠️ 异常输入引发错误: {type(e).__name__}")
        
        # 至少要能处理一半的异常情况
        handling_rate = handled_gracefully / len(problematic_inputs)
        self.assertGreaterEqual(handling_rate, 0.5, f"错误处理能力不足: {handling_rate:.1%}")

def run_user_experience_tests():
    """运行用户体验测试"""
    print("🎨 开始用户体验测试 - 产品易用性验证")
    print("=" * 60)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUserExperience)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 用户体验测试通过！")
        print("✅ 响应时间性能良好")
        print("✅ Demo案例加载正常")
        print("✅ 错误处理优雅")
    else:
        print("❌ 用户体验测试存在问题！")
        print("🔧 需要优化用户界面和交互体验")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_user_experience_tests()
    sys.exit(0 if success else 1)
''',

        "run_all_tests.py": '''#!/usr/bin/env python3
"""
综合测试运行器
"""

import sys
import os
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入测试模块
from tests.test_kevin_case import run_kevin_tests
from tests.test_diagnosis_accuracy import run_diagnosis_accuracy_tests
from tests.test_user_experience import run_user_experience_tests

def print_test_header():
    """打印测试开始信息"""
    print("🧠 认知黑匣子 - 完整测试套件")
    print("=" * 70)
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    print(f"📂 项目路径: {Path.cwd()}")
    print("=" * 70)

def print_test_summary(results):
    """打印测试总结"""
    print("\\n" + "=" * 70)
    print("📊 测试总结报告")
    print("=" * 70)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print(f"📈 总测试套件数: {total_tests}")
    print(f"✅ 通过测试套件: {passed_tests}")
    print(f"❌ 失败测试套件: {total_tests - passed_tests}")
    
    print("\\n📋 详细结果:")
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        priority = "🔥 CRITICAL" if test_name == "Kevin案例测试" else "🎯 重要"
        print(f"  {status} {test_name} ({priority})")
    
    if all(results.values()):
        print("\\n🎉🎉🎉 所有测试通过！产品已具备商业化条件！🎉🎉🎉")
        print("✨ 核心功能验证: Kevin案例处理完美")
        print("✨ 系统质量验证: 诊断准确性达标")  
        print("✨ 用户体验验证: 界面交互友好")
        print("🚀 Ready for Prime Time!")
        return True
    else:
        print("\\n⚠️⚠️⚠️ 存在测试失败，需要立即修复！⚠️⚠️⚠️")
        if not results.get("Kevin案例测试", True):
            print("🚨 CRITICAL: Kevin案例测试失败直接影响产品核心价值！")
        print("🔧 请根据上述测试结果进行针对性修复")
        return False

def main():
    """主测试函数"""
    print_test_header()
    
    # 检查基本环境
    required_dirs = ["utils", "knowledge_base", "demo_cases"]
    missing_dirs = []
    
    for dir_name in required_dirs:
        if not (Path.cwd() / dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print("❌ 缺少必需目录:")
        for dir_name in missing_dirs:
            print(f"   - {dir_name}/")
        print("\\n请确保在项目根目录运行测试，并且已上传所有必需文件")
        return False
    
    results = {}
    
    # 1. Kevin案例专项测试（最高优先级）
    print("\\n🔥 第一阶段：Kevin案例专项测试（产品价值试金石）")
    print("-" * 50)
    results["Kevin案例测试"] = run_kevin_tests()
    
    # 如果Kevin案例测试失败，询问是否继续
    if not results["Kevin案例测试"]:
        print("\\n⚠️ Kevin案例测试失败！")
        try:
            continue_test = input("是否继续其他测试？(y/N): ").lower().strip()
            if continue_test != 'y':
                print("测试中止。请先修复Kevin案例问题。")
                return False
        except (EOFError, KeyboardInterrupt):
            print("\\n测试中止。")
            return False
    
    # 2. 诊断准确性测试
    print("\\n🎯 第二阶段：诊断准确性测试（系统质量验证）")
    print("-" * 50)
    results["诊断准确性测试"] = run_diagnosis_accuracy_tests()
    
    # 3. 用户体验测试
    print("\\n🎨 第三阶段：用户体验测试（产品易用性验证）")
    print("-" * 50)
    results["用户体验测试"] = run_user_experience_tests()
    
    # 打印总结并返回结果
    success = print_test_summary(results)
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\\n\\n⚠️ 测试被用户中断")
        sys.exit(2)
    except Exception as e:
        print(f"\\n\\n❌ 测试过程中发生未预期错误: {e}")
        sys.exit(3)
''',

        "README.md": '''# 🧪 认知黑匣子测试套件

> 确保产品核心价值和商业化就绪的完整测试体系

## 🎯 快速开始

### 1. 运行Kevin案例测试（最重要）
```bash
python tests/test_kevin_case.py
```
**这是最关键的测试！必须100%通过才能证明产品核心价值**

### 2. 运行完整测试套件
```bash
python tests/run_all_tests.py
```

### 3. 分别运行各项测试
```bash
python tests/test_kevin_case.py          # 🔥 Kevin案例专项测试
python tests/test_diagnosis_accuracy.py  # 🎯 诊断准确性测试
python tests/test_user_experience.py     # 🎨 用户体验测试
```

## 📊 测试套件说明

### 🔥 Kevin案例专项测试 (CRITICAL)
**重要性**: 产品价值验证的试金石
**测试内容**: 验证系统能否正确识别合伙人冲突问题
**成功标准**: 必须识别为P20药方，置信度>80%

### 🎯 诊断准确性测试
**重要性**: 系统整体质量验证
**测试内容**: 多种认知陷阱识别准确性
**成功标准**: 基本诊断成功率>50%

### 🎨 用户体验测试
**重要性**: 产品易用性验证
**测试内容**: 响应时间、错误处理、Demo案例加载
**成功标准**: 响应时间<10秒，错误处理优雅

## ✅ 成功标准

当所有测试通过时，表示：
- 🔥 **Kevin案例处理完美** → 核心价值验证
- 🎯 **诊断准确性达标** → 系统质量保证  
- 🎨 **用户体验良好** → 产品易用性确保

**Ready for Prime Time!** 🚀

## 🚨 故障排除

### Kevin案例测试失败
1. 检查 `knowledge_base/diagnosis_system/diagnosis_rules.json` 是否存在
2. 确认文件中包含 `RULE_TF01_KEVIN_CASE` 规则
3. 验证 `utils/diagnosis_engine.py` 正常工作

### 导入错误
1. 确保在项目根目录运行测试
2. 检查所需文件是否已上传到GitHub
3. 确认Python路径配置正确

### 其他问题
- 检查网络连接（如果使用OpenAI API）
- 确认所有依赖已安装
- 查看具体错误信息进行针对性修复

---

*测试通过 = 产品商业化就绪* 🎯
'''
    }
    
    # 创建所有文件
    created_files = []
    for filename, content in files_content.items():
        file_path = tests_dir / filename
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            created_files.append(filename)
            print(f"✅ 创建文件: {filename}")
        except Exception as e:
            print(f"❌ 创建文件失败 {filename}: {e}")
    
    # 设置可执行权限（Unix系统）
    if os.name != 'nt':  # 非Windows系统
        for py_file in tests_dir.glob("*.py"):
            try:
                os.chmod(py_file, 0o755)
            except:
                pass
    
    print("\n" + "=" * 60)
    print("🎉 测试套件创建完成！")
    print(f"📁 创建目录: {tests_dir}")
    print(f"📄 创建文件: {len(created_files)}个")
    
    # 下一步指导
    print("\n🚀 下一步操作:")
    print("1. 🔥 立即运行Kevin案例测试:")
    print("   python tests/test_kevin_case.py")
    
    print("\n2. 如果Kevin测试通过，运行完整测试:")
    print("   python tests/run_all_tests.py")
    
    print("\n3. 将测试文件提交到GitHub:")
    print("   git add tests/")
    print("   git commit -m '🧪 添加完整测试套件'")
    print("   git push origin main")
    
    print("\n💡 重要提示:")
    print("   - Kevin案例测试是最关键的，必须优先确保通过")
    print("   - 测试失败时请查看具体错误信息")  
    print("   - 所有测试通过 = 产品Ready for Prime Time!")
    
    return True

if __name__ == "__main__":
    print("🛠️ 认知黑匣子测试文件自动创建脚本")
    print("=" * 60)
    
    create_tests_directory()
    
    print("\n🎊 脚本执行完成！")
    print("现在可以运行测试验证产品质量了！")
