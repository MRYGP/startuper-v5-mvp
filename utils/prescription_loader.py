"""
药方加载器 - 加载和管理药方内容
"""
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
import streamlit as st

class PrescriptionLoader:
    def __init__(self):
        self.prescription_cache = {}
        self.base_dir = Path(__file__).parent.parent
        self.knowledge_base_dir = self.base_dir / "knowledge_base"
        self.load_all_prescriptions()
    
    def load_all_prescriptions(self):
        """加载所有药方"""
        try:
            for category_dir in ["01_basics", "02_advanced", "03_team"]:
                category_path = self.knowledge_base_dir / category_dir
                if category_path.exists():
                    for file_path in category_path.glob("*.md"):
                        prescription_id = self.extract_prescription_id(file_path.name)
                        if prescription_id:
                            prescription_data = self.load_prescription(file_path)
                            if prescription_data:
                                self.prescription_cache[prescription_id] = prescription_data
            
            print(f"加载了 {len(self.prescription_cache)} 个药方")
            
        except Exception as e:
            print(f"加载药方时出错: {e}")
            # 创建一些默认药方用于测试
            self.create_default_prescriptions()
    
    def create_default_prescriptions(self):
        """创建默认药方（用于测试）"""
        self.prescription_cache = {
            "P20": {
                "id": "P20",
                "display_name": "创始人冲突认知解码器",
                "category": "团队管理药方",
                "impact_score": 10,
                "tags": ["团队", "冲突", "合伙人", "认知偏差"],
                "symptoms": [
                    "合伙人之间存在严重分歧",
                    "决策陷入长期僵局",
                    "归因对方'不理解'或'不专业'"
                ],
                "related_prescriptions": ["P54", "P56", "P57"],
                "content": "# 💊 创始人冲突认知解码器\n\n## 🎯 主治认知陷阱\n**团队认知偏差：镜子陷阱**\n\n原来问题不在人，而在认知系统的兼容性..."
            },
            "P26": {
                "id": "P26",
                "display_name": "商业模式设计思维剂",
                "category": "独特深度药方",
                "impact_score": 10,
                "tags": ["商业模式", "产品思维", "价值主张"],
                "symptoms": [
                    "产品好但不知道怎么赚钱",
                    "商业模式不清晰",
                    "价值主张模糊"
                ],
                "related_prescriptions": ["P27", "P28", "P42"],
                "content": "# 💊 商业模式设计思维剂\n\n## 🎯 主治认知陷阱\n**产品中心主义偏见**\n\n原来好产品不等于好生意..."
            },
            "P27": {
                "id": "P27",
                "display_name": "心流状态设计剂",
                "category": "独特深度药方",
                "impact_score": 7,
                "tags": ["用户体验", "心流", "产品设计"],
                "symptoms": [
                    "用户容易分心或感到无聊",
                    "产品缺乏沉浸感",
                    "用户留存率低"
                ],
                "related_prescriptions": ["P29", "P54", "P55"],
                "content": "# 💊 心流状态设计剂\n\n## 🎯 主治认知陷阱\n**功能主义与工具理性陷阱**\n\n原来用户要的不是功能，而是体验..."
            }
        }
    
    def extract_prescription_id(self, filename: str) -> Optional[str]:
        """从文件名提取药方ID"""
        if filename.startswith("P") and "_" in filename:
            return filename.split("_")[0]
        return None
    
    def load_prescription(self, file_path: Path) -> Dict:
        """加载单个药方"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析YAML前置元数据
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    markdown_content = parts[2]
                    
                    try:
                        metadata = yaml.safe_load(yaml_content)
                        if metadata:
                            metadata['content'] = markdown_content
                            metadata['file_path'] = str(file_path)
                            return metadata
                    except yaml.YAMLError as e:
                        print(f"YAML解析错误 {file_path}: {e}")
            
            # 如果没有YAML元数据，尝试从文件名推断
            prescription_id = self.extract_prescription_id(file_path.name)
            return {
                "id": prescription_id,
                "display_name": f"药方{prescription_id}",
                "category": "未分类",
                "impact_score": 5,
                "content": content,
                "file_path": str(file_path)
            }
            
        except Exception as e:
            print(f"加载药方文件错误 {file_path}: {e}")
            return {}
    
    def get_prescription(self, prescription_id: str) -> Optional[Dict]:
        """获取特定药方"""
        return self.prescription_cache.get(prescription_id)
    
    def get_all_prescriptions(self) -> Dict:
        """获取所有药方"""
        return self.prescription_cache
    
    def get_prescriptions_by_category(self, category: str) -> List[Dict]:
        """根据类别获取药方"""
        results = []
        for prescription_id, prescription in self.prescription_cache.items():
            if prescription.get('category', '').lower() == category.lower():
                results.append({
                    'id': prescription_id,
                    'prescription': prescription
                })
        return results
    
    def search_prescriptions(self, query: str) -> List[Dict]:
        """搜索药方"""
        if not query:
            return []
        
        results = []
        query_lower = query.lower()
        
        for prescription_id, prescription in self.prescription_cache.items():
            score = 0
            
            # 搜索显示名称
            if query_lower in prescription.get('display_name', '').lower():
                score += 10
            
            # 搜索标签
            for tag in prescription.get('tags', []):
                if query_lower in tag.lower():
                    score += 5
            
            # 搜索症状
            for symptom in prescription.get('symptoms', []):
                if query_lower in symptom.lower():
                    score += 3
            
            # 搜索内容
            if query_lower in prescription.get('content', '').lower():
                score += 1
            
            if score > 0:
                results.append({
                    'id': prescription_id,
                    'prescription': prescription,
                    'score': score
                })
        
        # 按相关性排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results
    
    def get_related_prescriptions(self, prescription_id: str) -> List[Dict]:
        """获取相关药方"""
        prescription = self.get_prescription(prescription_id)
        if not prescription:
            return []
        
        related_ids = prescription.get('related_prescriptions', [])
        results = []
        
        for related_id in related_ids:
            related_prescription = self.get_prescription(related_id)
            if related_prescription:
                results.append({
                    'id': related_id,
                    'prescription': related_prescription
                })
        
        return results
    
    def get_prescription_stats(self) -> Dict:
        """获取药方库统计信息"""
        if not self.prescription_cache:
            return {"total": 0, "by_category": {}, "by_impact": {}}
        
        stats = {
            "total": len(self.prescription_cache),
            "by_category": {},
            "by_impact": {}
        }
        
        for prescription in self.prescription_cache.values():
            # 按类别统计
            category = prescription.get('category', '未分类')
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            
            # 按影响评级统计
            impact = prescription.get('impact_score', 5)
            impact_range = f"{impact//2*2}-{impact//2*2+1}分" if impact < 10 else "10分"
            stats["by_impact"][impact_range] = stats["by_impact"].get(impact_range, 0) + 1
        
        return stats
