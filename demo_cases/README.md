# 🎭 黄金Demo案例库

## 📁 文件位置
```
cognitive-blackbox/demo_cases/
├── README.md                       # 本说明文件
├── cases_index.json                # 案例库索引
├── case_01_tech_supremacy.json     # 技术至上偏见案例
├── case_02_team_conflict.json      # 团队冲突案例 (Kevin专用)
├── case_03_confirmation_bias.json  # 确认偏见案例
└── case_04_execution_gap.json      # 执行力gap案例
```

## 🎯 案例库设计目的

### 1. **降低用户体验门槛**
- 用户首次接触产品时，可能不愿意输入真实问题
- 通过Demo案例让用户先体验产品价值
- 建立信任后再引导用户投入真实问题

### 2. **Kevin案例验证工具** 
- case_02_team_conflict 专门解决Kevin类型问题
- 验证系统对"合伙人冲突"问题的诊断和处理能力
- 产品商业价值验证的试金石

### 3. **认知陷阱类型覆盖**
- **技术陷阱**：过度关注技术优势，忽视用户价值
- **团队陷阱**：误解团队协作的本质规律
- **市场陷阱**：确认偏见导致的市场判断错误
- **执行陷阱**：知行分离的深层心理机制

## 📊 案例质量标准

### ✅ **真实性**
- 每个案例都有具体的公司背景
- 明确的时间线和失败节点
- 真实可信的人物设定

### ✅ **代表性**
- case_01: 90%技术背景创业者的通病
- case_02: 合伙人冲突的经典模式  
- case_03: 数据驱动决策者的盲区
- case_04: 学习型创业者的执行困境

### ✅ **认知冲击力**
- 每个案例都有明确的"认知突破点"
- 设计"我原来想错了"的顿悟时刻
- 从具体问题升维到思维模式问题

## 🔄 与提示词系统的集成

### P-H-01 Demo引导
```python
# 触发条件
if len(user_input) < 50 or is_generic_question(user_input):
    return demo_guidance_with_case()
```

### P-H-02 诊断引擎
```python
# 诊断参考
case_patterns = load_demo_cases()
diagnosis_confidence += case_pattern_matching(user_input, case_patterns)
```

### P-I-01 投资人质询
```python
# 失败案例类比
similar_case = find_most_similar_case(diagnosed_trap)
return grand_failure_analogy(similar_case)
```

## 🚨 Kevin案例特别说明

### case_02_team_conflict.json
**专用目的**：验证系统能否正确处理"合伙人冲突"问题

**关键特征**：
- 包含"合伙人"、"团队"、"沟通"、"信任"等关键词
- 表面问题：产品方向分歧
- 深层问题：认知模式不兼容
- 预期诊断：团队认知偏差：镜子陷阱

**验证标准**：
- ✅ 系统能识别为团队问题，而非产品问题
- ✅ 诊断出"镜子陷阱"认知偏见
- ✅ 提供团队协作框架，而非产品验证方法

## 🛠️ 技术实现要求

### 案例加载
```python
import json

def load_demo_case(case_id):
    with open(f'demo_cases/{case_id}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_random_case():
    cases = ['case_01', 'case_02', 'case_03', 'case_04']
    return random.choice(cases)
```

### 案例匹配
```python
def match_case_by_keywords(user_input):
    keyword_patterns = {
        'case_01': ['技术', '算法', '产品', '用户不买账'],
        'case_02': ['合伙人', '团队', '分歧', '沟通'],
        'case_03': ['调研', '数据', '市场', '用户反馈'],
        'case_04': ['计划', '执行', '拖延', '方法']
    }
    return best_matching_case(user_input, keyword_patterns)
```

## 📈 成功指标

### Demo阶段
- **体验完成率** > 80%
- **转化为正式使用率** > 30%  
- **案例相关性评分** > 4.0/5.0

### Kevin案例验证
- **诊断准确率** = 100% (必须正确)
- **用户认知冲击感** > 4.5/5.0
- **解决方案相关性** > 4.0/5.0

## 🔄 迭代计划

### 版本1.0 (当前)
- ✅ 4个核心案例完成
- ✅ JSON格式标准化
- ✅ Kevin案例专用解决方案

### 版本1.1 (计划)
- [ ] 增加行业细分案例（SaaS、电商、教育等）
- [ ] 案例难度分级（初级、中级、高级）
- [ ] 多语言支持

### 版本2.0 (愿景)
- [ ] 动态案例生成（基于用户画像）
- [ ] 案例个性化推荐
- [ ] 用户贡献案例机制

---

*黄金Demo案例库 - 让每个创业者都能找到自己的影子* 🎭
