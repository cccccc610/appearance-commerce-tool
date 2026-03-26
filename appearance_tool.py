#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外观商业化思考小工具
Game Appearance Commerce Thinking Tool

一个综合性的外观商业化方案思考工具，整合：
- 检查清单验证
- 决策树引导
- 方案框架生成

使用方式：
    python appearance_tool.py

作者：OpenClaw Assistant
版本：1.0.0
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


# ==================== 数据模型 ====================

class GameType(Enum):
    MOBA = "moba"
    FPS = "fps"
    SIMULATION = "simulation"


class AppearanceType(Enum):
    SKIN = "skin"
    DECORATION = "decoration"
    VFX = "vfx"
    ANIMATION = "animation"
    MOUNT = "mount"
    SOUND = "sound"
    THEME = "theme"


@dataclass
class ChecklistResult:
    """检查清单结果"""
    category: str
    total_items: int
    checked_items: int
    score: float
    missing_items: List[str]
    

@dataclass
class DecisionPath:
    """决策路径记录"""
    tree_name: str
    questions: List[str]
    answers: List[str]
    conclusion: str
    reason: str
    actions: List[str]


@dataclass
class RiskWarning:
    """风险预警"""
    level: str  # critical, high, medium, low
    category: str
    description: str
    suggestion: str


@dataclass
class CommercePlan:
    """商业化方案"""
    game_type: str
    appearance_type: str
    created_at: str
    decision_results: List[DecisionPath] = field(default_factory=list)
    checklist_results: List[ChecklistResult] = field(default_factory=list)
    risks: List[RiskWarning] = field(default_factory=list)
    art_content: Dict = field(default_factory=dict)
    competitors: List[Dict] = field(default_factory=list)
    framework: Dict = field(default_factory=dict)


# ==================== 数据加载 ====================

class DataLoader:
    """数据加载器"""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.data_dir = data_dir
        self._cache = {}
    
    def load_json(self, filename: str) -> Dict:
        """加载JSON文件"""
        if filename not in self._cache:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                self._cache[filename] = json.load(f)
        return self._cache[filename]
    
    def get_competitors(self, game_type: str) -> List[Dict]:
        """获取竞品数据"""
        data = self.load_json('competitors.json')
        return data.get(game_type, {}).get('competitors', [])
    
    def get_checklists(self) -> Dict:
        """获取检查清单"""
        return self.load_json('checklists.json')
    
    def get_decision_trees(self) -> Dict:
        """获取决策树"""
        return self.load_json('decision_trees.json')
    
    def get_art_content(self, game_type: str) -> Dict:
        """获取美术内容配置"""
        data = self.load_json('art_content.json')
        return data.get(game_type, {})


# ==================== 决策树引擎 ====================

class DecisionTreeEngine:
    """决策树引擎"""
    
    def __init__(self, tree_data: Dict):
        self.tree_data = tree_data
        self.path = []
    
    def run(self) -> DecisionPath:
        """运行决策树"""
        questions = []
        answers = []
        
        current_node = "start"
        
        while True:
            node = self.tree_data['nodes'].get(current_node)
            if not node:
                break
            
            # 结论节点
            if node.get('conclusion'):
                return DecisionPath(
                    tree_name=self.tree_data['name'],
                    questions=questions,
                    answers=answers,
                    conclusion=node.get('result', ''),
                    reason=node.get('reason', ''),
                    actions=node.get('actions', [])
                )
            
            # 计算节点
            if node.get('type') == 'calculate':
                # 这里需要根据之前的答案计算
                result = self._calculate_result(node, answers)
                return DecisionPath(
                    tree_name=self.tree_data['name'],
                    questions=questions,
                    answers=answers,
                    conclusion=result,
                    reason="根据您的选择计算得出",
                    actions=[]
                )
            
            # 问题节点
            question = node.get('question', '')
            if not question:
                break
            
            questions.append(question)
            
            # 显示选项
            options = node.get('options', {})
            if options:
                print(f"\n❓ {question}")
                options_list = list(options.items())
                for i, (key, _) in enumerate(options_list, 1):
                    print(f"   {i}. {key}")
                
                # 获取用户输入
                while True:
                    try:
                        choice = int(input("\n👉 请选择（输入数字）："))
                        if 1 <= choice <= len(options_list):
                            selected_key, next_node = options_list[choice - 1]
                            answers.append(selected_key)
                            current_node = next_node
                            break
                        else:
                            print("   ⚠️ 请输入有效数字")
                    except ValueError:
                        print("   ⚠️ 请输入数字")
            else:
                break
        
        return DecisionPath(
            tree_name=self.tree_data['name'],
            questions=questions,
            answers=answers,
            conclusion="无法确定",
            reason="决策路径中断",
            actions=[]
        )
    
    def _calculate_result(self, node: Dict, answers: List[str]) -> str:
        """计算结果"""
        # 简化计算逻辑
        return "根据输入计算得出定价建议"


# ==================== 检查清单引擎 ====================

class ChecklistEngine:
    """检查清单引擎"""
    
    def __init__(self, checklist_data: Dict):
        self.checklist_data = checklist_data
    
    def run_category(self, category_key: str) -> ChecklistResult:
        """运行单个检查类别"""
        categories = self.checklist_data.get('categories', [])
        
        for category in categories:
            if category.get('name') == category_key or category_key == 'all':
                return self._check_category(category)
        
        return ChecklistResult(
            category=category_key,
            total_items=0,
            checked_items=0,
            score=0,
            missing_items=[]
        )
    
    def run_all(self) -> List[ChecklistResult]:
        """运行所有检查"""
        results = []
        categories = self.checklist_data.get('categories', [])
        
        for category in categories:
            result = self._check_category(category)
            results.append(result)
        
        return results
    
    def _check_category(self, category: Dict) -> ChecklistResult:
        """检查单个类别"""
        items = category.get('items', [])
        checked = 0
        total_weight = 0
        checked_weight = 0
        missing = []
        
        print(f"\n📋 【{category['name']}】检查")
        print("-" * 40)
        
        for item in items:
            total_weight += item.get('weight', 1)
            print(f"   [{item['id']}] {item['content']}")
            
            while True:
                answer = input("   ✅ 已完成？(y/n/skip): ").lower()
                if answer in ['y', 'n', 'skip']:
                    break
                print("   ⚠️ 请输入 y/n/skip")
            
            if answer == 'y':
                checked += 1
                checked_weight += item.get('weight', 1)
            elif answer == 'n':
                missing.append(f"{item['id']}: {item['content']}")
        
        score = (checked_weight / total_weight * 100) if total_weight > 0 else 0
        
        return ChecklistResult(
            category=category['name'],
            total_items=len(items),
            checked_items=checked,
            score=round(score, 1),
            missing_items=missing
        )


# ==================== 方案生成器 ====================

class PlanGenerator:
    """方案生成器"""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
    
    def generate(
        self,
        game_type: str,
        appearance_type: str,
        decision_results: List[DecisionPath],
        checklist_results: List[ChecklistResult]
    ) -> CommercePlan:
        """生成完整方案"""
        
        # 获取竞品参考
        competitors = self.data_loader.get_competitors(game_type)
        
        # 获取美术内容
        art_content = self.data_loader.get_art_content(game_type)
        
        # 分析风险
        risks = self._analyze_risks(checklist_results)
        
        # 生成框架
        framework = self._generate_framework(
            game_type, appearance_type, decision_results, checklist_results
        )
        
        return CommercePlan(
            game_type=game_type,
            appearance_type=appearance_type,
            created_at=datetime.now().isoformat(),
            decision_results=decision_results,
            checklist_results=checklist_results,
            risks=risks,
            art_content=art_content.get('art_categories', {}),
            competitors=competitors[:3],  # 取前3个竞品
            framework=framework
        )
    
    def _analyze_risks(self, checklist_results: List[ChecklistResult]) -> List[RiskWarning]:
        """分析风险"""
        risks = []
        
        for result in checklist_results:
            # 评分低于60分的类别产生风险预警
            if result.score < 60:
                risk_level = "high" if result.score < 40 else "medium"
                for item in result.missing_items:
                    risks.append(RiskWarning(
                        level=risk_level,
                        category=result.category,
                        description=f"未完成：{item}",
                        suggestion=f"建议补充完善 {result.category} 相关内容"
                    ))
            elif result.score < 80:
                # 评分60-80产生低风险预警
                if result.missing_items:
                    risks.append(RiskWarning(
                        level="low",
                        category=result.category,
                        description=f"{result.category} 存在 {len(result.missing_items)} 项未完成",
                        suggestion="建议尽快完善"
                    ))
        
        return risks
    
    def _generate_framework(
        self,
        game_type: str,
        appearance_type: str,
        decision_results: List[DecisionPath],
        checklist_results: List[ChecklistResult]
    ) -> Dict:
        """生成方案框架"""
        
        # 计算总体得分
        total_score = sum(r.score for r in checklist_results) / len(checklist_results) if checklist_results else 0
        
        # 提取决策结论
        decisions = {}
        for d in decision_results:
            decisions[d.tree_name] = {
                'conclusion': d.conclusion,
                'reason': d.reason,
                'actions': d.actions
            }
        
        framework = {
            'summary': {
                'game_type': game_type,
                'appearance_type': appearance_type,
                'overall_score': round(total_score, 1),
                'status': self._get_status(total_score)
            },
            'decisions': decisions,
            'sections': [
                {
                    'name': '设计定位',
                    'items': [
                        '目标用户群体定义',
                        '主题风格方向',
                        '品质等级定位',
                        '差异化卖点'
                    ]
                },
                {
                    'name': '美术内容',
                    'items': [
                        '主题题材设计',
                        '视觉风格/配色',
                        '模型制作规格',
                        '特效设计方向',
                        '动画需求清单',
                        '音效/语音需求'
                    ]
                },
                {
                    'name': '定价策略',
                    'items': [
                        '基础定价确定',
                        '定价系数计算',
                        '折扣促销规划',
                        '套餐组合设计'
                    ]
                },
                {
                    'name': '制作排期',
                    'items': [
                        '各阶段时间节点',
                        '里程碑评审点',
                        '资源需求评估',
                        '上线时间确定'
                    ]
                },
                {
                    'name': '运营规划',
                    'items': [
                        '预热宣传计划',
                        '上线活动方案',
                        '数据指标目标',
                        '监控方案制定'
                    ]
                }
            ]
        }
        
        return framework
    
    def _get_status(self, score: float) -> str:
        """获取状态评价"""
        if score >= 90:
            return "✅ 优秀 - 方案完整度高，可进入执行阶段"
        elif score >= 70:
            return "🟢 良好 - 方案基本完整，建议完善部分内容"
        elif score >= 50:
            return "🟡 待完善 - 存在较多缺失项，建议补充后再执行"
        else:
            return "🔴 不完整 - 方案存在重大缺失，建议重新规划"


# ==================== 输出生成器 ====================

class OutputGenerator:
    """输出生成器"""
    
    @staticmethod
    def generate_markdown(plan: CommercePlan) -> str:
        """生成Markdown格式输出"""
        
        md = f"""# 外观商业化方案报告

> 生成时间：{plan.created_at}
> 游戏品类：{plan.game_type.upper()}
> 外观类型：{plan.appearance_type}

---

## 📊 方案概览

| 维度 | 内容 |
|------|------|
| **游戏品类** | {plan.game_type.upper()} |
| **外观类型** | {plan.appearance_type} |
| **完整度评分** | {plan.framework['summary']['overall_score']}分 |
| **状态评估** | {plan.framework['summary']['status']} |

---

## 🎯 决策引导结果

"""
        
        for decision in plan.decision_results:
            md += f"""### {decision.tree_name}

**结论：** {decision.conclusion}

**原因：** {decision.reason}

**建议行动：**
"""
            for action in decision.actions:
                md += f"- {action}\n"
            md += "\n"
        
        md += """---

## ✅ 检查清单结果

"""
        
        for result in plan.checklist_results:
            status = "✅" if result.score >= 80 else "🟡" if result.score >= 60 else "🔴"
            md += f"""### {status} {result.category}

| 指标 | 数值 |
|------|------|
| 完成项数 | {result.checked_items}/{result.total_items} |
| 得分 | {result.score}% |

"""
            if result.missing_items:
                md += "**待完成项：**\n"
                for item in result.missing_items:
                    md += f"- [ ] {item}\n"
                md += "\n"
        
        md += """---

## ⚠️ 风险预警

"""
        
        if plan.risks:
            # 按风险等级分组
            critical = [r for r in plan.risks if r.level == 'critical']
            high = [r for r in plan.risks if r.level == 'high']
            medium = [r for r in plan.risks if r.level == 'medium']
            low = [r for r in plan.risks if r.level == 'low']
            
            if critical:
                md += "### 🔴 严重风险\n\n"
                for r in critical:
                    md += f"- **{r.category}**：{r.description}\n  - 建议：{r.suggestion}\n\n"
            
            if high:
                md += "### 🟠 高风险\n\n"
                for r in high:
                    md += f"- **{r.category}**：{r.description}\n  - 建议：{r.suggestion}\n\n"
            
            if medium:
                md += "### 🟡 中风险\n\n"
                for r in medium:
                    md += f"- **{r.category}**：{r.description}\n  - 建议：{r.suggestion}\n\n"
            
            if low:
                md += "### 🟢 低风险\n\n"
                for r in low:
                    md += f"- **{r.category}**：{r.description}\n  - 建议：{r.suggestion}\n\n"
        else:
            md += "✅ 未发现重大风险\n\n"
        
        md += """---

## 🎨 美术内容参考

"""
        
        for category_name, category_data in plan.art_content.items():
            md += f"### {category_data.get('name', category_name)}\n\n"
            md += f"{category_data.get('description', '')}\n\n"
            
            if 'options' in category_data:
                md += "| 主题类型 | 关键元素 | 适用场景 |\n"
                md += "|----------|----------|----------|\n"
                for opt in category_data['options']:
                    md += f"| {opt['name']} | {opt.get('key_elements', '')} | {opt.get('best_for', '')} |\n"
                md += "\n"
            
            if 'items' in category_data:
                md += "| 项目 | 规格 | 品质要求 |\n"
                md += "|------|------|----------|\n"
                for item in category_data['items']:
                    spec = item.get('spec', '-')
                    quality = ', '.join([f"{k}:{v}" for k, v in item.get('quality_tier', {}).items()]) if item.get('quality_tier') else '-'
                    md += f"| {item['name']} | {spec} | {quality[:50]}... |\n" if len(quality) > 50 else f"| {item['name']} | {spec} | {quality} |\n"
                md += "\n"
        
        md += """---

## 🏆 竞品参考

"""
        
        for comp in plan.competitors:
            md += f"### {comp['name']}（{comp['company']}）\n\n"
            md += f"**定价模式：** {comp['pricing_model']}\n\n"
            
            if 'price_range' in comp:
                md += "**价格区间：**\n\n"
                md += "| 品质等级 | 价格 |\n"
                md += "|----------|------|\n"
                for quality, price in comp['price_range'].items():
                    md += f"| {quality} | {price} |\n"
                md += "\n"
            
            if 'features' in comp:
                md += "**核心特点：**\n"
                for feature in comp['features']:
                    md += f"- {feature}\n"
                md += "\n"
            
            if 'success_cases' in comp:
                md += "**成功案例：**\n\n"
                for case in comp['success_cases']:
                    md += f"- **{case['skin']}**（{case['type']}）：{case['sales']}\n"
                    md += f"  - 关键成功因素：{case['key_success']}\n"
                md += "\n"
        
        md += """---

## 📝 方案框架

"""
        
        for section in plan.framework.get('sections', []):
            md += f"### {section['name']}\n\n"
            for item in section['items']:
                md += f"- [ ] {item}\n"
            md += "\n"
        
        md += """---

## 📋 下一步行动

1. 完成检查清单中未完成的项目
2. 根据决策引导结果确定最终方案
3. 参考竞品案例优化定价和设计
4. 完善美术内容详细需求
5. 制定详细的时间排期表

---

> 本报告由外观商业化思考小工具自动生成
"""
        
        return md


# ==================== 主控制器 ====================

class AppearanceCommerceTool:
    """外观商业化思考小工具主控制器"""
    
    GAME_TYPES = {
        '1': ('moba', 'MOBA（多人在线战术竞技）'),
        '2': ('fps', 'FPS（第一人称射击）'),
        '3': ('simulation', '模拟经营')
    }
    
    APPEARANCE_TYPES = {
        '1': 'skin',
        '2': 'decoration',
        '3': 'vfx',
        '4': 'animation',
        '5': 'mount',
        '6': 'sound',
        '7': 'theme'
    }
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.decision_results = []
        self.checklist_results = []
        self.selected_game_type = None
        self.selected_appearance_type = None
    
    def run(self):
        """运行主程序"""
        self._print_header()
        
        # 选择游戏品类
        self.selected_game_type = self._select_game_type()
        
        # 选择外观类型
        self.selected_appearance_type = self._select_appearance_type()
        
        # 主菜单
        while True:
            self._print_menu()
            choice = input("\n👉 请选择功能（输入数字）：").strip()
            
            if choice == '1':
                self._run_decision_trees()
            elif choice == '2':
                self._run_checklists()
            elif choice == '3':
                self._show_competitors()
            elif choice == '4':
                self._show_art_content()
            elif choice == '5':
                self._generate_plan()
            elif choice == '6':
                self._run_all()
            elif choice == '0':
                print("\n👋 感谢使用外观商业化思考小工具！\n")
                break
            else:
                print("\n⚠️ 无效选择，请重新输入")
    
    def _print_header(self):
        """打印标题"""
        print("\n" + "=" * 50)
        print("🎨 外观商业化思考小工具 v1.0")
        print("=" * 50)
        print("\n确保外观商业化方案的基本盘")
        print("整合检查清单、决策树、方案生成三大功能\n")
    
    def _select_game_type(self) -> str:
        """选择游戏品类"""
        print("\n📌 请选择游戏品类：")
        print("-" * 30)
        for key, (code, name) in self.GAME_TYPES.items():
            print(f"   {key}. {name}")
        
        while True:
            choice = input("\n👉 请选择（输入数字）：").strip()
            if choice in self.GAME_TYPES:
                selected = self.GAME_TYPES[choice][0]
                print(f"\n✅ 已选择：{self.GAME_TYPES[choice][1]}")
                return selected
            print("⚠️ 无效选择，请重新输入")
    
    def _select_appearance_type(self) -> str:
        """选择外观类型"""
        print("\n📌 请选择外观类型：")
        print("-" * 30)
        appearance_names = {
            'skin': '皮肤',
            'decoration': '装饰',
            'vfx': '特效',
            'animation': '动画/动作',
            'mount': '载具/坐骑',
            'sound': '音效',
            'theme': '主题选材'
        }
        for key, value in self.APPEARANCE_TYPES.items():
            print(f"   {key}. {appearance_names.get(value, value)}")
        
        while True:
            choice = input("\n👉 请选择（输入数字）：").strip()
            if choice in self.APPEARANCE_TYPES:
                selected = self.APPEARANCE_TYPES[choice]
                print(f"\n✅ 已选择：{appearance_names.get(selected, selected)}")
                return selected
            print("⚠️ 无效选择，请重新输入")
    
    def _print_menu(self):
        """打印主菜单"""
        print("\n" + "-" * 50)
        print("📋 功能菜单")
        print("-" * 50)
        print("   1. 🌳 决策树引导（英雄选择/品质定位/定价/主题）")
        print("   2. ✅ 检查清单验证（完整性/合理性/风险）")
        print("   3. 🏆 竞品参考（查看同类产品商业化方案）")
        print("   4. 🎨 美术内容参考（题材/动画/特效/故事/音效）")
        print("   5. 📝 生成方案报告（输出完整方案文档）")
        print("   6. 🚀 一键运行（完整流程）")
        print("   0. 退出")
    
    def _run_decision_trees(self):
        """运行决策树"""
        print("\n" + "=" * 50)
        print("🌳 决策树引导")
        print("=" * 50)
        
        trees = self.data_loader.get_decision_trees()
        
        print("\n可用的决策树：")
        tree_list = list(trees.items())
        for i, (key, tree) in enumerate(tree_list, 1):
            applicable = tree.get('applicable', [])
            if self.selected_game_type in applicable or 'all' in applicable:
                print(f"   {i}. {tree['name']}")
                print(f"      {tree['description']}")
        
        print(f"\n   a. 运行所有决策树")
        print(f"   0. 返回主菜单")
        
        while True:
            choice = input("\n👉 请选择决策树（输入数字或a）：").strip().lower()
            
            if choice == '0':
                break
            elif choice == 'a':
                # 运行所有决策树
                for key, tree in tree_list:
                    applicable = tree.get('applicable', [])
                    if self.selected_game_type in applicable or 'all' in applicable:
                        print(f"\n{'=' * 50}")
                        print(f"🌳 {tree['name']}")
                        print("=" * 50)
                        engine = DecisionTreeEngine(tree)
                        result = engine.run()
                        self.decision_results.append(result)
                        print(f"\n✅ 结论：{result.conclusion}")
                        print(f"📌 原因：{result.reason}")
                        if result.actions:
                            print("📋 建议行动：")
                            for action in result.actions:
                                print(f"   - {action}")
                break
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(tree_list):
                        key, tree = tree_list[idx]
                        applicable = tree.get('applicable', [])
                        if self.selected_game_type in applicable or 'all' in applicable:
                            engine = DecisionTreeEngine(tree)
                            result = engine.run()
                            self.decision_results.append(result)
                            print(f"\n✅ 结论：{result.conclusion}")
                            print(f"📌 原因：{result.reason}")
                            if result.actions:
                                print("📋 建议行动：")
                                for action in result.actions:
                                    print(f"   - {action}")
                            break
                        else:
                            print("⚠️ 该决策树不适用于当前游戏品类")
                    else:
                        print("⚠️ 无效选择")
                except ValueError:
                    print("⚠️ 请输入有效数字")
    
    def _run_checklists(self):
        """运行检查清单"""
        print("\n" + "=" * 50)
        print("✅ 检查清单验证")
        print("=" * 50)
        
        checklists = self.data_loader.get_checklists()
        
        print("\n可用的检查清单：")
        checklist_types = [
            ('completeness', '完整性检查', '确保方案覆盖所有关键环节'),
            ('rationality', '合理性检查', '确保定价、排期、目标合理可行'),
            ('risk', '风险检查', '识别方案潜在风险点')
        ]
        
        for i, (key, name, desc) in enumerate(checklist_types, 1):
            print(f"   {i}. {name}")
            print(f"      {desc}")
        
        print(f"\n   a. 运行所有检查")
        print(f"   0. 返回主菜单")
        
        while True:
            choice = input("\n👉 请选择（输入数字或a）：").strip().lower()
            
            if choice == '0':
                break
            elif choice == 'a':
                # 运行所有检查
                for key, name, _ in checklist_types:
                    print(f"\n{'=' * 50}")
                    print(f"✅ {name}")
                    print("=" * 50)
                    engine = ChecklistEngine(checklists[key])
                    results = engine.run_all()
                    self.checklist_results.extend(results)
                    
                    for result in results:
                        status = "✅" if result.score >= 80 else "🟡" if result.score >= 60 else "🔴"
                        print(f"\n{status} {result.category}: {result.score}% ({result.checked_items}/{result.total_items})")
                break
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(checklist_types):
                        key, name, _ = checklist_types[idx]
                        engine = ChecklistEngine(checklists[key])
                        results = engine.run_all()
                        self.checklist_results.extend(results)
                        
                        print(f"\n📊 {name}结果：")
                        total_score = sum(r.score for r in results) / len(results) if results else 0
                        print(f"   总体得分：{round(total_score, 1)}%")
                        break
                    else:
                        print("⚠️ 无效选择")
                except ValueError:
                    print("⚠️ 请输入有效数字")
    
    def _show_competitors(self):
        """显示竞品参考"""
        print("\n" + "=" * 50)
        print("🏆 竞品参考")
        print("=" * 50)
        
        competitors = self.data_loader.get_competitors(self.selected_game_type)
        
        for i, comp in enumerate(competitors, 1):
            print(f"\n{i}. {comp['name']}（{comp['company']}）")
            print(f"   定价模式：{comp['pricing_model']}")
            
            if 'features' in comp:
                print("   核心特点：")
                for feature in comp['features'][:5]:
                    print(f"   • {feature}")
            
            if 'success_cases' in comp:
                print("   成功案例：")
                for case in comp['success_cases'][:2]:
                    print(f"   • {case['skin']}：{case['key_success']}")
    
    def _show_art_content(self):
        """显示美术内容参考"""
        print("\n" + "=" * 50)
        print("🎨 美术内容参考")
        print("=" * 50)
        
        art_content = self.data_loader.get_art_content(self.selected_game_type)
        categories = art_content.get('art_categories', {})
        
        for key, category in categories.items():
            print(f"\n📌 {category['name']}")
            print(f"   {category['description']}")
            
            if 'options' in category:
                print("   可选方向：")
                for opt in category['options'][:3]:
                    print(f"   • {opt['name']}：{opt.get('key_elements', '')}")
    
    def _generate_plan(self):
        """生成方案报告"""
        print("\n" + "=" * 50)
        print("📝 生成方案报告")
        print("=" * 50)
        
        if not self.decision_results:
            print("\n⚠️ 请先运行决策树引导")
            return
        
        if not self.checklist_results:
            print("\n⚠️ 请先运行检查清单验证")
            return
        
        generator = PlanGenerator(self.data_loader)
        plan = generator.generate(
            self.selected_game_type,
            self.selected_appearance_type,
            self.decision_results,
            self.checklist_results
        )
        
        # 生成Markdown输出
        output = OutputGenerator.generate_markdown(plan)
        
        # 保存文件
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"commerce_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"\n✅ 方案报告已生成：{filepath}")
        print(f"\n📊 方案概要：")
        print(f"   游戏品类：{plan.game_type.upper()}")
        print(f"   外观类型：{plan.appearance_type}")
        print(f"   完整度评分：{plan.framework['summary']['overall_score']}分")
        print(f"   状态评估：{plan.framework['summary']['status']}")
        print(f"   风险预警：{len(plan.risks)}项")
    
    def _run_all(self):
        """一键运行完整流程"""
        print("\n" + "=" * 50)
        print("🚀 一键运行完整流程")
        print("=" * 50)
        
        # 运行决策树
        print("\n【步骤1/4】运行决策树引导...")
        trees = self.data_loader.get_decision_trees()
        for key, tree in trees.items():
            applicable = tree.get('applicable', [])
            if self.selected_game_type in applicable or 'all' in applicable:
                engine = DecisionTreeEngine(tree)
                result = engine.run()
                self.decision_results.append(result)
                print(f"   ✓ {tree['name']}: {result.conclusion}")
        
        # 运行检查清单
        print("\n【步骤2/4】运行检查清单验证...")
        checklists = self.data_loader.get_checklists()
        for key in ['completeness', 'rationality', 'risk']:
            engine = ChecklistEngine(checklists[key])
            results = engine.run_all()
            self.checklist_results.extend(results)
            avg_score = sum(r.score for r in results) / len(results) if results else 0
            print(f"   ✓ {checklists[key]['name']}: {round(avg_score, 1)}%")
        
        # 显示竞品参考
        print("\n【步骤3/4】加载竞品参考...")
        competitors = self.data_loader.get_competitors(self.selected_game_type)
        print(f"   ✓ 已加载 {len(competitors)} 个竞品案例")
        
        # 生成报告
        print("\n【步骤4/4】生成方案报告...")
        self._generate_plan()


# ==================== 入口 ====================

def main():
    """主入口"""
    tool = AppearanceCommerceTool()
    tool.run()


if __name__ == '__main__':
    main()
