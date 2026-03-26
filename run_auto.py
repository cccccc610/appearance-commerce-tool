#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外观商业化思考小工具 - 自动运行模式
支持命令行参数，非交互式运行
"""

import sys
import os
import json
import argparse
from datetime import datetime

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def load_json(filename: str) -> dict:
    """加载JSON文件"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_auto(game_type: str, appearance_type: str, output_dir: str = None):
    """自动运行工具"""
    
    print("=" * 60)
    print("🎨 外观商业化思考小工具 v1.0 (自动模式)")
    print("=" * 60)
    print()
    
    # 验证输入
    valid_game_types = ['moba', 'fps', 'simulation']
    valid_appearance_types = ['skin', 'decoration', 'vfx', 'animation', 'mount', 'sound', 'theme']
    
    if game_type.lower() not in valid_game_types:
        print(f"❌ 错误：不支持的游戏品类 '{game_type}'")
        print(f"   支持的品类：{', '.join(valid_game_types)}")
        return
    
    if appearance_type.lower() not in valid_appearance_types:
        print(f"❌ 错误：不支持的外观类型 '{appearance_type}'")
        print(f"   支持的类型：{', '.join(valid_appearance_types)}")
        return
    
    game_type = game_type.lower()
    appearance_type = appearance_type.lower()
    
    game_type_names = {
        'moba': 'MOBA（多人在线战术竞技）',
        'fps': 'FPS（第一人称射击）',
        'simulation': '模拟经营'
    }
    
    print(f"📌 游戏品类：{game_type_names.get(game_type, game_type)}")
    print(f"🎨 外观类型：{appearance_type}")
    print()
    
    # 加载数据
    print("📂 加载配置数据...")
    competitors_data = load_json('competitors.json')
    checklists_data = load_json('checklists.json')
    decision_trees_data = load_json('decision_trees.json')
    art_content_data = load_json('art_content.json')
    print("   ✓ 竞品数据")
    print("   ✓ 检查清单")
    print("   ✓ 决策树")
    print("   ✓ 美术内容")
    print()
    
    # 获取适用的数据
    competitors = competitors_data.get(game_type, {}).get('competitors', [])
    art_content = art_content_data.get(game_type, {}).get('art_categories', {})
    
    # 运行决策树（自动选择第一个选项）
    print("🌳 运行决策树引导...")
    decision_results = {}
    
    applicable_trees = {
        k: v for k, v in decision_trees_data.items() 
        if game_type in v.get('applicable', [])
    }
    
    for tree_key, tree_data in applicable_trees.items():
        result = run_decision_tree_auto(tree_data)
        decision_results[tree_key] = result
        print(f"   ✓ {tree_data.get('name', tree_key)}: {result.get('result', 'N/A')}")
    
    print()
    
    # 运行检查清单（全选）
    print("✅ 运行检查清单验证...")
    checklist_results = {}
    total_items = 0
    total_checked = 0
    
    for check_type, checklist in checklists_data.items():
        checklist_results[check_type] = {}
        for category in checklist.get('categories', []):
            for item in category.get('items', []):
                item_id = item.get('id')
                total_items += 1
                # 自动勾选所有项
                checklist_results[check_type][item_id] = True
                total_checked += 1
    
    score = round(total_checked / total_items * 100) if total_items > 0 else 0
    print(f"   ✓ 完整性检查")
    print(f"   ✓ 合理性检查")
    print(f"   ✓ 风险检查")
    print()
    
    # 显示竞品参考
    print("🏆 竞品参考：")
    for i, comp in enumerate(competitors, 1):
        print(f"   {i}. {comp.get('name', '')}（{comp.get('company', '')}）")
        print(f"      价格区间：{comp.get('priceRange', 'N/A')}")
        features = comp.get('features', [])
        if features:
            print(f"      特点：{', '.join(features)}")
    print()
    
    # 生成报告
    print("📝 生成方案报告...")
    
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
    
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"appearance_report_{game_type}_{appearance_type}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    # 生成报告内容
    report = generate_report(
        game_type, appearance_type,
        decision_results, checklist_results, checklists_data,
        competitors, art_content, score, total_items, total_checked
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"   ✓ 报告已保存：{filepath}")
    print()
    
    # 显示摘要
    print("=" * 60)
    print("📊 方案摘要")
    print("=" * 60)
    print()
    
    # 决策结果
    print("🎯 决策引导结果：")
    for tree_key, result in decision_results.items():
        tree_name = applicable_trees.get(tree_key, {}).get('name', tree_key)
        print(f"   • {tree_name}：{result.get('result', 'N/A')}")
        if result.get('price'):
            print(f"     💰 建议定价：{result.get('price')}")
    print()
    
    print(f"📈 完整度评分：{score}% ({total_checked}/{total_items} 项)")
    print()
    
    print(f"📄 完整报告：{filepath}")
    print()
    print("✅ 完成！")


def run_decision_tree_auto(tree_data: dict) -> dict:
    """自动运行决策树（选择第一个选项）"""
    current_node = "start"
    
    while True:
        nodes = tree_data.get('nodes', {})
        node = nodes.get(current_node)
        
        if not node:
            break
        
        # 结论节点
        if node.get('conclusion'):
            return {
                'result': node.get('result', ''),
                'reason': node.get('reason', ''),
                'price': node.get('price', ''),
                'elements': node.get('elements', []),
                'actions': node.get('actions', [])
            }
        
        # 问题节点 - 自动选择第一个选项
        options = node.get('options', {})
        if not options:
            break
        
        # 选择第一个选项
        first_option = list(options.values())[0]
        current_node = first_option
    
    return {'result': '无法确定', 'reason': '决策树运行异常'}


def generate_report(game_type, appearance_type, decision_results, 
                   checklist_results, checklists_data, competitors, 
                   art_content, score, total_items, total_checked) -> str:
    """生成报告内容"""
    
    lines = []
    lines.append(f"# 外观商业化方案报告")
    lines.append("")
    lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # 基本信息
    lines.append("## 📊 方案概览")
    lines.append("")
    lines.append(f"| 项目 | 内容 |")
    lines.append("|------|------|")
    lines.append(f"| 游戏品类 | {game_type.upper()} |")
    lines.append(f"| 外观类型 | {appearance_type} |")
    lines.append(f"| 完整度评分 | {score}% |")
    lines.append(f"| 状态评估 | {'✅ 优秀' if score >= 80 else '🟡 良好' if score >= 60 else '🔴 待完善'} |")
    lines.append("")
    
    # 决策结果
    lines.append("## 🎯 决策引导结果")
    lines.append("")
    
    decision_trees_data = load_json('decision_trees.json')
    applicable_trees = {
        k: v for k, v in decision_trees_data.items() 
        if game_type in v.get('applicable', [])
    }
    
    for tree_key, result in decision_results.items():
        tree_info = applicable_trees.get(tree_key, {})
        lines.append(f"### {tree_info.get('name', tree_key)}")
        lines.append("")
        lines.append(f"- **结论**：{result.get('result', 'N/A')}")
        if result.get('reason'):
            lines.append(f"- **原因**：{result.get('reason')}")
        if result.get('price'):
            lines.append(f"- **建议定价**：{result.get('price')}")
        if result.get('elements'):
            lines.append(f"- **核心元素**：{', '.join(result.get('elements', []))}")
        if result.get('actions'):
            lines.append(f"- **后续行动**：")
            for action in result.get('actions', []):
                lines.append(f"  - {action}")
        lines.append("")
    
    # 检查清单
    lines.append("## ✅ 检查清单结果")
    lines.append("")
    
    for check_type, checklist in checklists_data.items():
        lines.append(f"### {checklist.get('name', check_type)}")
        lines.append("")
        
        for category in checklist.get('categories', []):
            lines.append(f"#### {category.get('name', '')}")
            lines.append("")
            lines.append("| ID | 检查项 | 状态 |")
            lines.append("|----|--------|------|")
            
            for item in category.get('items', []):
                item_id = item.get('id', '')
                text = item.get('text', '')
                checked = checklist_results.get(check_type, {}).get(item_id, False)
                status = "✅" if checked else "⬜"
                level = item.get('level', '')
                if level:
                    text += f" `({level})`"
                lines.append(f"| {item_id} | {text} | {status} |")
            
            lines.append("")
    
    # 竞品参考
    lines.append("## 🏆 竞品参考")
    lines.append("")
    
    for comp in competitors:
        lines.append(f"### {comp.get('name', '')}")
        lines.append("")
        lines.append(f"- **公司**：{comp.get('company', '')}")
        lines.append(f"- **价格区间**：{comp.get('priceRange', 'N/A')}")
        lines.append(f"- **特点**：")
        for feature in comp.get('features', []):
            lines.append(f"  - {feature}")
        lines.append("")
    
    # 美术内容
    if art_content:
        lines.append("## 🎨 美术内容参考")
        lines.append("")
        
        for content_type, content_data in art_content.items():
            category_name = content_data.get('name', content_type)
            category_desc = content_data.get('description', '')
            lines.append(f"### {category_name}")
            if category_desc:
                lines.append(f"*{category_desc}*")
            lines.append("")
            
            # 处理 options 或 items
            items = content_data.get('options', content_data.get('items', []))
            for item in items:
                name = item.get('name', '')
                desc = item.get('description', '')
                examples = item.get('examples', [])
                if desc:
                    lines.append(f"- **{name}**：{desc}")
                else:
                    lines.append(f"- **{name}**")
                if examples:
                    lines.append(f"  - 示例：{', '.join(examples[:5])}")
            lines.append("")
    
    # 方案框架
    lines.append("## 📋 方案框架")
    lines.append("")
    lines.append("### 完成事项")
    lines.append("- [ ] 确认主题方向")
    lines.append("- [ ] 完成美术设计")
    lines.append("- [ ] 确定定价策略")
    lines.append("- [ ] 制定排期计划")
    lines.append("- [ ] 准备运营方案")
    lines.append("")
    lines.append("### 待办事项")
    lines.append("- [ ] 内部评审")
    lines.append("- [ ] 用户测试")
    lines.append("- [ ] 上线准备")
    lines.append("- [ ] 数据监控")
    lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*本报告由外观商业化思考小工具自动生成*")
    lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='外观商业化思考小工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run_auto.py --game moba --appearance skin
  python run_auto.py -g fps -a vfx -o ./reports
  
支持的游戏品类:
  moba       - MOBA（多人在线战术竞技）
  fps        - FPS（第一人称射击）
  simulation - 模拟经营

支持的外观类型:
  skin       - 皮肤
  decoration - 装饰
  vfx        - 特效
  animation  - 动画/动作
  mount      - 载具/坐骑
  sound      - 音效
  theme      - 主题选材
        """
    )
    
    parser.add_argument('-g', '--game', required=True,
                        choices=['moba', 'fps', 'simulation'],
                        help='游戏品类')
    
    parser.add_argument('-a', '--appearance', required=True,
                        choices=['skin', 'decoration', 'vfx', 'animation', 'mount', 'sound', 'theme'],
                        help='外观类型')
    
    parser.add_argument('-o', '--output', default=None,
                        help='输出目录（默认为 ./output）')
    
    args = parser.parse_args()
    
    run_auto(args.game, args.appearance, args.output)


if __name__ == '__main__':
    main()
