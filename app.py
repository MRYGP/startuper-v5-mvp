"""
认知黑匣子 Streamlit 主应用
"""
import streamlit as st
import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

# 导入自定义模块
from config import *
from utils.diagnosis_engine import DiagnosisEngine
from utils.prescription_loader import PrescriptionLoader
from utils.demo_case_manager import DemoCaseManager
from utils.streamlit_components import *

# 页面配置
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
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
</style>
""", unsafe_allow_html=True)

def main():
    """主应用函数"""
    
    # 初始化组件
    if 'diagnosis_engine' not in st.session_state:
        st.session_state.diagnosis_engine = DiagnosisEngine()
        st.session_state.prescription_loader = PrescriptionLoader()
        st.session_state.demo_manager = DemoCaseManager()
    
    # 主标题
    st.markdown(f"""
    <div class="main-header">
        <h1>{APP_TITLE}</h1>
        <p>{APP_SUBTITLE}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.markdown("### 🎯 功能导航")
        
        page = st.selectbox(
            "选择功能",
            ["🔍 智能诊断", "🎭 Demo案例体验", "📚 药方库浏览", "🧪 Kevin案例测试"]
        )
    
    # 主内容区域
    if page == "🔍 智能诊断":
        render_diagnosis_page()
    elif page == "🎭 Demo案例体验":
        render_demo_cases_page()
    elif page == "📚 药方库浏览":
        render_prescription_library_page()
    elif page == "🧪 Kevin案例测试":
        render_kevin_test_page()

def render_diagnosis_page():
    """渲染诊断页面"""
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
    """执行诊断"""
    with st.spinner("AI正在分析你的认知模式..."):
        try:
            # 调用诊断引擎
            diagnosis_result = st.session_state.diagnosis_engine.diagnose(user_input)
            
            # 显示诊断结果
            if diagnosis_result:
                render_diagnosis_result(diagnosis_result)
            else:
                st.error("诊断失败，请重新尝试")
                
        except Exception as e:
            st.error(f"诊断过程中出现错误：{str(e)}")

def render_diagnosis_result(result):
    """渲染诊断结果"""
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
    """渲染Demo案例页面"""
    st.markdown("## 🎭 Demo案例体验")
    st.markdown("### 通过真实案例体验产品价值")
    
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
        
        if st.button(f"体验案例：{meta.get('protagonist', '未知')}", key=f"demo_{case_id}"):
            experience_demo_case(case_id, case_data)

def render_kevin_test_page():
    """渲染Kevin案例测试页面"""
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
        if st.button("🧪 执行Kevin案例测试", type="primary"):
            test_kevin_case(kevin_input)

def test_kevin_case(test_input):
    """执行Kevin案例测试"""
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

# 其他辅助函数...
def render_prescription_detail(prescription_id):
    """渲染药方详情"""
    # 实现药方详情展示
    pass

def experience_demo_case(case_id, case_data):
    """体验Demo案例"""
    # 实现Demo案例体验流程
    pass

def render_prescription_library_page():
    """渲染药方库浏览页面"""
    # 实现药方库浏览功能
    pass

if __name__ == "__main__":
    main()
