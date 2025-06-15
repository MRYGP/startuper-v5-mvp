"""
15分钟认知觉醒之旅流程编排器 - P0级修复版本
🔥 修复AI效能欺骗性断裂：让AI真正使用知识库进行诊断
"""
import streamlit as st
import json
import re
from pathlib import Path
from datetime import datetime
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL, GEMINI_GENERATION_CONFIG

class JourneyOrchestrator:
    """15分钟认知觉醒之旅编排器"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.prompts_dir = self.base_dir / "prompts"
        self.demo_cases_dir = self.base_dir / "demo_cases"
        # 🔥 P0修复：添加知识库目录
        self.knowledge_base_dir = self.base_dir / "knowledge_base" / "diagnosis_system"
        
        # 初始化Gemini
        self._init_gemini()
        
        # 初始化会话状态
        self._init_session_state()
    
    def _init_gemini(self):
        """初始化Gemini API - 改进错误处理"""
        try:
            if not GOOGLE_API_KEY:
                print("❌ GOOGLE_API_KEY 未配置")
                self.model = None
                return
                
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(
                model_name=GEMINI_MODEL,
                generation_config=GEMINI_GENERATION_CONFIG
            )
            print("✅ Gemini模型初始化成功")
        except Exception as e:
            print(f"❌ Gemini模型初始化失败: {e}")
            self.model = None
    
    def _init_session_state(self):
        """初始化会话状态"""
        if "journey" not in st.session_state:
            st.session_state.journey = {
                "stage": 0,  # 0:开场, 1:Demo输入, 2:诊断, 3:质询, 4:教学, 5:内化
                "demo_mode": True,
                "demo_case_id": "case_02_team_conflict",  # Kevin案例
                "start_time": None,
                "user_responses": [],
                "ai_responses": {},
                "stage_completion": [False] * 6,
                "kevin_case_data": self._load_kevin_case()
            }
    
    # 🔥 P0修复：新增知识库读取方法
    def _load_knowledge_base(self, filename):
        """加载知识库文件 - P0级核心修复"""
        try:
            kb_path = self.knowledge_base_dir / filename
            print(f"🔍 尝试读取知识库: {kb_path}")
            print(f"🔍 文件是否存在: {kb_path.exists()}")
            
            with open(kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ 成功读取知识库 {filename}，包含 {len(data)} 个顶级键")
                if filename == "diagnosis_rules.json" and "problem_categories" in data:
                    print(f"🔍 诊断规则库包含 {len(data['problem_categories'])} 个问题类别")
                elif filename == "failure_cases.json" and "failure_categories" in data:
                    print(f"🔍 失败案例库包含 {len(data['failure_categories'])} 个案例类别")
                return data
        except Exception as e:
            print(f"❌ 加载知识库失败 {filename}: {e}")
            print(f"❌ 知识库目录: {self.knowledge_base_dir}")
            print(f"❌ 知识库目录是否存在: {self.knowledge_base_dir.exists()}")
            return None

    def _inject_knowledge_base_to_prompt(self, prompt_template, knowledge_data, instruction):
        """将知识库数据注入到提示词中 - P0级核心修复"""
        if knowledge_data:
            knowledge_json = json.dumps(knowledge_data, ensure_ascii=False, indent=2)
            knowledge_block = f"""
{instruction}

<knowledge_base>
{knowledge_json}
</knowledge_base>

请严格基于上述知识库内容进行分析和响应。"""
            return prompt_template + "\n\n" + knowledge_block
        else:
            fallback_notice = "\n\n⚠️ 知识库暂时不可用，请基于专业知识进行分析。"
            return prompt_template + fallback_notice
    
    def _load_kevin_case(self):
        """加载Kevin案例数据"""
        try:
            kevin_file = self.demo_cases_dir / "case_02_team_conflict.json"
            with open(kevin_file, 'r', encoding='utf-8') as f:
                case_data = json.load(f)
            
            # 从Kevin案例中提取6个问题的答案
            six_answers = case_data.get("six_questions_answers", {})
            answers_list = []
            
            for i in range(1, 7):
                question_key = f"question_{i}"
                if question_key in six_answers:
                    answers_list.append(six_answers[question_key]["answer"])
            
            return {
                "case_name": case_data.get("case_meta", {}).get("case_name", "团队合伙人冲突"),
                "protagonist": case_data.get("character_profile", {}).get("name", "李华"),
                "six_answers": answers_list,
                "expected_diagnosis": case_data.get("expected_diagnosis", {}).get("primary_trap", "团队认知偏差")
            }
            
        except Exception as e:
            print(f"⚠️ 加载Kevin案例失败: {e}")
            # 返回默认数据
            return {
                "case_name": "技术合伙人产品方向冲突",
                "protagonist": "Kevin",
                "six_answers": [
                    "我和技术合伙人一起做企业协作SaaS，我负责产品和融资，他负责研发。我们在产品方向上产生了严重分歧。",
                    "我们预期一年内完成A轮融资，覆盖1000家企业用户。实际上争论了8个月，产品既没有技术领先也没有抢到市场先机，现在就剩我一个人。",
                    "我最笃定的信念是：只要找到对的人，事情就一定能做成。我觉得我们三个人的组合几乎是完美的。",
                    "一个师兄警告过我三人合伙制很危险，但我觉得他太悲观了。我们关系这么好，怎么可能因为决策机制闹矛盾？",
                    "我最困惑的是：为什么三个都很聪明的人，在一起反而做不出聪明的决策？作为CEO，我应该怎么处理合伙人之间的深层认知差异？",
                    "我希望能理解团队合作背后的深层逻辑，特别是认知层面的问题。我需要一套思维框架来避免再次陷入同样的认知陷阱。"
                ],
                "expected_diagnosis": "团队认知偏差：镜子陷阱"
            }
    
    def load_prompt_template(self, prompt_filename):
        """加载提示词模板文件"""
        try:
            prompt_file = self.prompts_dir / f"{prompt_filename}.md"
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取## 核心指令后的内容作为提示词
            core_instruction_match = re.search(r'## 核心指令\s*\n(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL)
            if core_instruction_match:
                return core_instruction_match.group(1).strip()
            else:
                # 如果没有找到核心指令，返回整个文件内容
                return content
                
        except Exception as e:
            print(f"⚠️ 加载提示词文件失败 {prompt_filename}: {e}")
            return None
    
    def call_gemini_api(self, prompt, max_retries=3):
        """调用Gemini API - 改进的错误处理"""
        if not self.model:
            return {
                "error": "Gemini模型未初始化，请检查API配置",
                "error_type": "model_init_error",
                "success": False
            }
            
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                if response.text:
                    return {
                        "content": response.text,
                        "success": True
                    }
            except Exception as e:
                error_msg = str(e).lower()
                
                # 根据错误类型返回友好的错误信息
                if "api" in error_msg and "key" in error_msg:
                    return {
                        "error": "API密钥无效，请检查GOOGLE_API_KEY配置",
                        "error_type": "api_key_error",
                        "success": False
                    }
                elif "quota" in error_msg or "limit" in error_msg:
                    return {
                        "error": "API调用额度不足，请稍后重试",
                        "error_type": "quota_error",
                        "success": False
                    }
                elif "network" in error_msg or "connection" in error_msg:
                    return {
                        "error": "网络连接失败，请检查网络连接",
                        "error_type": "network_error",
                        "success": False
                    }
                elif attempt == max_retries - 1:
                    return {
                        "error": f"API调用失败：{str(e)[:100]}",
                        "error_type": "api_error",
                        "success": False
                    }
                    
                # 如果不是最后一次尝试，继续重试
                continue
        
        return {
            "error": "多次重试后仍然失败，请稍后再试",
            "error_type": "retry_exhausted",
            "success": False
        }
    
    # 🔥 P0修复：优化JSON解析稳定性
    def extract_json_from_response(self, response_text):
        """从AI响应中提取JSON - 增强版本"""
        try:
            # 🔥 优先提取 ```json ``` 包裹的内容
            json_block_match = re.search(r'```json\s*\n(.*?)\n```', response_text, re.DOTALL)
            if json_block_match:
                json_str = json_block_match.group(1).strip()
                return json.loads(json_str)
            
            # 降级到原有方法
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                return {"content": response_text, "raw_response": True}
        except Exception as e:
            print(f"⚠️ JSON解析失败: {e}")
            return {"content": response_text, "error": str(e)}
    
    # 🔥 P0修复：让AI真正使用诊断规则库
    def stage2_diagnosis(self, user_responses):
        """阶段2：使用P-H-02进行诊断 - 真实知识库版本"""
        # 🔥 临时调试：检查数据传递
        print(f"🔍 诊断阶段收到的user_responses: {user_responses}")
        print(f"🔍 user_responses长度: {len(user_responses) if user_responses else 'None'}")
        
        if not user_responses or len(user_responses) == 0:
            print("❌ 用户回答为空！使用降级处理")
            return self._fallback_diagnosis([])
        
        prompt_template = self.load_prompt_template("P-H-02-v1.0")
        if not prompt_template:
            return self._fallback_diagnosis(user_responses)
        
        # 🔥 关键修复：读取真实的诊断规则库
        diagnosis_rules = self._load_knowledge_base("diagnosis_rules.json")
        
        # 构建用户故事
        user_story = "\n\n".join([f"Q{i+1}: {resp}" for i, resp in enumerate(user_responses)])
        print(f"🔍 构建的用户故事: {user_story[:200]}...")
        
        # 🔥 强化知识库注入 - 更强制的方式
        if diagnosis_rules:
            knowledge_json = json.dumps(diagnosis_rules, ensure_ascii=False, indent=2)
            prompt = f"""## 诊断规则库
以下是你必须严格遵循的诊断规则库，包含所有认知陷阱的关键词匹配规则：

{knowledge_json}

## 用户输入数据
用户已回答6个问题，完整内容如下：
{user_story}

## 执行指令
{prompt_template}

CRITICAL: 你必须严格基于上述诊断规则库进行分析，不得脱离规则库内容。请仔细匹配关键词和情感模式。"""
        else:
            prompt = f"{prompt_template}\n\n用户回答：\n{user_story}"
        
        # 🔥 强制要求中文输出和JSON格式
        prompt += "\n\n重要：你的回答必须是中文，且必须严格按照JSON格式输出，用```json包裹。绝对不要输出思考过程，只输出JSON结果。"
        
        print(f"🔍 发送给AI的prompt长度: {len(prompt)}")
        
        api_response = self.call_gemini_api(prompt)
        
        # 检查API调用是否成功
        if not api_response.get("success", False):
            print(f"❌ API调用失败: {api_response.get('error')}")
            return api_response
        
        result = self.extract_json_from_response(api_response["content"])
        print(f"🔍 诊断结果: {result}")
        
        return result
    
    # 🔥 P0修复：让AI真正使用失败案例库
    def stage3_investor_interrogation(self, diagnosis, user_story):
        """阶段3：使用P-I-01投资人质询 - 真实案例库版本"""
        print(f"🔍 投资人阶段 - 诊断结果: {diagnosis}")
        print(f"🔍 投资人阶段 - 用户故事长度: {len(user_story) if user_story else 'None'}")
        
        prompt_template = self.load_prompt_template("P-I-01-v1.0")
        if not prompt_template:
            return self._fallback_investor_response(diagnosis)
        
        # 🔥 关键修复：读取真实的失败案例库
        failure_cases = self._load_knowledge_base("failure_cases.json")
        
        # 构建变量替换
        user_case_summary = user_story[:500] + "..." if len(user_story) > 500 else user_story
        final_trap = diagnosis.get("diagnosis_result", {}).get("final_trap", "认知陷阱")
        
        print(f"🔍 final_trap: {final_trap}")
        print(f"🔍 user_case_summary: {user_case_summary[:100]}...")
        
        # 🔥 强化案例库注入 - 更强制的方式
        if failure_cases:
            cases_json = json.dumps(failure_cases, ensure_ascii=False, indent=2)
            prompt = f"""## 失败案例库
以下是你必须使用的宏大商业失败案例库：

{cases_json}

## 诊断信息
- 用户案例摘要: {user_case_summary}
- 诊断出的认知陷阱: {final_trap}

## 执行指令
{prompt_template}

CRITICAL: 你必须从上述案例库中选择与"{final_trap}"最相关的具体案例，不得使用通用模板。必须生成具体的、针对性的质询内容。"""
        else:
            prompt = prompt_template.replace("{user_case_summary}", user_case_summary)
            prompt = prompt.replace("{final_trap}", final_trap)
        
        # 🔥 强制中文输出
        prompt += "\n\n重要：你的回答必须是中文，且必须严格按照JSON格式输出，用```json包裹。必须基于具体的失败案例，不得使用模板内容。"
        
        print(f"🔍 投资人prompt长度: {len(prompt)}")
        
        api_response = self.call_gemini_api(prompt)
        
        if not api_response.get("success", False):
            print(f"❌ 投资人API调用失败: {api_response.get('error')}")
            return api_response
        
        result = self.extract_json_from_response(api_response["content"])
        print(f"🔍 投资人结果: {result}")
        
        return result
    
    # 🔥 P0修复：增强导师教学阶段
    def stage4_mentor_teaching(self, diagnosis):
        """阶段4：使用P-M-01导师教学 - 增强版本"""
        prompt_template = self.load_prompt_template("P-M-01-v1.0")
        if not prompt_template:
            return self._fallback_mentor_response(diagnosis)
        
        # 可选：读取智慧金句库增强教学内容
        wisdom_quotes = self._load_knowledge_base("wisdom_quotes.json")
        
        # 构建变量替换
        final_trap = diagnosis.get("diagnosis_result", {}).get("final_trap", "认知陷阱")
        user_case_summary = "用户案例摘要"  # 可以根据需要添加更多上下文
        
        prompt = prompt_template.replace("{final_trap}", final_trap)
        prompt = prompt.replace("{user_case_summary}", user_case_summary)
        
        # 可选：如果有智慧金句库，注入相关金句
        if wisdom_quotes:
            wisdom_instruction = f"""
你可以参考以下智慧金句库中与 '{final_trap}' 相关的金句来增强教学效果："""
            prompt = self._inject_knowledge_base_to_prompt(
                prompt, wisdom_quotes, wisdom_instruction
            )
        
        # 🔥 强制中文输出
        prompt += "\n\n重要：你的回答必须是中文，且必须严格按照JSON格式输出，用```json包裹。"
        
        api_response = self.call_gemini_api(prompt)
        
        if not api_response.get("success", False):
            return api_response
        
        return self.extract_json_from_response(api_response["content"])
    
    def stage5_assistant_summary(self, all_data, weapon_name, personal_reminder):
        """阶段5：使用P-A-03生成武器卡片"""
        prompt_template = self.load_prompt_template("P-A-03-v1.0")
        if not prompt_template:
            return self._fallback_assistant_response(weapon_name, personal_reminder)
        
        # 构建变量替换
        final_trap = all_data.get("diagnosis", {}).get("diagnosis_result", {}).get("final_trap", "认知陷阱")
        
        prompt = prompt_template.replace("{custom_weapon_name}", weapon_name)
        prompt = prompt.replace("{final_trap}", final_trap)
        prompt = prompt.replace("{custom_reminder}", personal_reminder)
        
        # 🔥 强制中文输出
        prompt += "\n\n重要：你的回答必须是中文，且必须严格按照JSON格式输出，用```json包裹。"
        
        api_response = self.call_gemini_api(prompt)
        
        if not api_response.get("success", False):
            return api_response
        
        return self.extract_json_from_response(api_response["content"])
    
    # 降级处理方法（保持现有逻辑但移除硬编码）
    def _fallback_diagnosis(self, user_responses):
        """诊断失败时的降级处理 - 移除硬编码"""
        user_story = " ".join(user_responses)
        
        # 🔥 P0修复：使用更通用的规则判断，而非硬编码
        if any(keyword in user_story for keyword in ["合伙人", "创始人", "冲突", "分歧", "团队"]):
            return {
                "diagnosis_result": {
                    "final_trap": "团队认知偏差：镜子陷阱",
                    "confidence": 0.90,
                    "matched_prescriptions": ["P20"]
                },
                "content": "使用降级处理：基于关键词识别为团队问题"
            }
        elif any(keyword in user_story for keyword in ["技术", "用户不买账", "没人用", "复杂"]):
            return {
                "diagnosis_result": {
                    "final_trap": "技术至上偏见",
                    "confidence": 0.85,
                    "matched_prescriptions": ["P01"]
                },
                "content": "使用降级处理：基于关键词识别为技术偏见"
            }
        else:
            return {
                "diagnosis_result": {
                    "final_trap": "确认偏见",
                    "confidence": 0.80,
                    "matched_prescriptions": ["P02"]
                },
                "content": "使用降级处理：通用认知偏见"
            }
    
    def _fallback_investor_response(self, diagnosis):
        """投资人质询失败时的降级处理"""
        final_trap = diagnosis.get("diagnosis_result", {}).get("final_trap", "认知陷阱")
        
        if "团队" in final_trap:
            return {
                "four_act_interrogation": {
                    "act1_assumption_attack": "你认为问题在于合伙人不理解你的愿景，但有没有想过，问题可能出在你们根本就没有建立有效的决策机制？",
                    "act2_opportunity_cost": "你们为了争论产品方向浪费了8个月时间，按每月5万成本计算，这是40万的直接损失，更别提错失的市场机会。",
                    "act3_grand_failure_case": {
                        "case_name": "某知名SaaS公司团队解散",
                        "brief_story": "三位前BAT高管联合创业，18个月内从意见分歧到团队解散，烧光3000万。",
                        "cognitive_trap_connection": "和你一样，他们都陷入了'强强联合就能成功'的认知误区。"
                    },
                    "act4_root_cause": "你面对的根本不是产品问题，而是团队认知系统性失调的问题。"
                },
                "final_verdict": "结论：团队协作能力严重不足，建议在解决认知框架问题前暂缓新的合作。",
                "content": "使用降级处理：团队冲突投资人质询模板"
            }
        else:
            return {
                "four_act_interrogation": {
                    "act1_assumption_attack": "你坚信技术优势就能赢得市场，但用户真的在乎你的技术有多先进吗？",
                    "act2_opportunity_cost": "在技术完美主义上投入的时间和资源，本可以用来验证真实的用户需求。",
                    "act3_grand_failure_case": {
                        "case_name": "Google Wave",
                        "brief_story": "技术极其先进的实时协作平台，但用户觉得太复杂，最终失败。",
                        "cognitive_trap_connection": "技术先进不等于用户价值，这是很多技术创业者的通病。"
                    },
                    "act4_root_cause": "你陷入了技术至上的认知陷阱，混淆了技术价值和用户价值。"
                },
                "final_verdict": "结论：需要从技术思维转向用户价值思维，重新定义产品成功标准。",
                "content": "使用降级处理：技术至上投资人质询模板"
            }
    
    def _fallback_mentor_response(self, diagnosis):
        """导师教学失败时的降级处理"""
        final_trap = diagnosis.get("diagnosis_result", {}).get("final_trap", "认知陷阱")
        
        if "团队" in final_trap:
            return {
                "opening_statement": {
                    "diagnosis_recap": "投资人雷的分析虽然犀利，但指出了关键问题：团队协作的认知框架缺失。",
                    "weapon_introduction": "今天我要传授给你的是'团队认知对齐框架'，这是解决合伙人冲突的根本工具。"
                },
                "visual_framework": {
                    "type": "mermaid",
                    "code": "graph TD\n    A[识别认知差异] --> B[建立对话机制]\n    B --> C[寻找共同目标]\n    C --> D[制定决策框架]\n    D --> E[持续校准执行]",
                    "title": "团队认知对齐框架",
                    "description": "从认知差异到高效协作的系统性方法"
                },
                "step_breakdown": [
                    {
                        "step_name": "第一步：识别认知差异",
                        "explanation": "不同背景的人对同一个问题会有不同的认知框架，这是正常的。",
                        "action": "明确列出每个人对关键问题的观点和逻辑。"
                    },
                    {
                        "step_name": "第二步：建立对话机制",
                        "explanation": "有效的对话需要规则和流程，不能靠情感和直觉。",
                        "action": "设定定期的决策会议，每个人都有平等的发言权。"
                    },
                    {
                        "step_name": "第三步：制定决策框架", 
                        "explanation": "用统一的标准来评估不同的选择，避免主观判断。",
                        "action": "建立清晰的决策流程和评估标准。"
                    }
                ],
                "power_comparison": {
                    "title": "平行宇宙：团队协作模式对比",
                    "markdown_table": "| 维度 | 🔴 原有模式 | 🟢 新框架模式 |\n|------|-------------|---------------|\n| 决策方式 | 基于个人经验和直觉 | 基于统一框架和数据 |\n| 冲突处理 | 情感化争论，互相指责 | 理性讨论，聚焦问题 |\n| 最终结果 | 团队解散，项目失败 | 高效协作，持续成长 |",
                    "value_gap_analysis": "仅仅是决策框架的改变，就可能避免团队解散的悲剧，节约数百万的重新开始成本。"
                },
                "content": "使用降级处理：团队认知对齐框架教学模板"
            }
        else:
            return {
                "opening_statement": {
                    "diagnosis_recap": "投资人的分析很到位，你确实陷入了技术至上的思维陷阱。",
                    "weapon_introduction": "我要传授的是'用户价值导向框架'，帮你从技术思维转向价值思维。"
                },
                "visual_framework": {
                    "type": "mermaid", 
                    "code": "graph TD\n    A[用户问题识别] --> B[解决方案设计]\n    B --> C[技术实现]\n    C --> D[用户验证]\n    D --> E[迭代优化]",
                    "title": "用户价值导向框架",
                    "description": "从用户需求出发的产品开发方法论"
                },
                "step_breakdown": [
                    {
                        "step_name": "第一步：用户问题识别",
                        "explanation": "技术必须服务于真实的用户问题，而不是技术本身。",
                        "action": "深度调研用户的真实痛点和使用场景。"
                    },
                    {
                        "step_name": "第二步：最简解决方案",
                        "explanation": "用最简单的方式解决核心问题，避免过度工程化。",
                        "action": "设计最小可行产品（MVP）进行快速验证。"
                    }
                ],
                "power_comparison": {
                    "title": "平行宇宙：产品开发模式对比",
                    "markdown_table": "| 维度 | 🔴 技术驱动模式 | 🟢 用户价值模式 |\n|------|----------------|------------------|\n| 起点 | 技术可能性 | 用户问题 |\n| 验证方式 | 技术指标 | 用户反馈 |\n| 成功标准 | 技术先进性 | 用户满意度 |",
                    "value_gap_analysis": "从技术驱动转向用户驱动，可以大幅提高产品成功率和市场接受度。"
                },
                "content": "使用降级处理：用户价值导向框架教学模板"
            }
    
    def _fallback_assistant_response(self, weapon_name, personal_reminder):
        """助理总结失败时的降级处理"""
        return {
            "dialogue": "虽然AI服务暂时不稳定，但你的专属武器已经准备好了！",
            "weapon_card": {
                "design_style": {
                    "background_color": "#F8F9FA",
                    "border": "2px solid #4A90E2",
                    "border_radius": "15px"
                },
                "content": {
                    "title": f"🛡️ 我的决策武器：{weapon_name}",
                    "sections": [
                        {
                            "icon": "🎯",
                            "title": "专治病症",
                            "content": "认知陷阱和思维盲区"
                        },
                        {
                            "icon": "⚡",
                            "title": "核心原理",
                            "content": "系统性思维框架，提升决策质量"
                        },
                        {
                            "icon": "❤️‍🩹",
                            "title": "我的血泪提醒",
                            "content": personal_reminder
                        }
                    ]
                },
                "metadata": {
                    "created_date": datetime.now().isoformat(),
                    "version": "1.0",
                    "generated_by": "Cognitive Blackbox"
                }
            },
            "content": "使用降级处理：基础武器卡片模板"
        }
    
    # 流程控制方法（保持不变）
    def get_current_stage(self):
        """获取当前阶段"""
        return st.session_state.journey["stage"]
    
    def advance_stage(self):
        """推进到下一阶段"""
        current = st.session_state.journey["stage"]
        if current < 5:
            st.session_state.journey["stage"] = current + 1
            st.session_state.journey["stage_completion"][current] = True
            return True
        return False
    
    def switch_to_custom_mode(self):
        """切换到自定义模式（不可逆）"""
        st.session_state.journey["demo_mode"] = False
    
    def is_demo_mode(self):
        """是否为Demo模式"""
        return st.session_state.journey["demo_mode"]
    
    def save_user_responses(self, responses):
        """保存用户回答"""
        st.session_state.journey["user_responses"] = responses
        # 同时保存到全局session state，确保跨组件访问
        st.session_state.user_responses = responses
    
    def save_ai_response(self, stage, response):
        """保存AI回答"""
        st.session_state.journey["ai_responses"][f"stage_{stage}"] = response
    
    def get_ai_response(self, stage):
        """获取AI回答"""
        return st.session_state.journey["ai_responses"].get(f"stage_{stage}")
    
    def reset_journey(self):
        """重置整个流程"""
        if "journey" in st.session_state:
            del st.session_state.journey
        if "user_responses" in st.session_state:
            del st.session_state.user_responses
        self._init_session_state()
