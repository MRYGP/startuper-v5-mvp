"""
Streamlit自定义组件 - UI组件和样式
"""
import streamlit as st
from typing import Dict, List, Optional
import json

def render_prescription_card(prescription: Dict, show_details: bool = False):
    """渲染药方卡片"""
    prescription_id = prescription.get('id', '')
    display_name = prescription.get('display_name', '未知药方')
    impact_score = prescription.get('impact_score', 5)
    category = prescription.get('category', '')
    
    # 根据类别选择颜色
    category_colors = {
        '基础必需品药方': '#2563eb',
        '独特深度药方': '#7c3aed',
        '团队管理药方': '#dc2626',
        'basics': '#2563eb',
        'advanced': '#7c3aed',
        'team': '#dc2626'
    }
    
    color = category_colors.get(category, '#6b7280')
    
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid {color};
        margin-bottom: 1rem;
    ">
        <h3 style="color: {color}; margin-bottom: 0.5rem;">💊 {display_name}</h3>
        <p><strong>📊 影响评级：</strong>{'█' * impact_score}{'░' * (10 - impact_score)} ({impact_score}/10)</p>
        <p><strong>🏷️ 类别：</strong>{category}</p>
        <p><strong>🆔 ID：</strong>{prescription_id}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if show_details:
        symptoms = prescription.get('symptoms', [])
        if symptoms:
            st.markdown("**🎯 主要症状：**")
            for symptom in symptoms[:3]:
                st.markdown(f"• {symptom}")

def render_diagnosis_confidence(confidence: float):
    """渲染诊断置信度"""
    confidence_pct = confidence * 100
    
    if confidence >= 0.9:
        color = "#28a745"  # 高置信度 - 绿色
        label = "极高置信度"
        emoji = "🎯"
    elif confidence >= 0.7:
        color = "#ffc107"  # 中等置信度 - 黄色
        label = "较高置信度"
        emoji = "✅"
    elif confidence >= 0.5:
        color = "#fd7e14"  # 低置信度 - 橙色
        label = "中等置信度"
        emoji = "⚠️"
    else:
        color = "#dc3545"  # 很低置信度 - 红色
        label = "低置信度"
        emoji = "❌"
    
    st.markdown(f"""
    <div style="
        background: {color}20;
        border: 1px solid {color};
        border-radius: 5px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
    ">
        <strong style="color: {color};">{emoji} 诊断置信度: {confidence_pct:.1f}% ({label})</strong>
    </div>
    """, unsafe_allow_html=True)

def render_impact_score_visual(impact_score: int):
    """渲染影响评级可视化"""
    colors = {
        'high': '#dc2626',    # 红色 (9-10分)
        'medium': '#ea580c',  # 橙色 (7-8分)
        'low': '#ca8a04',     # 黄色 (5-6分)
        'minimal': '#16a34a'  # 绿色 (1-4分)
    }
    
    if impact_score >= 9:
        color = colors['high']
        level = "🚨 高危"
        description = "严重影响创业成功率"
    elif impact_score >= 7:
        color = colors['medium']
        level = "⚠️ 警告"
        description = "明显影响项目进展"
    elif impact_score >= 5:
        color = colors['low']
        level = "💡 注意"
        description = "需要关注和改进"
    else:
        color = colors['minimal']
        level = "✅ 轻微"
        description = "影响相对较小"
    
    # 绘制条形图
    filled_bars = "█" * impact_score
    empty_bars = "░" * (10 - impact_score)
    
    st.markdown(f"""
    <div style="
        background: {color}20;
        border-left: 4px solid {color};
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    ">
        <h4 style="color: {color}; margin: 0 0 0.5rem 0;">{level}</h4>
        <div style="
            font-family: monospace;
            font-size: 1.2rem;
            color: {color};
            letter-spacing: 2px;
        ">
            {filled_bars}<span style="color: #ccc;">{empty_bars}</span>
        </div>
        <p style="margin: 0.5rem 0 0 0; color: {color};">
            <strong>影响评级: {impact_score}/10</strong>
        </p>
        <p style="margin: 0.25rem 0 0 0; color: #666; font-size: 0.9rem;">
            {description}
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_kevin_case_special_marker():
    """渲染Kevin案例特殊标记"""
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #ff6b6b, #feca57);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        animation: pulse 2s infinite;
    ">
        🔥 Kevin案例专用解决方案 🔥
        <br>
        <small>专门处理合伙人冲突认知陷阱</small>
    </div>
    <style>
    @keyframes pulse {
        0% { box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        50% { box-shadow: 0 6px 12px rgba(0,0,0,0.3); }
        100% { box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
    }
    </style>
    """, unsafe_allow_html=True)

def render_demo_case_preview(case_data: Dict, case_id: str = ""):
    """渲染Demo案例预览"""
    meta = case_data.get('case_meta', {})
    character = case_data.get('character_profile', {})
    
    case_name = meta.get('case_name', '未知案例')
    protagonist = character.get('name', meta.get('protagonist', '未知主角'))
    background = character.get('background', '未知背景')
    pain_point = character.get('pain_point', '未知痛点')
    problem_summary = case_data.get('problem_summary', '未知问题摘要')
    
    # Kevin案例特殊样式
    if meta.get('kevin_case_solution'):
        border_color = "#dc3545"
        bg_color = "#f8d7da"
        special_marker = "🔥 Kevin案例专用"
        special_class = "kevin-special"
    else:
        border_color = "#ffc107"
        bg_color = "#fff3cd"
        special_marker = ""
        special_class = ""
    
    st.markdown(f"""
    <div class="demo-case-card {special_class}" style="
        background: {bg_color};
        border-left: 4px solid {border_color};
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        cursor: pointer;
        transition: transform 0.2s;
    " onmouseover="this.style.transform='translateY(-2px)'" 
       onmouseout="this.style.transform='translateY(0)'">
        <h4 style="color: {border_color}; margin-bottom: 0.5rem;">
            {case_name} {special_marker}
        </h4>
        <p><strong>🎭 主角：</strong>{protagonist}</p>
        <p><strong>🏢 背景：</strong>{background}</p>
        <p><strong>💔 核心困境：</strong>{problem_summary}</p>
        <p><strong>🎯 目标陷阱：</strong>{meta.get('target_trap', '未知')}</p>
        <p><strong>💥 认知冲击：</strong>{meta.get('cognitive_impact_score', 0)}/10</p>
    </div>
    """, unsafe_allow_html=True)
    
    return st.button(f"体验案例：{protagonist}", key=f"demo_{case_id}", use_container_width=True)

def render_progress_bar(current_step: int, total_steps: int, time_remaining: int):
    """渲染15分钟流程进度条"""
    progress = current_step / total_steps
    progress_pct = int(progress * 100)
    
    # 时间格式化
    minutes = time_remaining // 60
    seconds = time_remaining % 60
    
    st.markdown(f"""
    <div style="
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        ">
            <span><strong>🛠️ 15分钟认知重构 - 第{current_step}/{total_steps}步</strong></span>
            <span>⏰ 剩余时间: {minutes:02d}:{seconds:02d}</span>
        </div>
        <div style="
            background: #e9ecef;
            border-radius: 5px;
            height: 8px;
            overflow: hidden;
        ">
            <div style="
                background: linear-gradient(90deg, #667eea, #764ba2);
                height: 100%;
                width: {progress_pct}%;
                transition: width 0.3s ease;
            "></div>
        </div>
        <div style="
            text-align: center;
            margin-top: 0.5rem;
            font-size: 0.9rem;
            color: #6c757d;
        ">
            {progress_pct}% 完成
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_diagnosis_result_card(result: Dict):
    """渲染诊断结果卡片"""
    primary = result.get('primary_prescription', {})
    prescription_name = primary.get('display_name', '未知药方')
    confidence = primary.get('confidence', 0)
    impact_score = primary.get('impact_score', 5)
    cognitive_breakthrough = result.get('cognitive_breakthrough', '未知认知突破')
    matched_symptoms = result.get('matched_symptoms', [])
    
    st.markdown(f"""
    <div class="diagnosis-result" style="
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <h3 style="color: #28a745; margin-bottom: 1rem;">🎯 诊断结果</h3>
        <h2 style="color: #333; margin-bottom: 0.5rem;">💊 {prescription_name}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # 置信度显示
    render_diagnosis_confidence(confidence)
    
    # 影响评级显示
    render_impact_score_visual(impact_score)
    
    # 匹配症状
    if matched_symptoms:
        st.markdown("### 📝 识别到的核心症状：")
        for symptom in matched_symptoms:
            st.markdown(f"• {symptom}")
    
    # 认知突破点
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
    ">
        <h4 style="margin: 0 0 0.5rem 0;">💡 认知突破点</h4>
        <p style="margin: 0; font-size: 1.1rem; font-weight: 500;">
            "{cognitive_breakthrough}"
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_kevin_test_result(test_passed: bool, actual_result: Dict, expected_result: Dict):
    """渲染Kevin案例测试结果"""
    if test_passed:
        st.success("✅ Kevin案例测试通过！")
        st.balloons()
        
        st.markdown("""
        <div style="
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 1rem;
            margin: 1rem 0;
        ">
            <h4 style="color: #155724; margin: 0 0 0.5rem 0;">🎉 测试验证成功</h4>
            <p style="color: #155724; margin: 0;">
                系统正确识别了合伙人冲突问题，可以准确区分团队问题和产品问题！
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ Kevin案例测试失败！")
        
        st.markdown("""
        <div style="
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 1rem;
            margin: 1rem 0;
        ">
            <h4 style="color: #721c24; margin: 0 0 0.5rem 0;">⚠️ 测试失败</h4>
            <p style="color: #721c24; margin: 0;">
                系统未能正确识别Kevin案例，需要调整诊断规则！
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 详细结果对比
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔬 实际结果")
        st.json(actual_result)
    
    with col2:
        st.markdown("### ✅期望结果")
        st.json(expected_result)

def render_stats_dashboard(prescription_stats: Dict, case_stats: Dict):
    """渲染统计仪表板"""
    st.markdown("## 📊 知识库统计")
    
    # 药方统计
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📚 总药方数",
            value=prescription_stats.get('total', 0)
        )
    
    with col2:
        basics_count = prescription_stats.get('by_category', {}).get('基础必需品药方', 0)
        st.metric(
            label="🛡️ 基础药方",
            value=basics_count
        )
    
    with col3:
        advanced_count = prescription_stats.get('by_category', {}).get('独特深度药方', 0)
        st.metric(
            label="🧠 高级药方",
            value=advanced_count
        )
    
    with col4:
        team_count = prescription_stats.get('by_category', {}).get('团队管理药方', 0)
        st.metric(
            label="👥 团队药方",
            value=team_count
        )
    
    # Demo案例统计
    st.markdown("### 🎭 Demo案例统计")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🎯 总案例数",
            value=case_stats.get('total', 0)
        )
    
    with col2:
        kevin_count = case_stats.get('kevin_cases', 0)
        st.metric(
            label="🔥 Kevin专用案例",
            value=kevin_count
        )
    
    with col3:
        high_impact = case_stats.get('by_impact', {}).get('10分', 0)
        st.metric(
            label="💥 高冲击案例",
            value=high_impact
        )

def render_search_interface():
    """渲染搜索界面"""
    st.markdown("### 🔍 智能搜索")
    
    search_query = st.text_input(
        "搜索药方或案例",
        placeholder="输入关键词，如：团队、合伙人、技术、产品..."
    )
    
    search_type = st.selectbox(
        "搜索类型",
        ["全部", "药方库", "Demo案例"]
    )
    
    return search_query, search_type

def render_error_message(error_type: str, error_details: str = ""):
    """渲染错误信息"""
    error_configs = {
        "loading_error": {
            "emoji": "📁",
            "title": "文件加载错误",
            "color": "#dc3545"
        },
        "diagnosis_error": {
            "emoji": "🔬",
            "title": "诊断处理错误",
            "color": "#fd7e14"
        },
        "network_error": {
            "emoji": "🌐",
            "title": "网络连接错误",
            "color": "#dc3545"
        },
        "validation_error": {
            "emoji": "✅",
            "title": "数据验证错误",
            "color": "#ffc107"
        }
    }
    
    config = error_configs.get(error_type, {
        "emoji": "⚠️",
        "title": "未知错误",
        "color": "#6c757d"
    })
    
    st.markdown(f"""
    <div style="
        background: {config['color']}20;
        border: 1px solid {config['color']};
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    ">
        <h4 style="color: {config['color']}; margin: 0 0 0.5rem 0;">
            {config['emoji']} {config['title']}
        </h4>
        <p style="color: {config['color']}; margin: 0;">
            {error_details or "发生了意外错误，请稍后重试"}
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_loading_spinner(message: str = "处理中..."):
    """渲染加载动画"""
    with st.spinner(message):
        st.empty()

def apply_custom_css():
    """应用自定义CSS样式"""
    st.markdown("""
    <style>
    /* 主标题样式 */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    /* 药方卡片样式 */
    .prescription-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    
    .prescription-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* 诊断结果样式 */
    .diagnosis-result {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    /* Demo案例卡片样式 */
    .demo-case-card {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #ffc107;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .demo-case-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Kevin案例特殊样式 */
    .kevin-special {
        background: #f8d7da;
        border-left-color: #dc3545;
    }
    
    /* 隐藏Streamlit默认样式 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 自定义按钮样式 */
    .stButton > button {
        border-radius: 8px;
        border: none;
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
