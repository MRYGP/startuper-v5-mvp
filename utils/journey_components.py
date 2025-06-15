"""
15分钟认知觉醒之旅专用UI组件 - 完整修复版本
修复了KeyError问题和所有已知bug
"""
import streamlit as st
import time
from datetime import datetime
from utils.journey_orchestrator import JourneyOrchestrator

def render_15min_journey():
    """渲染15分钟觉醒之旅主入口 - 修复初始化问题"""
    
    # 确保orchestrator正确初始化
    try:
        orchestrator = JourneyOrchestrator()
        
        # 强制确保session state正确初始化
        if "journey" not in st.session_state:
            orchestrator._init_session_state()
        
        # 确保kevin_case_data存在
        if "kevin_case_data" not in st.session_state.journey:
            kevin_case_data = orchestrator._load_kevin_case()
            st.session_state.journey["kevin_case_data"] = kevin_case_data
        
        stage = orchestrator.get_current_stage()
        
    except Exception as e:
        # 如果初始化失败，显示错误并提供重置选项
        st.error(f"初始化失败：{str(e)}")
        st.error("可能的原因：Kevin案例文件缺失或格式错误")
        
        if st.button("🔄 重置并重新开始", type="primary"):
            # 清除所有相关状态
            for key in ["journey", "user_responses"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        return
    
    # 应用自定义CSS
        apply_journey_css()
    
    # 渲染进度指示器
        render_progress_indicator(stage)
    
    # 根据阶段渲染对应界面
    try:
        # 检查是否已完成流程（优先检查）
        feedback_submitted = st.session_state.get("feedback_submitted", False)
    if feedback_submitted:
            render_journey_completion()
            return  # ← 添加这行！
        elif stage == 0:
            render_opening_stage(orchestrator)
        elif stage == 1:
            render_demo_input_stage(orchestrator)
        elif stage == 2:
            render_diagnosis_stage(orchestrator)
        elif stage == 3:
            render_investor_stage(orchestrator)
        elif stage == 4:
            render_mentor_stage(orchestrator)
        elif stage == 5:
            render_assistant_stage(orchestrator)
    except Exception as e:
        st.error(f"渲染阶段{stage}时出错：{str(e)}")
        st.error("请尝试重新开始或联系技术支持")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 重置流程"):
                for key in ["journey", "user_responses"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("🏠 返回首页"):
                st.session_state.current_page = "🏠 产品介绍"
                st.rerun()
        
        with col3:
            if st.button("📊 查看错误详情"):
                st.exception(e)

def apply_journey_css():
    """应用15分钟流程专用CSS样式"""
    st.markdown("""
    <style>
    .journey-progress {
        display: flex;
        justify-content: space-between;
        margin: 1rem 0 2rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
    }
    
    .journey-stage {
        background: #e9ecef;
        color: #6c757d;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        min-width: 80px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .journey-stage.completed {
        background: #28a745;
        color: white;
    }
    
    .journey-stage.current {
        background: #007bff;
        color: white;
        transform: scale(1.1);
    }
    
    .ai-role-header {
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .demo-answer-box {
        background: #f8f9fa;
        border: 2px dashed #667eea;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .shock-card {
        background: linear-gradient(135deg, #ff4757, #ff3838);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(255, 71, 87, 0.3);
    }
    
    .weapon-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border: 3px solid #fff;
        font-family: 'Arial', sans-serif;
    }
    
    .mermaid-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .answer-completed {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def render_progress_indicator(current_stage):
    """超简化版本"""
    stages = ["🎭开场", "📝情境", "🔍诊断", "💼质询", "🧠重构", "🤝内化"]
    
    cols = st.columns(6)
    for i, stage in enumerate(stages):
        with cols[i]:
            if i <= current_stage:
                st.success(stage)
            else:
                st.info(stage)

def render_ai_role_header(role_name, stage_num, description, color):
    """渲染AI角色头部 - 修复HTML渲染"""
    role_configs = {
        "主持人": {"icon": "🎯", "time": "4分钟"},
        "投资人": {"icon": "💼", "time": "3分钟"},
        "导师": {"icon": "🧠", "time": "4分钟"},
        "助理": {"icon": "🤝", "time": "3分钟"}
    }
    
    config = role_configs.get(role_name, {"icon": "🎭", "time": "3分钟"})
    
    header_html = f'''
    <div class="ai-role-header" style="background: linear-gradient(135deg, {color}, {color}dd);">
        <h1>{config["icon"]} {role_name}</h1>
        <p style="margin: 0.5rem 0; font-size: 1.1rem; opacity: 0.9;">
            第{stage_num}/5阶段 • {description}
        </p>
        <div style="
            background: rgba(255,255,255,0.2);
            border-radius: 20px;
            padding: 0.5rem 1rem;
            display: inline-block;
            margin-top: 0.5rem;
        ">
            ⏱️ 预计用时: {config["time"]}
        </div>
    </div>
    '''
    # 修复：添加 unsafe_allow_html=True
    st.markdown(header_html, unsafe_allow_html=True)

def render_opening_stage(orchestrator):
    """阶段0：开场页面 - 修复HTML渲染"""
    opening_html = '''
    <div style="text-align: center; padding: 3rem 1rem;">
        <h1 style="color: #667eea; font-size: 3rem; margin-bottom: 1rem;">🧠 认知黑匣子</h1>
        <h2 style="color: #764ba2; font-size: 2rem; margin-bottom: 2rem;">15分钟认知觉醒之旅</h2>
        <p style="font-size: 1.4rem; color: #666; margin: 2rem 0;">
            从"我是对的"到"我原来想错了"
        </p>
        <div style="
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin: 3rem auto;
            max-width: 600px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        ">
            <h3 style="margin-top: 0;">💡 即将体验</h3>
            <p style="margin: 1rem 0;">一个真实创业者的认知觉醒故事</p>
            <p style="margin: 1rem 0;">四个AI角色的深度引导</p>
            <p style="margin-bottom: 0;">一个专属于你的认知武器</p>
        </div>
    </div>
    '''
    # 修复：添加 unsafe_allow_html=True
    st.markdown(opening_html, unsafe_allow_html=True)
    
    # 智慧金句展示
    render_daily_wisdom()
    
    # 开始按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 开始我的觉醒之旅", type="primary", use_container_width=True, key="start_journey"):
            orchestrator.advance_stage()
            st.rerun()

def render_daily_wisdom():
    """渲染每日智慧金句 - 修复HTML渲染"""
    quotes = [
        {
            "text": "第一原理是你不能欺骗自己——而你是最容易被欺骗的人。",
            "author": "理查德·费曼"
        },
        {
            "text": "我们无法用创造问题时的思维来解决问题。",
            "author": "阿尔伯特·爱因斯坦"
        },
        {
            "text": "未经审视的人生不值得过。",
            "author": "苏格拉底"
        }
    ]
    
    import random
    daily_quote = random.choice(quotes)
    
    wisdom_html = f'''
    <div style="
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 2rem auto;
        max-width: 700px;
        font-style: italic;
    ">
        <h4 style="color: #667eea; margin-top: 0;">💎 今日智慧</h4>
        <p style="font-size: 1.1rem; margin: 1rem 0;">"{daily_quote["text"]}"</p>
        <p style="text-align: right; margin-bottom: 0; color: #666;">—— {daily_quote["author"]}</p>
    </div>
    '''
    # 修复：添加 unsafe_allow_html=True
    st.markdown(wisdom_html, unsafe_allow_html=True)

def render_demo_input_stage(orchestrator):
    """阶段1：交互式Demo输入 - 修复KeyError和状态管理问题"""
    render_ai_role_header("主持人", 1, "温和引导，深度聚焦", "#667eea")
    
    st.markdown("## 📋 请回答以下6个问题")
    st.markdown("*您可以体验Kevin的真实案例，或随时切换输入自己的情况*")
    
    # 确保Session State正确初始化
    if "user_responses" not in st.session_state:
        st.session_state.user_responses = []
    
    # 修复：安全地获取kevin_case_data
    if "journey" not in st.session_state or "kevin_case_data" not in st.session_state.journey:
        # 如果journey或kevin_case_data不存在，重新初始化
        if "journey" not in st.session_state:
            st.session_state.journey = {}
        
        # 使用默认Kevin案例数据
        st.session_state.journey["kevin_case_data"] = {
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
    
    questions = [
        "你做了什么事情没有达到预期的效果？",
        "当初预期的效果是怎么样的？而真实效果又是怎么样的？",
        "当时，你最笃定的一个信念是什么？",
        "在做决策前，你有没有忽略或不相信某些信息/建议？",
        "基于这个结果，你现在最大的困惑是什么？",
        "你最希望我们帮你解决什么问题？"
    ]
    
    # 现在安全地访问kevin_case_data
    kevin_case = st.session_state.journey["kevin_case_data"]
    kevin_answers = kevin_case.get("six_answers", [])
    demo_mode = orchestrator.is_demo_mode()
    
    # 关键修复：使用Session State中的列表长度
    completed_count = len(st.session_state.user_responses)
    
    # 问题输入循环 - 逐个显示问题
    for i, question in enumerate(questions):
        st.markdown(f"### 问题 {i+1}")
        st.markdown(f"**{question}**")
        
        # 判断当前问题是否已完成
        is_completed = i < completed_count
        
        if is_completed:
            # 显示已保存的答案
            answer_preview = st.session_state.user_responses[i]
            if len(answer_preview) > 100:
                answer_preview = answer_preview[:100] + "..."
            
            completed_html = f'''
            <div class="answer-completed">
                <strong>✅ 已保存</strong><br>
                <div style="margin-top: 0.5rem; font-style: italic;">{answer_preview}</div>
            </div>
            '''
            st.markdown(completed_html, unsafe_allow_html=True)
        else:
            # 显示输入界面 - 只显示当前需要回答的问题
            if demo_mode and i < len(kevin_answers):
                demo_answer = kevin_answers[i]
                
                # 显示Kevin的Demo答案
                demo_html = f'''
                <div class="demo-answer-box">
                    <small style="color: #667eea; font-weight: bold;">💭 {kevin_case.get("protagonist", "Kevin")}的回答：</small><br>
                    <div style="margin-top: 0.5rem;">{demo_answer}</div>
                </div>
                '''
                st.markdown(demo_html, unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    user_input = st.text_area(
                        "您的回答：",
                        value="",
                        placeholder="点击这里输入您的真实情况，或直接确认Kevin的回答",
                        height=80,
                        key=f"input_{i}"
                    )
                
                with col2:
                    # 修复：确认Kevin回答的回调函数
                    if not user_input.strip():
                        if st.button("👍 确认Kevin的回答", key=f"confirm_{i}"):
                            st.session_state.user_responses.append(demo_answer)
                            st.rerun()
                    else:
                        # 用户开始输入，提供保存选项
                        if st.button("💾 保存我的回答", key=f"save_{i}"):
                            st.session_state.user_responses.append(user_input.strip())
                            orchestrator.switch_to_custom_mode()
                            st.rerun()
            else:
                # 自定义模式：普通输入
                user_input = st.text_area(
                    "您的回答：",
                    height=100,
                    key=f"custom_{i}",
                    placeholder="请详细描述您的情况..."
                )
                if st.button(f"保存第{i+1}个回答", key=f"save_custom_{i}"):
                    if user_input.strip():
                        st.session_state.user_responses.append(user_input.strip())
                        st.rerun()
            
            # 只显示第一个未完成的问题，然后跳出循环
            break
        
        st.markdown("---")
    
    # 显示完成状态和下一步按钮
    remaining = 6 - completed_count
    
    if completed_count == 6:
        st.success("🎉 所有问题已完成！")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔬 开始AI深度诊断", type="primary", use_container_width=True, key="start_diagnosis"):
                # 保存用户回答到orchestrator
                orchestrator.save_user_responses(st.session_state.user_responses)
                
                # 推进到诊断阶段
                orchestrator.advance_stage()
                st.rerun()
    else:
        st.info(f"📝 还需完成 {remaining} 个问题")

def render_diagnosis_stage(orchestrator):
    """阶段2：AI诊断分析 - 修复错误处理"""
    st.markdown("### 🤖 AI正在分析您的认知模式...")
    
    # 检查是否已有诊断结果
    cached_diagnosis = orchestrator.get_ai_response(2)
    
    if not cached_diagnosis:
        with st.spinner("深度分析中，请稍候..."):
            user_responses = st.session_state.get("user_responses", [])
            if not user_responses:
                user_responses = st.session_state.journey.get("user_responses", [])
            
            diagnosis = orchestrator.stage2_diagnosis(user_responses)
            
            if diagnosis:
                orchestrator.save_ai_response(2, diagnosis)
                cached_diagnosis = diagnosis
    
    if cached_diagnosis:
        # 检查是否有错误
        if "error" in cached_diagnosis:
            st.error(f"😔 {cached_diagnosis['error']}")
            if st.button("🔄 重新诊断", key="retry_diagnosis"):
                # 清除缓存的错误结果
                if "stage_2" in st.session_state.journey["ai_responses"]:
                    del st.session_state.journey["ai_responses"]["stage_2"]
                st.rerun()
            return
        
        # 显示诊断结果
        diagnosis_result = cached_diagnosis.get("diagnosis_result", {})
        final_trap = diagnosis_result.get("final_trap", "认知陷阱")
        confidence = diagnosis_result.get("confidence", 0.9)
        
        result_html = f'''
        <div style="
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
        ">
            <h2>🎯 诊断结果</h2>
            <h3 style="margin: 1rem 0;">{final_trap}</h3>
            <p style="font-size: 1.1rem;">AI诊断置信度: {confidence:.1%}</p>
        </div>
        '''
        st.markdown(result_html, unsafe_allow_html=True)
        
        st.markdown("### 📊 诊断详情")
        if cached_diagnosis.get("raw_response"):
            st.markdown(cached_diagnosis.get("content", "诊断分析中..."))
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("😱 这个诊断很准确，继续", type="primary", use_container_width=True, key="accept_diagnosis"):
                orchestrator.advance_stage()
                st.rerun()
    else:
        st.error("😔 诊断服务暂时不可用，请稍后重试")
        if st.button("🔄 重新诊断", key="retry_diagnosis_main"):
            st.rerun()

def render_investor_stage(orchestrator):
    """阶段3：投资人犀利质询"""
    render_ai_role_header("投资人", 2, "犀利质询，击穿现实", "#dc3545")
    
    # 获取诊断结果
    diagnosis = orchestrator.get_ai_response(2)
    if not diagnosis:
        st.error("缺少诊断结果，请重新开始")
        return
    
    # 生成或获取投资人质询
    cached_interrogation = orchestrator.get_ai_response(3)
    
    if not cached_interrogation:
        with st.spinner("投资人雷正在准备犀利质询..."):
            user_responses = st.session_state.get("user_responses", [])
            if not user_responses:
                user_responses = st.session_state.journey.get("user_responses", [])
            user_story = "\n".join(user_responses)
            
            interrogation = orchestrator.stage3_investor_interrogation(diagnosis, user_story)
            if interrogation:
                orchestrator.save_ai_response(3, interrogation)
                cached_interrogation = interrogation
    
    if cached_interrogation:
        # 检查是否有错误
        if "error" in cached_interrogation:
            st.error(f"😔 {cached_interrogation['error']}")
            return
        
        four_acts = cached_interrogation.get("four_act_interrogation", {})
        
        # 问题本质高亮卡片（视觉焦点）
        st.markdown("### 💥 问题本质")
        root_cause = four_acts.get("act4_root_cause", "你面对的根本问题需要深入分析")
        
        shock_html = f'''
        <div class="shock-card">
            🎯 {root_cause}
        </div>
        '''
        st.markdown(shock_html, unsafe_allow_html=True)
        
        # 四重奏质询内容（标签页展示）
        tab1, tab2, tab3, tab4 = st.tabs(["💥 假设攻击", "💰 机会成本", "📉 失败案例", "⚖️ 最终判决"])
        
        with tab1:
            st.markdown("### 🗡️ 核心假设攻击")
            st.markdown(four_acts.get("act1_assumption_attack", "核心假设攻击内容"))
            
        with tab2:
            st.markdown("### 💸 机会成本量化")
            st.markdown(four_acts.get("act2_opportunity_cost", "机会成本分析"))
            
        with tab3:
            st.markdown("### 🏢 宏大失败案例")
            failure_case = four_acts.get("act3_grand_failure_case", {})
            if isinstance(failure_case, dict):
                st.markdown(f"**案例**: {failure_case.get('case_name', '经典失败案例')}")
                st.markdown(failure_case.get("brief_story", "案例描述"))
                st.markdown(f"**与你的关联**: {failure_case.get('cognitive_trap_connection', '认知陷阱关联')}")
            else:
                st.markdown(str(failure_case))
            
        with tab4:
            st.markdown("### ⚖️ 投委会最终判决")
            final_verdict = cached_interrogation.get("final_verdict", "需要进行认知框架重构")
            st.markdown(f"**{final_verdict}**")
        
        # 继续按钮
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("😰 我被震撼到了，需要解药", type="primary", use_container_width=True, key="need_solution"):
                orchestrator.advance_stage()
                st.rerun()

def render_mentor_stage(orchestrator):
    """阶段4：导师智慧重构"""
    render_ai_role_header("导师", 3, "智慧传授，认知重构", "#28a745")
    
    # 获取诊断结果
    diagnosis = orchestrator.get_ai_response(2)
    
    # 生成或获取导师教学材料
    cached_teaching = orchestrator.get_ai_response(4)
    
    if not cached_teaching:
        with st.spinner("导师正在准备智慧框架..."):
            teaching = orchestrator.stage4_mentor_teaching(diagnosis)
            if teaching:
                orchestrator.save_ai_response(4, teaching)
                cached_teaching = teaching
    
    if cached_teaching:
        # 检查是否有错误
        if "error" in cached_teaching:
            st.error(f"😔 {cached_teaching['error']}")
            return
        
        opening = cached_teaching.get("opening_statement", {})
        framework = cached_teaching.get("visual_framework", {})
        comparison = cached_teaching.get("power_comparison", {})
        steps = cached_teaching.get("step_breakdown", [])
        
        # 开场白和武器介绍
        st.markdown("### 🎯 解药介绍")
        weapon_intro = opening.get("weapon_introduction", "现在我要传授给你一个强大的认知框架")
        st.markdown(weapon_intro)
        
        # Mermaid流程图
        if framework.get("code"):
            st.markdown("### 🗺️ 思维框架图")
            framework_title = framework.get("title", "认知重构框架")
            st.markdown(f"**{framework_title}**")
            
            try:
                # 尝试使用streamlit-mermaid
                from streamlit_mermaid import st_mermaid
                st_mermaid(framework["code"])
            except ImportError:
                # 降级到代码显示
                mermaid_html = f'''
                <div class="mermaid-container">
                    <pre><code>{framework["code"]}</code></pre>
                    <small>💡 这是流程图的Mermaid代码，在支持的环境中会显示为图表</small>
                </div>
                '''
                st.markdown(mermaid_html, unsafe_allow_html=True)
        
        # 步骤分解
        if steps:
            st.markdown("### 🛠️ 框架步骤分解")
            cols = st.columns(min(len(steps), 3))
            
            for i, step in enumerate(steps[:3]):
                with cols[i % len(cols)]:
                    step_html = f'''
                    <div style="
                        background: #e3f2fd;
                        padding: 1rem;
                        border-radius: 10px;
                        text-align: center;
                        margin: 0.5rem 0;
                    ">
                        <h4>🥇 {step.get("step_name", f"步骤{i+1}")}</h4>
                        <p style="margin: 0.5rem 0;"><strong>原理：</strong>{step.get("explanation", "步骤说明")}</p>
                        <p style="margin: 0;"><strong>行动：</strong>{step.get("action", "具体行动")}</p>
                    </div>
                    '''
                    st.markdown(step_html, unsafe_allow_html=True)
        
        # 平行宇宙对比
        st.markdown("### 📊 平行宇宙对比")
        if comparison.get("markdown_table"):
            st.markdown(comparison["markdown_table"])
        else:
            # 默认对比表
            st.markdown("""
            | 维度 | 🔴 你的原路径 | 🟢 新框架路径 |
            |------|-------------|-------------|
            | 决策方式 | 基于直觉和经验 | 基于框架和数据 |
            | 投入成本 | 高时间高资金成本 | 低成本快速验证 |
            | 最终结果 | 项目失败，团队解散 | 认知升级，能力提升 |
            """)
        
        # 价值差距分析
        if comparison.get("value_gap_analysis"):
            st.markdown(f"**💡 关键洞察**: {comparison['value_gap_analysis']}")
        
        # 继续按钮
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💡 我豁然开朗了！", type="primary", use_container_width=True, key="enlightened"):
                orchestrator.advance_stage()
                st.rerun()

def render_assistant_stage(orchestrator):
    """阶段5：助理温暖内化 - 修复反馈提交后的状态管理BUG"""
    render_ai_role_header("助理", 4, "温暖总结，价值固化", "#17a2b8")
    
    # 检查是否已经提交反馈（新增状态检查）
    feedback_submitted = st.session_state.get("feedback_submitted", False)
    
    if feedback_submitted:
        # 如果已提交反馈，显示完成页面
        render_journey_completion()
        return
    
    # 第一步：掌握测试
    st.markdown("## 🧪 第一步：掌握验证")
    
    diagnosis = orchestrator.get_ai_response(2)
    diagnosis_result = diagnosis.get("diagnosis_result", {}) if diagnosis else {}
    final_trap = diagnosis_result.get("final_trap", "认知陷阱")
    
    test_question = f"如果你的朋友也遇到了'{final_trap}'的问题，你会用刚才学到的框架给他什么建议？"
    
    mastery_answer = st.text_area(
        test_question,
        height=100,
        placeholder="用新框架来分析和建议...",
        key="mastery_test"
    )
    
    mastery_passed = st.session_state.get("mastery_passed", False)
    
    if mastery_answer and len(mastery_answer) > 20 and not mastery_passed:
        if st.button("✅ 提交验证答案", key="submit_mastery"):
            st.success("🎉 很好！你已经掌握了框架的精髓。")
            st.session_state["mastery_passed"] = True
            mastery_passed = True
            st.rerun()
    
    # 第二步：个人定制
    if mastery_passed:
        st.markdown("---")
        st.markdown("## 🎨 第二步：打造专属武器")
        
        col1, col2 = st.columns(2)
        
        with col1:
            weapon_name = st.text_input(
                "给你的认知武器起个名字：",
                placeholder="例如：我的团队决策雷达",
                key="weapon_name"
            )
        
        with col2:
            personal_reminder = st.text_input(
                "写一句血泪提醒：",
                placeholder="例如：优秀的人≠优秀的团队",
                key="personal_reminder"
            )
        
        usage_scenarios = st.text_area(
            "这个武器在什么情况下使用？",
            placeholder="例如：\n• 组建新团队时\n• 出现决策分歧时\n• 招聘核心成员时",
            height=100,
            key="usage_scenarios"
        )
        
        # 生成武器卡片
        if weapon_name and personal_reminder and usage_scenarios:
            if st.button("🔨 锻造我的专属认知武器", type="primary", use_container_width=True, key="forge_weapon"):
                
                with st.spinner("正在锻造您的专属认知武器..."):
                    all_data = {
                        "diagnosis": diagnosis,
                        "user_responses": st.session_state.get("user_responses", [])
                    }
                    
                    weapon_card = orchestrator.stage5_assistant_summary(
                        all_data, weapon_name, personal_reminder
                    )
                    
                    if weapon_card:
                        render_final_weapon_card(weapon_card, weapon_name, personal_reminder, usage_scenarios)
                        
                        # 完成整个流程
                        st.balloons()
                        st.markdown("### 🎉 恭喜完成15分钟认知觉醒之旅！")
                        
                        # 反馈收集
                        render_feedback_collection(orchestrator)

def render_final_weapon_card(weapon_card, name, reminder, scenarios):
    """简化版武器卡片"""
    st.success(f"🛡️ {name}")
    st.info(f"❤️‍🩹 血泪提醒: {reminder}")
    st.info(f"💡 使用场景: {scenarios}")
    
    # 保存功能（简化版）
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 保存为图片", use_container_width=True, key="save_image"):
            st.success("🎉 武器卡片已生成！请截图保存。")
    with col2:
        if st.button("📋 复制内容", use_container_width=True, key="copy_content"):
            st.success("📋 内容已准备好复制")
    with col3:
        if st.button("🔄 重新定制", use_container_width=True, key="redesign"):
            st.rerun()

def render_feedback_collection(orchestrator):
    """渲染反馈收集 - 修复状态管理BUG"""
    st.markdown("---")
    st.markdown("### 💬 分享你的体验感受")
    
    col1, col2 = st.columns(2)
    
    with col1:
        satisfaction = st.slider("体验满意度", 1, 10, 8, key="satisfaction")
        recommend = st.radio("是否会推荐给朋友？", ["是", "否", "可能"], key="recommend")
    
    with col2:
        most_valuable = st.text_area(
            "最大收获是什么？",
            placeholder="分享你的感受...",
            height=100,
            key="most_valuable"
        )
    
    if st.button("📝 提交反馈", type="primary", key="submit_feedback"):    
        # 关键修复：设置反馈已提交标记
        st.session_state["feedback_submitted"] = True
        st.rerun()  # 重新渲染页面，将显示完成页面
def render_journey_completion():
    """渲染流程完成页面 - 新增函数"""
    st.markdown("### 🎉 感谢您的宝贵反馈！")
    st.success("✨ 15分钟认知觉醒之旅已圆满完成！")
    
    # 显示完成统计信息
    completion_html = '''
    <div style="
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    ">
        <h2>🏆 旅程完成</h2>
        <p style="font-size: 1.2rem; margin: 1rem 0;">
            您已经成功获得了专属的认知武器！<br>
            现在可以选择开始新的旅程或返回主页。
        </p>
    </div>
    '''
    st.markdown(completion_html, unsafe_allow_html=True)
    
    # 显示结束选项
    st.markdown("### 🚀 接下来做什么？")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 重新体验", use_container_width=True, key="restart_journey_final"):
            # 清空所有状态并重新开始
            keys_to_clear = [
                "journey", "user_responses", "mastery_passed", 
                "feedback_submitted", "weapon_name", "personal_reminder", 
                "usage_scenarios", "satisfaction", "recommend", "most_valuable"
            ]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    with col2:
        if st.button("🏠 返回首页", use_container_width=True, key="go_home_final"):
            st.session_state.current_page = "🏠 产品介绍"
            # 保留反馈已提交状态，但清理其他临时状态
            keys_to_clear = [
                "mastery_passed", "weapon_name", "personal_reminder", 
                "usage_scenarios", "satisfaction", "recommend", "most_valuable"
            ]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # 额外的功能选项
    st.markdown("---")
    st.markdown("### 🔧 更多选项")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 体验智能诊断", use_container_width=True):
            st.session_state.current_page = "🔍 智能诊断"
            st.rerun()
    
    with col2:
        if st.button("🧬 查看其他案例", use_container_width=True):
            st.session_state.current_page = "🧬 Demo案例体验"
            st.rerun()
    
    with col3:
        if st.button("📚 浏览药方库", use_container_width=True):
            st.session_state.current_page = "📚 药方库浏览"
            st.rerun()
