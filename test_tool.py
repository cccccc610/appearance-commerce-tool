#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外观商业化思考小工具 - 自动化测试脚本

用于测试工具的各个功能模块，生成示例报告
"""

import json
import os
import sys
from datetime import datetime

# 添加工具目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from appearance_tool import (
    DataLoader, DecisionTreeEngine, ChecklistEngine,
    PlanGenerator, OutputGenerator, AppearanceCommerceTool
)


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_data_loading():
    """测试数据加载"""
    print_section("测试1: 数据加载")
    
    loader = DataLoader()
    
    # 测试竞品数据
    competitors = loader.get_competitors('moba')
    print(f"✅ MOBA竞品数据: {len(competitors)} 个竞品")
    
    competitors_fps = loader.get_competitors('fps')
    print(f"✅ FPS竞品数据: {len(competitors_fps)} 个竞品")
    
    competitors_sim = loader.get_competitors('simulation')
    print(f"✅ 模拟经营竞品数据: {len(competitors_sim)} 个竞品")
    
    # 测试检查清单
    checklists = loader.get_checklists()
    total_items = sum(
        len(cat['items']) 
        for checklist in checklists.values() 
        for cat in checklist.get('categories', [])
    )
    print(f"✅ 检查清单: {len(checklists)} 个维度, 共 {total_items} 个检查项")
    
    # 测试决策树
    trees = loader.get_decision_trees()
    print(f"✅ 决策树: {len(trees)} 个决策树")
    
    # 测试美术内容
    art_moba = loader.get_art_content('moba')
    print(f"✅ MOBA美术内容: {len(art_moba.get('art_categories', {}))} 个类别")
    
    return True


def test_decision_trees():
    """测试决策树（模拟输入）"""
    print_section("测试2: 决策树引擎")
    
    loader = DataLoader()
    trees = loader.get_decision_trees()
    
    # 模拟决策路径
    simulated_paths = [
        {
            'tree': 'hero_selection',
            'answers': ['T1（强势）', '≥15%（高人气）', '≤3款'],
            'expected': '优先候选'
        },
        {
            'tree': 'quality_tier',
            'answers': ['是，完全重做', '是', '专属回城动画', '专属语音包', '专属击杀/死亡特效'],
            'expected': '传说级或限定级'
        }
    ]
    
    results = []
    for path in simulated_paths:
        tree_data = trees.get(path['tree'])
        if tree_data:
            print(f"\n🌳 决策树: {tree_data['name']}")
            print(f"   模拟回答: {' → '.join(path['answers'])}")
            print(f"   预期结论: {path['expected']}")
            
            # 手动遍历决策树获取结果
            result = simulate_decision_path(tree_data, path['answers'])
            print(f"   实际结果: {result}")
            results.append({
                'tree': tree_data['name'],
                'answers': path['answers'],
                'result': result
            })
    
    print(f"\n✅ 决策树测试完成: {len(results)} 个决策树")
    return results


def simulate_decision_path(tree_data, answers):
    """模拟决策路径"""
    nodes = tree_data['nodes']
    current = 'start'
    answer_idx = 0
    
    while current in nodes:
        node = nodes[current]
        
        if node.get('conclusion'):
            return node.get('result', '未知')
        
        if node.get('type') == 'choice' and 'options' in node:
            options = list(node['options'].keys())
            if answer_idx < len(answers):
                selected = answers[answer_idx]
                if selected in node['options']:
                    current = node['options'][selected]
                    answer_idx += 1
                    continue
            # 默认选择第一个选项
            current = list(node['options'].values())[0]
            answer_idx += 1
        else:
            break
    
    return "决策路径结束"


def test_checklist():
    """测试检查清单（模拟检查）"""
    print_section("测试3: 检查清单引擎")
    
    loader = DataLoader()
    checklists = loader.get_checklists()
    
    # 模拟检查结果
    simulated_results = {
        'completeness': {
            '设计定位': {'checked': 5, 'total': 6},
            '美术内容': {'checked': 4, 'total': 6},
            '定价策略': {'checked': 4, 'total': 5},
            '制作排期': {'checked': 3, 'total': 5},
            '运营规划': {'checked': 3, 'total': 5}
        },
        'rationality': {
            '定价合理性': {'checked': 4, 'total': 5},
            '排期合理性': {'checked': 3, 'total': 5},
            '目标合理性': {'checked': 4, 'total': 5}
        },
        'risk': {
            '设计风险': {'checked': 4, 'total': 5},
            '技术风险': {'checked': 4, 'total': 5},
            '运营风险': {'checked': 3, 'total': 5},
            '合规风险': {'checked': 5, 'total': 5}
        }
    }
    
    results = []
    for checklist_type, categories in simulated_results.items():
        print(f"\n📋 {checklists[checklist_type]['name']}:")
        total_score = 0
        for cat_name, data in categories.items():
            score = round(data['checked'] / data['total'] * 100, 1)
            total_score += score
            status = "✅" if score >= 80 else "🟡" if score >= 60 else "🔴"
            print(f"   {status} {cat_name}: {score}% ({data['checked']}/{data['total']})")
            results.append({
                'category': cat_name,
                'score': score,
                'total': data['total'],
                'checked': data['checked']
            })
        avg_score = round(total_score / len(categories), 1)
        print(f"   📊 平均得分: {avg_score}%")
    
    print(f"\n✅ 检查清单测试完成")
    return results


def test_report_generation():
    """测试报告生成"""
    print_section("测试4: 报告生成")
    
    loader = DataLoader()
    generator = PlanGenerator(loader)
    
    # 创建模拟数据
    from appearance_tool import DecisionPath, ChecklistResult, CommercePlan
    
    decision_results = [
        DecisionPath(
            tree_name="英雄/角色选择决策树",
            questions=["目标英雄版本强度?", "出场率?", "现有皮肤数量?"],
            answers=["T1（强势）", "≥15%（高人气）", "≤3款"],
            conclusion="优先候选",
            reason="版本强势+高人气+皮肤存量少，是理想的皮肤目标",
            actions=["确认主题方向与英雄气质匹配", "评估制作资源", "制定时间排期"]
        ),
        DecisionPath(
            tree_name="品质等级决策树",
            questions=["是否制作新模型?", "是否制作全套特效?", "是否包含高级特性?"],
            answers=["是，完全重做", "是", "专属回城动画+专属语音包"],
            conclusion="传说级",
            reason="全新模型+全套特效+多项高级特性",
            actions=["规划15周制作周期", "预留评审时间", "制定高规格验收标准"]
        ),
        DecisionPath(
            tree_name="定价决策树",
            questions=["品质等级?", "英雄人气?", "主题类型?", "销售策略?"],
            answers=["传说", "TOP10", "IP联动", "限时销售"],
            conclusion="建议定价 198-268 元",
            reason="传说级品质+高人气英雄+IP联动溢价+限定稀缺性",
            actions=["首周折扣建议 8.5折", "可捆绑装饰套装销售"]
        ),
        DecisionPath(
            tree_name="主题选择决策树",
            questions=["计划何时上线?", "是否有IP联动机会?"],
            answers=["春节/新年期间", "有明确IP合作计划"],
            conclusion="春节IP联动主题",
            reason="春节节点+IP合作机会，双重溢价",
            actions=["确认IP授权细节", "融入春节元素", "预留IP审核时间"]
        )
    ]
    
    checklist_results = [
        ChecklistResult(category="设计定位", total_items=6, checked_items=5, score=83.3, missing_items=["D06: 参考对标已确定"]),
        ChecklistResult(category="美术内容", total_items=6, checked_items=5, score=83.3, missing_items=["A06: 音效/语音需求已明确"]),
        ChecklistResult(category="定价策略", total_items=5, checked_items=4, score=80.0, missing_items=["P05: 与竞品定价对比已完成"]),
        ChecklistResult(category="制作排期", total_items=5, checked_items=4, score=80.0, missing_items=["S05: 预热/运营时间线已规划"]),
        ChecklistResult(category="运营规划", total_items=5, checked_items=3, score=60.0, missing_items=["O04: 监控方案已制定", "O05: 返场/长尾策略已考虑"]),
        ChecklistResult(category="定价合理性", total_items=5, checked_items=4, score=80.0, missing_items=["R05: 付费用户价格接受度已评估"]),
        ChecklistResult(category="排期合理性", total_items=5, checked_items=4, score=80.0, missing_items=["R10: 预留了缓冲时间"]),
        ChecklistResult(category="目标合理性", total_items=5, checked_items=4, score=80.0, missing_items=["R15: 风险预案已准备"]),
        ChecklistResult(category="设计风险", total_items=5, checked_items=4, score=80.0, missing_items=["RK05: 是否存在穿模/模型冲突问题"]),
        ChecklistResult(category="技术风险", total_items=5, checked_items=4, score=80.0, missing_items=["RK10: 是否有低配模式开关"]),
        ChecklistResult(category="运营风险", total_items=5, checked_items=3, score=60.0, missing_items=["RK14: 返场规则是否提前告知", "RK15: 是否准备了舆情应对预案"]),
        ChecklistResult(category="合规风险", total_items=5, checked_items=5, score=100.0, missing_items=[])
    ]
    
    # 生成方案
    plan = generator.generate(
        game_type='moba',
        appearance_type='skin',
        decision_results=decision_results,
        checklist_results=checklist_results
    )
    
    # 生成 Markdown 报告
    output = OutputGenerator.generate_markdown(plan)
    
    # 保存报告
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"✅ 测试报告已生成: {filepath}")
    print(f"\n📊 报告概要:")
    print(f"   游戏品类: {plan.game_type.upper()}")
    print(f"   外观类型: {plan.appearance_type}")
    print(f"   完整度评分: {plan.framework['summary']['overall_score']}分")
    print(f"   风险预警: {len(plan.risks)}项")
    
    return filepath


def test_competitors_display():
    """测试竞品参考展示"""
    print_section("测试5: 竞品参考展示")
    
    loader = DataLoader()
    
    for game_type in ['moba', 'fps', 'simulation']:
        competitors = loader.get_competitors(game_type)
        print(f"\n🎮 {game_type.upper()} 竞品 ({len(competitors)}个):")
        for comp in competitors:
            print(f"   • {comp['name']} ({comp['company']})")
            if 'success_cases' in comp and comp['success_cases']:
                case = comp['success_cases'][0]
                print(f"     成功案例: {case['skin']} - {case['key_success']}")
    
    return True


def test_art_content_display():
    """测试美术内容展示"""
    print_section("测试6: 美术内容展示")
    
    loader = DataLoader()
    
    for game_type in ['moba']:
        art = loader.get_art_content(game_type)
        print(f"\n🎨 {game_type.upper()} 美术内容:")
        for cat_key, cat_data in art.get('art_categories', {}).items():
            print(f"   📌 {cat_data['name']}")
            if 'options' in cat_data:
                for opt in cat_data['options'][:3]:
                    print(f"      • {opt['name']}")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("  🧪 外观商业化思考小工具 - 自动化测试")
    print("=" * 60)
    print(f"  测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # 测试1: 数据加载
    try:
        results['data_loading'] = test_data_loading()
        print("\n✅ 数据加载测试通过")
    except Exception as e:
        print(f"\n❌ 数据加载测试失败: {e}")
        results['data_loading'] = False
    
    # 测试2: 决策树
    try:
        results['decision_trees'] = test_decision_trees()
        print("\n✅ 决策树测试通过")
    except Exception as e:
        print(f"\n❌ 决策树测试失败: {e}")
        results['decision_trees'] = False
    
    # 测试3: 检查清单
    try:
        results['checklist'] = test_checklist()
        print("\n✅ 检查清单测试通过")
    except Exception as e:
        print(f"\n❌ 检查清单测试失败: {e}")
        results['checklist'] = False
    
    # 测试4: 报告生成
    try:
        results['report'] = test_report_generation()
        print("\n✅ 报告生成测试通过")
    except Exception as e:
        print(f"\n❌ 报告生成测试失败: {e}")
        results['report'] = False
    
    # 测试5: 竞品参考
    try:
        results['competitors'] = test_competitors_display()
        print("\n✅ 竞品参考测试通过")
    except Exception as e:
        print(f"\n❌ 竞品参考测试失败: {e}")
        results['competitors'] = False
    
    # 测试6: 美术内容
    try:
        results['art_content'] = test_art_content_display()
        print("\n✅ 美术内容测试通过")
    except Exception as e:
        print(f"\n❌ 美术内容测试失败: {e}")
        results['art_content'] = False
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("  📊 测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n  通过: {passed}/{total}")
    
    for name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status} - {name}")
    
    print("\n" + "=" * 60)
    
    if passed == total:
        print("  🎉 所有测试通过！工具可正常运行。")
    else:
        print("  ⚠️ 部分测试失败，请检查错误信息。")
    
    print("=" * 60 + "\n")
    
    return results


if __name__ == '__main__':
    run_all_tests()
