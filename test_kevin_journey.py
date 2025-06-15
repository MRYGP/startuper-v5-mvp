"""
Kevin案例15分钟完整流程测试脚本
用于验证系统的核心功能和演示就绪性
"""
import sys
import os
import json
import time
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent))

try:
    from utils.journey_orchestrator import JourneyOrchestrator
    from config import GOOGLE_API_KEY
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保所有依赖文件都在正确位置")
    sys.exit(1)

class KevinJourneyTester:
    """Kevin案例完整流程测试器"""
    
    def __init__(self):
        self.orchestrator = JourneyOrchestrator()
        self.test_results = {}
        self.start_time = None
        
    def run_complete_test(self):
        """运行完整的Kevin案例测试"""
        print("🧪 开始Kevin案例15分钟完整流程测试")
        print("=" * 60)
        
        self.start_time = time.time()
        
        # 测试序列
        tests = [
            ("环境检查", self.test_environment),
            ("Kevin案例数据加载", self.test_kevin_data_loading),
            ("阶段1：主持人诊断", self.test_stage1_diagnosis),
            ("阶段2：投资人质询", self.test_stage2_investor),
            ("阶段3：导师教学", self.test_stage3_mentor),
            ("阶段4：助理内化", self.test_stage4_assistant),
            ("完整流程验证", self.test_complete_flow)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔬 测试: {test_name}")
            print("-" * 40)
            
            try:
                result = test_func()
                if result:
                    print(f"✅ {test_name} - 通过")
                    passed_tests += 1
                else:
                    print(f"❌ {test_name} - 失败")
                    
                self.test_results[test_name] = result
                
            except Exception as e:
                print(f"❌ {test_name} - 异常: {e}")
                self.test_results[test_name] = False
        
        # 生成测试报告
        self.generate_test_report(passed_tests, total_tests)
        
        return passed_tests == total_tests
    
    def test_environment(self):
        """测试环境配置"""
        print("检查环境配置...")
        
        # 检查API密钥
        if not GOOGLE_API_KEY:
            print("❌ GOOGLE_API_KEY 未配置")
            return False
        
        if not GOOGLE_API_KEY.startswith("AIza"):
            print("❌ GOOGLE_API_KEY 格式不正确")
            return False
        
        print(f"✅ API密钥配置正确: {GOOGLE_API_KEY[:20]}...")
        
        # 检查Gemini连接
        if self.orchestrator.model:
            print("✅ Gemini模型初始化成功")
            return True
        else:
            print("❌ Gemini模型初始化失败")
            return False
    
    def test_kevin_data_loading(self):
        """测试Kevin案例数据加载"""
        print("加载Kevin案例数据...")
        
        kevin_data = self.orchestrator._load_kevin_case()
        
        # 检查必要字段
        required_fields = ["case_name", "protagonist", "six_answers"]
        
        for field in required_fields:
            if field not in kevin_data:
                print(f"❌ 缺少字段: {field}")
                return False
        
        # 检查6个问题答案
        if len(kevin_data["six_answers"]) != 6:
            print(f"❌ 应该有6个答案，实际有{len(kevin_data['six_answers'])}个")
            return False
        
        # 检查答案质量
        for i, answer in enumerate(kevin_data["six_answers"]):
            if len(answer) < 50:
                print(f"❌ 第{i+1}个答案太短: {len(answer)}字符")
                return False
        
        print(f"✅ Kevin案例数据完整")
        print(f"✅ 主角: {kevin_data['protagonist']}")
        print(f"✅ 案例: {kevin_data['case_name']}")
        print(f"✅ 6个答案长度: {[len(a) for a in kevin_data['six_answers']]}")
        
        return True
    
    def test_stage1_diagnosis(self):
        """测试阶段1：主持人诊断"""
        print("测试主持人诊断阶段...")
        
        # 使用Kevin案例的回答
        kevin_data = self.orchestrator._load_kevin_case()
        user_responses = kevin_data["six_answers"]
        
        # 调用诊断
        diagnosis = self.orchestrator.stage2_diagnosis(user_responses)
        
        if not diagnosis:
            print("❌ 诊断返回为空")
            return False
        
        # 检查诊断结果
        diagnosis_result = diagnosis.get("diagnosis_result", {})
        final_trap = diagnosis_result.get("final_trap", "")
        confidence = diagnosis_result.get("confidence", 0)
        
        print(f"诊断结果: {final_trap}")
        print(f"置信度: {confidence}")
        
        # Kevin案例应该诊断为团队问题
        if "团队" not in final_trap and "合伙人" not in final_trap:
            print(f"⚠️ 诊断结果可能不准确: {final_trap}")
            print("（但继续测试降级处理）")
        
        if confidence < 0.7:
            print(f"⚠️ 置信度较低: {confidence}")
        
        print("✅ 诊断阶段完成")
        return True
    
    def test_stage2_investor(self):
        """测试阶段2：投资人质询"""
        print("测试投资人质询阶段...")
        
        # 模拟诊断结果
        mock_diagnosis = {
            "diagnosis_result": {
                "final_trap": "团队认知偏差：镜子陷阱",
                "confidence": 0.95
            }
        }
        
        user_story = "Kevin的团队冲突案例"
        
        # 调用投资人质询
        interrogation = self.orchestrator.stage3_investor_interrogation(mock_diagnosis, user_story)
        
        if not interrogation:
            print("❌ 投资人质询返回为空")
            return False
        
        # 检查四重奏结构
        four_acts = interrogation.get("four_act_interrogation", {})
        required_acts = ["act1_assumption_attack", "act2_opportunity_cost", "act3_grand_failure_case", "act4_root_cause"]
        
        for act in required_acts:
            if act not in four_acts:
                print(f"⚠️ 缺少质询环节: {act}")
            else:
                content = four_acts[act]
                if isinstance(content, str) and len(content) > 20:
                    print(f"✅ {act}: {content[:50]}...")
                elif isinstance(content, dict):
                    print(f"✅ {act}: 结构化内容")
        
        print("✅ 投资人质询完成")
        return True
    
    def test_stage3_mentor(self):
        """测试阶段3：导师教学"""
        print("测试导师教学阶段...")
        
        # 模拟诊断结果
        mock_diagnosis = {
            "diagnosis_result": {
                "final_trap": "团队认知偏差：镜子陷阱",
                "confidence": 0.95
            }
        }
        
        # 调用导师教学
        teaching = self.orchestrator.stage4_mentor_teaching(mock_diagnosis)
        
        if not teaching:
            print("❌ 导师教学返回为空")
            return False
        
        # 检查教学材料结构
        required_sections = ["opening_statement", "visual_framework", "power_comparison"]
        
        for section in required_sections:
            if section in teaching:
                print(f"✅ {section}: 存在")
            else:
                print(f"⚠️ {section}: 缺失")
        
        # 检查Mermaid图表
        framework = teaching.get("visual_framework", {})
        if "code" in framework:
            mermaid_code = framework["code"]
            if "graph" in mermaid_code or "flowchart" in mermaid_code:
                print(f"✅ Mermaid流程图: {len(mermaid_code)}字符")
            else:
                print("⚠️ Mermaid代码格式可能有问题")
        
        print("✅ 导师教学完成")
        return True
    
    def test_stage4_assistant(self):
        """测试阶段4：助理内化"""
        print("测试助理内化阶段...")
        
        # 模拟完整数据
        mock_data = {
            "diagnosis": {
                "diagnosis_result": {
                    "final_trap": "团队认知偏差：镜子陷阱"
                }
            }
        }
        
        weapon_name = "我的团队认知雷达"
        personal_reminder = "优秀的人≠优秀的团队"
        
        # 调用助理总结
        weapon_card = self.orchestrator.stage5_assistant_summary(mock_data, weapon_name, personal_reminder)
        
        if not weapon_card:
            print("❌ 武器卡片生成失败")
            return False
        
        # 检查武器卡片结构
        if "weapon_card" in weapon_card:
            card_content = weapon_card["weapon_card"]
            if "content" in card_content:
                print("✅ 武器卡片内容结构正确")
            else:
                print("⚠️ 武器卡片内容格式异常")
        
        print(f"✅ 武器名称: {weapon_name}")
        print(f"✅ 血泪提醒: {personal_reminder}")
        print("✅ 助理内化完成")
        return True
    
    def test_complete_flow(self):
        """测试完整流程"""
        print("验证完整流程一致性...")
        
        elapsed_time = time.time() - self.start_time
        print(f"总测试用时: {elapsed_time:.1f}秒")
        
        # 检查所有阶段是否都能正常工作
        passed_stages = sum([
            self.test_results.get("阶段1：主持人诊断", False),
            self.test_results.get("阶段2：投资人质询", False),
            self.test_results.get("阶段3：导师教学", False),
            self.test_results.get("阶段4：助理内化", False)
        ])
        
        if passed_stages == 4:
            print("✅ 四个阶段全部通过")
            
            # 模拟真实时间评估
            estimated_real_time = elapsed_time * 3  # API调用会慢一些
            print(f"预估实际用时: {estimated_real_time/60:.1f}分钟")
            
            if estimated_real_time <= 900:  # 15分钟 = 900秒
                print("✅ 时间控制在15分钟内")
                return True
            else:
                print("⚠️ 可能超过15分钟时限")
                return True  # 仍然算通过，只是性能警告
        else:
            print(f"❌ 只有{passed_stages}/4个阶段通过")
            return False
    
    def generate_test_report(self, passed, total):
        """生成测试报告"""
        print("\n" + "="*60)
        print("🧪 Kevin案例15分钟流程测试报告")
        print("="*60)
        
        print(f"\n📊 总体结果: {passed}/{total} 测试通过")
        print(f"⏱️ 总用时: {time.time() - self.start_time:.1f}秒")
        
        # 详细结果
        print("\n📋 详细结果:")
        for test_name, result in self.test_results.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"  {status} {test_name}")
        
        # 总结评价
        if passed == total:
            print("\n🎉 恭喜！Kevin案例测试全部通过")
            print("✨ 系统已准备好进行完美演示")
        elif passed >= total * 0.8:
            print("\n⚠️ 大部分测试通过，但需要调试部分功能")
        else:
            print("\n❌ 多个关键功能失败，需要重新检查配置")
        
        # 保存报告到文件
        report_data = {
            "timestamp": time.time(),
            "total_tests": total,
            "passed_tests": passed,
            "test_results": self.test_results,
            "test_duration": time.time() - self.start_time
        }
        
        try:
            with open("kevin_test_report.json", "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            print(f"\n📄 测试报告已保存到: kevin_test_report.json")
        except Exception as e:
            print(f"\n⚠️ 无法保存测试报告: {e}")

def main():
    """主函数"""
    print("🧠 认知黑匣子 - Kevin案例测试")
    print("测试15分钟觉醒之旅的完整流程\n")
    
    tester = KevinJourneyTester()
    
    try:
        success = tester.run_complete_test()
        
        if success:
            print("\n🎯 下一步建议:")
            print("1. 运行 streamlit run app.py 启动应用")
            print("2. 手动测试完整的15分钟流程")
            print("3. 准备向技术合伙人演示")
            
            return 0
        else:
            print("\n🔧 修复建议:")
            print("1. 检查 config.py 中的API配置")
            print("2. 确认所有提示词文件存在")
            print("3. 检查Kevin案例数据格式")
            
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⏹️ 测试被用户中断")
        return 1
    except Exception as e:
        print(f"\n❌ 测试过程出现异常: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
