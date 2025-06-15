"""
认知黑匣子 Streamlit 主应用 - 修复版本
修复了按钮回调和页面导航问题
"""
import streamlit as st
import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

# 导入现有模块
from config import *
from utils.diagnosis_engine import DiagnosisEngine
from utils.prescription_loader import PrescriptionLoader
from utils.demo_case_manager import DemoCaseManager
from utils.streamlit_components import *

# 导入新增的15分钟流程模块
from utils.journey_components import render_15min_journey

# 页面配置
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS（保持现有样式并添加新样式）
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 2rem;
}

.prescription-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-left: 4px solid #667eea;
    margin-bottom: 1rem;
}

.diagnosis-result {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #28a745;
    margin: 1rem 0;
}

.demo-case-card {
    background: #fff3cd;
    padding: 1rem;
    border-radius: 8px;
    border-left: 3px solid #ffc107;
    margin: 0.5rem 0;
    cursor: pointer;
}

.kevin-special {
    background: #f8d7da;
    border-left-color: #dc3545;
}

/* 新增15分钟流程专用样式 */
.journey-highlight {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.journey-nav-card {
    background: #f8f9fa;
    border: 2px solid #667eea;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    text-align: center;
    transition: transform 0.3s ease;
}

.journey-nav-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}
</style>
""", unsafe_allow_html=True)

# 修复：添加回调函数
def start_journey_callback():
    """启动15分钟觉醒之旅的回调函数"""
    # 初始化journey状态
    if "journey" not in st.session_state:
        st.session_state.journey = {
            "stage": 0,
            "demo_mode": True,
            "demo_case_id": "case_02_team_conflict",
            "start_time": None,
            "user_responses": [],
            "ai_responses": {},
            "stage_completion": [False] * 6,
        }
    
    # 重置相关状态
    st.session_state.user_responses = []
    if "mastery_passed" in st.session_state:
        del st.session_state["mastery_passed"]
    
    # 重置journey阶段为0（开场）
    st.session_state.journey["stage"] = 0
    st.session_state.journey["user_responses"] = []
    st.session_state.journey["ai_responses"] = {}
    
    # 设置当前页面为15分钟之旅
    st.session_state.current_page = "🎭 15分钟觉醒之旅"

def set_page_callback(page_name):
    """设置页面的回调函数"""
    st.session_state.current_page = page_name

def main():
    """主应用函数"""
    
    # 初始化组件（保持现有逻辑）
    if 'diagnosis_engine' not in st.session_state:
        st.session_state.diagnosis_engine = DiagnosisEngine()
        st.session_state.prescription_loader = PrescriptionLoader()
        st.session_state.demo_manager = DemoCaseManager()
    
    # 初始化页面状态
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 产品介绍"
    
    # 主标题
    st.markdown(f"""
    <div class="main-header">
        <h1>{APP_TITLE}</h1>
        <p>{APP_SUBTITLE}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏导航（新增15分钟流程选项）
    with st.sidebar:
        st.markdown("### 🎯 功能导航")
        
        # 添加15分钟流程的突出显示
        st.markdown("""
        <div class="journey-highlight">
            <h4 style="margin: 0;">🌟 核心体验</h4>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">15分钟认知觉醒之旅</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 修复：使用session_state中的current_page
        page_options = [
            "🏠 产品介绍",
            "🎭 15分钟觉醒之旅",  # 新增核心功能
            "🔍 智能诊断", 
            "🧬 Demo案例体验",
            "📚 药方库浏览", 
            "🧪 Kevin案例测试"
        ]
        
        # 确保当前页面在选项列表中
        if st.session_state.current_page not in page_options:
            st.session_state.current_page = "🏠 产品介绍"
        
        page = st.selectbox(
            "选择功能",
            page_options,
            index=page_options.index(st.session_state.current_page) if st.session_state.current_page in page_options else 0,
            key="page_selector"
        )
        
        # 更新当前页面状态
        if page != st.session_state.current_page:
            st.session_state.current_page = page
            st.rerun()
        
        # 添加流程说明
        if page == "🎭 15分钟觉醒之旅":
            st.markdown("""
            ---
            ### 📋 流程说明
            
            **🎯 阶段1：情境聚焦** (4分钟)  
            主持人温和引导
            
            **💼 阶段2：现实击穿** (3分钟)  
            投资人犀利质询
            
            **🧠 阶段3：框架重构** (4分钟)  
            导师智慧传授
            
            **🤝 阶段4：能力内化** (3分钟)  
            助理温暖总结
            
            **总计: 12-15分钟**
            """)
    
    # 主内容区域路由
    if page == "🏠 产品介绍":
        render_home_page()
    elif page == "🎭 15分钟觉醒之旅":
        render_15min_journey()  # 新增的核心功能
    elif page == "🔍 智能诊断":
        render_diagnosis_page()
    elif page == "🧬 Demo案例体验":
        render_demo_cases_page()
    elif page == "📚 药方库浏览":
        render_prescription_library_page()
    elif page == "🧪 Kevin案例测试":
        render_kevin_test_page()

def render_home_page():
    """渲染产品介绍主页 - 修复按钮回调"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🎯 产品介绍")
        st.markdown("""
        **认知黑匣子**是一个AI驱动的认知升级产品，旨在帮助创业者在15分钟内实现认知觉醒。
        
        ### 🌟 核心价值
        - **快速诊断**：AI精准识别认知陷阱
        - **深度冲击**：四阶段情感体验设计
        - **实用框架**：获得可复用的决策武器
        - **个性化**：基于真实案例的定制体验
        
        ### 🚀 立即体验
        点击右侧的"**15分钟觉醒之旅**"开始你的认知升级！
        """)
    
    with col2:
        # 核心体验入口卡片
        st.markdown("""
        <div class="journey-nav-card">
            <h3 style="color: #667eea; margin-top: 0;">🎭 15分钟觉醒之旅</h3>
            <p>体验完整的认知重构流程</p>
            <p style="font-size: 0.9rem; color: #666;">
                四个AI角色 • 深度引导<br>
                情境聚焦 → 现实击穿 → 框架重构 → 能力内化
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 修复：添加正确的回调函数
        if st.button("🚀 开始15分钟之旅", type="primary", use_container_width=True, 
                    on_click=start_journey_callback):
            st.rerun()
        
        # 其他功能快速入口
        st.markdown("### 🔧 其他功能")
        
        # 修复：添加回调函数
        if st.button("🔍 智能诊断", use_container_width=True):
            st.session_state.current_page = "🔍 智能诊断"
            st.rerun()
            
        if st.button("🧬 Demo案例", use_container_width=True):
            st.session_state.current_page = "🧬 Demo案例体验"
            st.rerun()

# 保持现有的页面渲染函数
def render_diagnosis_page():
    """渲染诊断页面（保持现有逻辑）"""
    st.markdown("## 🔍 智能诊断")
    st.markdown("### 描述你遇到的创业困境...")
    
    # 用户输入
    user_input = st.text_area(
        "请详细描述你的问题（建议150字以上）：",
        height=200,
        placeholder="例如：我和我的技术合伙人在产品方向上产生了严重分歧，我认为应该专注B端企业客户，但他坚持要做C端。我们为此争论了6个月，项目基本停滞..."
    )
    
    # 字数统计
    char_count = len(user_input)
    if char_count < MIN_INPUT_LENGTH:
        st.warning(f"建议输入至少{MIN_INPUT_LENGTH}字，当前{char_count}字")
    else:
        st.success(f"输入长度合适：{char_count}字")
    
    # 诊断按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔬 开始诊断", type="primary", use_container_width=True):
            if char_count >= MIN_INPUT_LENGTH:
                diagnose_user_input(user_input)
            else:
                st.error("请输入更详细的描述")

def diagnose_user_input(user_input):
    """执行诊断（保持现有逻辑）"""
    with st.spinner("AI正在分析你的认知模式..."):
        try:
            # 调用诊断引擎
            diagnosis_result = st.session_state.diagnosis_engine.diagnose(user_input)
            
            # 显示诊断结果
            if diagnosis_result:
                render_diagnosis_result(diagnosis_result)
                
                # 引导用户体验15分钟流程
                st.markdown("---")
                st.markdown("### 🎯 深度体验推荐")
                st.info("💡 想要获得完整的认知重构体验？试试我们的15分钟觉醒之旅！")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    # 修复：添加回调函数
                    if st.button("🎭 体验15分钟觉醒之旅", type="secondary", use_container_width=True,
                                on_click=start_journey_callback):
                        st.rerun()
            else:
                st.error("诊断失败，请重新尝试")
                
        except Exception as e:
            st.error(f"诊断过程中出现错误：{str(e)}")

def render_diagnosis_result(result):
    """渲染诊断结果（保持现有逻辑）"""
    st.markdown("## 🎯 诊断结果")
    
    # 主要药方
    primary = result.get('primary_prescription', {})
    
    # 结果卡片
    st.markdown(f"""
    <div class="diagnosis-result">
        <h3>💊 {primary.get('display_name', '未知药方')}</h3>
        <p><strong>📊 置信度：</strong>{primary.get('confidence', 0):.1%}</p>
        <p><strong>🚨 影响评级：</strong>{'█' * primary.get('impact_score', 0)}{'░' * (10 - primary.get('impact_score', 0))} ({primary.get('impact_score', 0)}/10)</p>
        <p><strong>💡 认知突破点：</strong>{result.get('cognitive_breakthrough', '暂无')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 查看完整药方按钮
    if st.button("📖 查看完整药方内容"):
        render_prescription_detail(primary.get('id'))

def render_demo_cases_page():
    """渲染Demo案例页面（保持现有逻辑）"""
    st.markdown("## 🧬 Demo案例体验")
    st.markdown("### 通过真实案例体验产品价值")
    
    # 添加15分钟流程推荐
    st.markdown("""
    <div class="journey-highlight">
        <h4 style="margin: 0;">💡 推荐体验</h4>
        <p style="margin: 0.5rem 0 0 0;">想要完整的四阶段体验？试试15分钟觉醒之旅！</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 加载案例
    cases = st.session_state.demo_manager.get_all_cases()
    
    for case_id, case_data in cases.items():
        meta = case_data.get('case_meta', {})
        
        # 特殊标记Kevin案例
        card_class = "demo-case-card kevin-special" if meta.get('kevin_case_solution') else "demo-case-card"
        
        st.markdown(f"""
        <div class="{card_class}">
            <h4>{meta.get('case_name', '未知案例')}</h4>
            <p><strong>主角：</strong>{meta.get('protagonist', '未知')}</p>
            <p><strong>陷阱类型：</strong>{meta.get('target_trap', '未知')}</p>
            <p><strong>认知冲击：</strong>{meta.get('cognitive_impact_score', 0)}/10</p>
            {'<p><strong>🔥 Kevin案例专用解决方案</strong></p>' if meta.get('kevin_case_solution') else ''}
        </div>
        """, unsafe_allow_html=True)
        
        # 修复：为体验按钮添加更好的处理
        if st.button(f"体验案例：{meta.get('protagonist', '未知')}", key=f"demo_{case_id}"):
            if case_id == "case_02_team_conflict":  # Kevin案例
                # 直接启动15分钟之旅
                start_journey_callback()
                st.rerun()
            else:
                experience_demo_case(case_id, case_data)

def render_prescription_library_page():
    """渲染药方库浏览页面（保持现有逻辑）"""
    st.markdown("## 📚 药方库浏览")
    
    # 获取所有药方
    prescriptions = st.session_state.prescription_loader.get_all_prescriptions()
    
    # 显示药方统计
    st.markdown(f"### 📊 药方总览 (共{len(prescriptions)}个)")
    
    # 分类显示
    categories = {}
    for pid, prescription in prescriptions.items():
        category = prescription.get('category', '未分类')
        if category not in categories:
            categories[category] = []
        categories[category].append((pid, prescription))
    
    for category, items in categories.items():
        st.markdown(f"#### {category} ({len(items)}个)")
        
        for pid, prescription in items:
            with st.expander(f"💊 {prescription.get('display_name', pid)}"):
                st.markdown(f"**影响评级：** {prescription.get('impact_score', 5)}/10")
                st.markdown(f"**标签：** {', '.join(prescription.get('tags', []))}")
                
                symptoms = prescription.get('symptoms', [])
                if symptoms:
                    st.markdown("**主要症状：**")
                    for symptom in symptoms[:3]:
                        st.markdown(f"• {symptom}")

def render_kevin_test_page():
    """渲染Kevin案例测试页面 - 修复按钮回调"""
    st.markdown("## 🧪 Kevin案例专项测试")
    st.markdown("### 验证系统对合伙人冲突问题的处理能力")
    
    # Kevin案例测试输入
    kevin_input = """我和我的技术合伙人在产品方向上产生了严重分歧，我认为应该专注B端企业客户，做项目管理SaaS，但他坚持要做C端的个人时间管理App。我们为此争论了6个月，项目基本停滞。最让我困惑的是，我明明有更多的市场调研数据支持B端方向，但他就是说服不了。现在我们的关系很紧张，投资人也开始质疑我们团队的执行力。"""
    
    st.text_area("Kevin案例测试输入：", value=kevin_input, height=150, disabled=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ 期望结果")
        st.markdown("""
        - **药方ID**: P20
        - **药方名称**: 创始人冲突认知解码器
        - **置信度**: > 90%
        - **类别**: 团队管理药方
        - **关键词匹配**: 合伙人、冲突、分歧
        """)
    
    with col2:
        st.markdown("### 🎭 完整流程测试")
        st.info("💡 想要测试Kevin案例的完整15分钟流程？")
        
        # 修复：添加正确的回调函数
        if st.button("🎭 Kevin案例15分钟流程", type="secondary", use_container_width=True,
                    on_click=start_journey_callback):
            st.rerun()
    
    if st.button("🧪 执行Kevin案例测试", type="primary"):
        test_kevin_case(kevin_input)

def test_kevin_case(test_input):
    """执行Kevin案例测试（保持现有逻辑）"""
    with st.spinner("正在测试Kevin案例识别..."):
        try:
            result = st.session_state.diagnosis_engine.diagnose(test_input)
            
            # 验证结果
            if result:
                primary = result.get('primary_prescription', {})
                prescription_id = primary.get('id', '')
                confidence = primary.get('confidence', 0)
                
                st.markdown("### 🔬 实际测试结果")
                
                if prescription_id == 'P20' and confidence > 0.9:
                    st.success("✅ Kevin案例测试通过！")
                    st.balloons()
                else:
                    st.error("❌ Kevin案例测试失败！")
                
                # 显示详细结果
                st.json({
                    "prescription_id": prescription_id,
                    "prescription_name": primary.get('display_name', ''),
                    "confidence": f"{confidence:.1%}",
                    "expected": "P20 (创始人冲突认知解码器)",
                    "test_passed": prescription_id == 'P20' and confidence > 0.9
                })
            else:
                st.error("测试失败：无法获取诊断结果")
                
        except Exception as e:
            st.error(f"测试过程中出现错误：{str(e)}")

# 其他辅助函数（保持现有逻辑）
def render_prescription_detail(prescription_id):
    """渲染药方详情"""
    # 实现药方详情展示
    pass

def experience_demo_case(case_id, case_data):
    """体验Demo案例"""
    # 实现Demo案例体验流程
    pass

if __name__ == "__main__":
    main()
