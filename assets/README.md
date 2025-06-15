# 🎨 认知黑匣子 - 资源文件指导

## 📁 文件结构
```
assets/
├── css/
│   ├── main.css              ✅ 已创建
│   └── components.css        📝 可选
├── images/
│   ├── logo.png             📝 需要生成
│   ├── logo.svg             ✅ 已创建 (见icons.svg)
│   ├── favicon.ico          📝 需要生成
│   ├── brain-icon.png       📝 需要生成
│   └── icons.svg            ✅ 已创建
└── README.md                ✅ 本文件
```

## 🎯 Logo设计规范

### 主Logo (logo.png / logo.svg)
- **设计概念**: 大脑🧠 + 黑匣子📦 = 认知黑匣子
- **主色调**: 
  - 主色: #667eea (蓝紫色)
  - 辅色: #764ba2 (深紫色)
  - 渐变: 从#667eea到#764ba2
- **尺寸要求**:
  - PNG: 512x512px (高清)
  - SVG: 可缩放矢量
  - Favicon: 32x32px, 16x16px

### 设计元素
1. **外框**: 圆角矩形，代表"黑匣子"
2. **内部**: 大脑图形，有褶皱细节
3. **指示灯**: 右上角红绿指示灯，显示系统状态
4. **文字**: "认知黑匣子"或"Cognitive BlackBox"

## 🛠️ 生成方法

### 方法1: 使用AI图像生成工具

#### 推荐工具:
- **Midjourney**: 最高质量
- **DALL-E 3**: OpenAI官方
- **Stable Diffusion**: 开源免费

#### 提示词模板:
```
A modern, minimalist logo for "Cognitive BlackBox", featuring a brain inside a rounded rectangle box, gradient colors from #667eea to #764ba2, clean vector style, transparent background, professional tech startup branding

认知黑匣子Logo，大脑图形融入黑匣子概念，现代简约风格，蓝紫色渐变，透明背景，科技感
```

### 方法2: 使用在线Logo生成器

#### 推荐平台:
1. **Canva** (https://canva.com)
   - 搜索"brain tech logo"
   - 自定义颜色为#667eea
   - 添加文字"认知黑匣子"

2. **Logo Maker** (https://logomaker.com)
   - 选择科技/AI类别
   - 搜索大脑图标
   - 组合矩形框架

3. **Figma** (免费)
   - 使用矢量工具绘制
   - 导出为PNG和SVG

### 方法3: 使用现有SVG

我已经在 `icons.svg` 中创建了基础的Logo SVG代码，你可以：

1. **直接使用SVG版本**
   ```html
   <svg width="100" height="100">
     <use href="assets/images/icons.svg#brain-box-logo"></use>
   </svg>
   ```

2. **转换为PNG**
   - 在浏览器中打开SVG
   - 使用截图工具保存为PNG
   - 或使用在线转换器: https://convertio.co/svg-png/

## 📄 Favicon生成

### 自动生成方法:
1. **访问Favicon生成器**
   ```
   https://favicon.io/favicon-generator/
   或
   https://realfavicongenerator.net/
   ```

2. **上传Logo图像**
   - 使用生成的logo.png
   - 选择32x32和16x16尺寸

3. **下载favicon.ico**
   - 保存到 `assets/images/favicon.ico`

### 手动生成方法:
```html
<!-- 在app.py中使用HTML添加favicon -->
st.set_page_config(
    page_title="认知黑匣子",
    page_icon="🧠",  # 临时使用emoji
    layout="wide"
)
```

## 🎨 可选的额外图像

### 1. 背景图片 (prescription-bg.jpg)
- **用途**: 药方卡片背景
- **规格**: 1920x1080px, 低饱和度
- **风格**: 抽象几何、神经网络纹理

### 2. 功能图标 (brain-icon.png)
- **用途**: 各种功能按钮图标
- **规格**: 64x64px, 透明背景
- **数量**: 可以创建一套，包括诊断、测试、药方等

### 3. Demo案例头像
- **用途**: Demo案例中的人物头像
- **规格**: 128x128px, 圆形头像
- **内容**: 张铭、李华、陈佳、王磊的卡通头像

## 🔗 在Streamlit中使用图像

### 1. 基础用法
```python
import streamlit as st

# 显示Logo
st.image("assets/images/logo.png", width=200)

# 在侧边栏显示
with st.sidebar:
    st.image("assets/images/logo.png", width=150)
```

### 2. HTML嵌入 (推荐)
```python
# 使用HTML和CSS控制
st.markdown("""
<div style="text-align: center;">
    <img src="assets/images/logo.png" width="200" alt="认知黑匣子"/>
</div>
""", unsafe_allow_html=True)
```

### 3. SVG直接嵌入
```python
# 读取SVG并嵌入
with open("assets/images/icons.svg", "r") as f:
    svg_content = f.read()

st.markdown(f"""
<div style="text-align: center;">
    {svg_content}
    <svg width="100" height="100">
        <use href="#brain-box-logo"></use>
    </svg>
</div>
""", unsafe_allow_html=True)
```

## 📊 品牌色彩系统

### 主色调
```css
--primary-color: #667eea;      /* 主品牌色 */
--primary-dark: #764ba2;       /* 深色变体 */
--secondary-color: #f093fb;    /* 辅助色 */
```

### 功能色彩
```css
--success-color: #10b981;      /* 成功/通过 */
--warning-color: #f59e0b;      /* 警告/注意 */
--error-color: #ef4444;        /* 错误/失败 */
--info-color: #3b82f6;         /* 信息/提示 */
```

### 药方分类色彩
```css
--basics-color: #2563eb;       /* 基础药方 */
--advanced-color: #7c3aed;     /* 高级药方 */
--team-color: #dc2626;         /* 团队药方 */
```

## ⚡ 快速开始指南

如果你想快速部署，暂时跳过图像生成：

1. **使用Emoji作为临时图标**
   ```python
   st.set_page_config(page_icon="🧠")
   ```

2. **使用已有的SVG图标**
   - 直接使用icons.svg中的矢量图标

3. **部署后再优化**
   - 先确保功能正常运行
   - 后续补充高质量的图像资源

## 🎯 优先级建议

### 高优先级 (立即需要)
- [x] CSS样式文件 (已完成)
- [x] SVG图标集 (已完成)
- [ ] favicon.ico (5分钟可完成)

### 中优先级 (部署后优化)
- [ ] 主Logo PNG版本
- [ ] 背景图片
- [ ] Demo案例头像

### 低优先级 (长期优化)
- [ ] 动画效果
- [ ] 多语言图标
- [ ] 主题变体

---

**🎨 记住：好的设计能提升用户体验，但核心功能更重要！**

先确保Kevin案例测试通过，再慢慢完善视觉设计。
