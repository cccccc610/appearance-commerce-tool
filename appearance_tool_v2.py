#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外观商业化思考小工具 v2.0
面向美术策划运营复合型岗位

功能：
1. 竞品分析参考
2. 美术内容规划
3. 运营策略建议
4. 风险检查清单
5. 方案报告生成

使用方式：
    python appearance_tool_v2.py --game moba --appearance skin --output ./output
"""

import json
import os
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def load_config() -> dict:
    """加载配置文件"""
    config_path = os.path.join(DATA_DIR, 'config_v2.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class AppearanceCommerceToolV2:
    """外观商业化思考小工具 v2.0"""
    
    def __init__(self):
        self.config = load_config()
        self.game_type = None
        self.appearance_type = None
        self.user_inputs = {}
        self.results = {}
    
    def run(self, game_type: str, appearance_type: str, 
            theme: str = None, quality: str = None) -> dict:
        """运行工具"""
        
        self.game_type = game_type
        self.appearance_type = appearance_type
        self.user_inputs = {
            'theme': theme,
            'quality': quality
        }
        
        # 获取品类配置
        game_config = self.config.get(game_type, {})
        if not game_config:
            return {'error': f'不支持的游戏品类: {game_type}'}
        
        # 1. 获取竞品参考
        self.results['competitors'] = self._get_competitor_analysis(game_config)
        
        # 2. 获取美术内容参考
        self.results['art_content'] = self._get_art_content(game_config)
        
        # 3. 获取运营策略参考
        self.results['operation'] = self._get_operation_strategy(game_config)
        
        # 4. 获取参考资源链接
        self.results['reference_links'] = self._get_reference_links()
        
        # 5. 风险检查
        self.results['risks'] = self._get_risk_checklist()
        
        # 6. 思考框架
        self.results['thinking'] = self._get_thinking_framework()
        
        return self.results
    
    def _get_competitor_analysis(self, game_config: dict) -> list:
        """获取竞品分析"""
        competitors = game_config.get('competitors', [])
        result = []
        
        for comp in competitors:
            analysis = {
                'name': comp.get('name', ''),
                'company': comp.get('company', ''),
                'pricing_model': comp.get('pricing_model', ''),
                'price_range': comp.get('price_range', {}),
                'key_features': comp.get('key_features', []),
                'success_cases': comp.get('success_cases', []),
                'reference_links': comp.get('reference_links', []),
                'insights': self._generate_competitor_insights(comp)
            }
            result.append(analysis)
        
        return result
    
    def _generate_competitor_insights(self, comp: dict) -> list:
        """生成竞品洞察"""
        insights = []
        
        # 价格洞察
        price_range = comp.get('price_range', {})
        if price_range:
            insights.append(f"定价策略：从{list(price_range.values())[0]}到{list(price_range.values())[-1]}的阶梯式定价")
        
        # 成功案例洞察
        success_cases = comp.get('success_cases', [])
        for case in success_cases[:2]:
            insights.append(f"成功案例：{case.get('name', '')} - {case.get('key', '')}")
        
        # 特色功能洞察
        features = comp.get('key_features', [])
        if features:
            insights.append(f"核心特色：{', '.join(features[:3])}")
        
        return insights
    
    def _get_art_content(self, game_config: dict) -> dict:
        """获取美术内容参考"""
        art_categories = game_config.get('art_categories', {})
        result = {}
        
        for category_name, category_data in art_categories.items():
            result[category_name] = {
                'description': category_data.get('description', ''),
                'dimensions': category_data.get('dimensions', []),
                'reference_search': category_data.get('reference_search', []),
                'recommendations': self._generate_art_recommendations(category_name, category_data)
            }
        
        return result
    
    def _generate_art_recommendations(self, category_name: str, category_data: dict) -> list:
        """生成美术建议"""
        recommendations = []
        
        dimensions = category_data.get('dimensions', [])
        for dim in dimensions:
            name = dim.get('name', '')
            options = dim.get('options', [])
            spec = dim.get('spec', '')
            
            if options:
                recommendations.append(f"{name}：{', '.join(options[:5])}")
            if spec:
                recommendations.append(f"  └ {spec}")
        
        return recommendations
    
    def _get_operation_strategy(self, game_config: dict) -> dict:
        """获取运营策略参考"""
        operation_features = game_config.get('operation_features', {})
        result = {}
        
        for feature_name, feature_data in operation_features.items():
            result[feature_name] = {
                'description': feature_data.get('description', ''),
                'dimensions': feature_data.get('dimensions', []),
                'recommendations': []
            }
            
            dimensions = feature_data.get('dimensions', [])
            for dim in dimensions:
                name = dim.get('name', '')
                options = dim.get('options', [])
                spec = dim.get('spec', '')
                
                rec = f"【{name}】"
                if options:
                    rec += f" {', '.join(options)}"
                if spec:
                    rec += f" - {spec}"
                result[feature_name]['recommendations'].append(rec)
        
        return result
    
    def _get_reference_links(self) -> dict:
        """获取参考资源链接"""
        return self.config.get('reference_links', {})
    
    def _get_risk_checklist(self) -> dict:
        """获取风险检查清单"""
        frameworks = self.config.get('thinking_frameworks', {})
        risk_framework = frameworks.get('风险检查框架', {})
        return risk_framework
    
    def _get_thinking_framework(self) -> dict:
        """获取思考框架"""
        frameworks = self.config.get('thinking_frameworks', {})
        return frameworks.get('商业化判断框架', {})
    
    def generate_report(self, output_dir: str = None) -> str:
        """生成报告"""
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), 'output')
        
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"appearance_report_v2_{self.game_type}_{self.appearance_type}_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)
        
        report = self._build_report()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filepath
    
    def _build_report(self) -> str:
        """构建报告内容"""
        lines = []
        
        # 标题
        game_name = self.config.get(self.game_type, {}).get('name', self.game_type)
        lines.append(f"# 外观商业化方案报告")
        lines.append("")
        lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"> 游戏品类：{game_name}")
        lines.append(f"> 外观类型：{self.appearance_type}")
        if self.user_inputs.get('theme'):
            lines.append(f"> 主题方向：{self.user_inputs['theme']}")
        if self.user_inputs.get('quality'):
            lines.append(f"> 品质定位：{self.user_inputs['quality']}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # 参考资源链接
        lines.append("## 🔗 参考资源")
        lines.append("")
        lines.append("### 美术参考网站")
        lines.append("")
        ref_links = self.results.get('reference_links', {})
        art_refs = ref_links.get('美术参考', {})
        for name, info in art_refs.items():
            url = info.get('url', '')
            desc = info.get('description', '')
            usage = info.get('usage', '')
            lines.append(f"- **[{name}]({url})**")
            lines.append(f"  - {desc}")
            if usage:
                lines.append(f"  - 用法：{usage}")
        lines.append("")
        
        lines.append("### 市场/运营参考")
        lines.append("")
        market_refs = ref_links.get('市场参考', {})
        market_refs.update(ref_links.get('运营资源', {}))
        for name, info in market_refs.items():
            url = info.get('url', '')
            desc = info.get('description', '')
            lines.append(f"- **[{name}]({url})** - {desc}")
        lines.append("")
        
        lines.append("### 游戏资讯")
        lines.append("")
        game_refs = ref_links.get('游戏资讯', {})
        for name, info in game_refs.items():
            url = info.get('url', '')
            desc = info.get('description', '')
            lines.append(f"- **[{name}]({url})** - {desc}")
        lines.append("")
        
        # 竞品分析
        lines.append("## 🏆 竞品分析")
        lines.append("")
        competitors = self.results.get('competitors', [])
        for i, comp in enumerate(competitors, 1):
            lines.append(f"### {i}. {comp['name']}（{comp['company']}）")
            lines.append("")
            lines.append(f"**定价模式**：{comp['pricing_model']}")
            lines.append("")
            
            if comp['price_range']:
                lines.append("**价格区间**：")
                lines.append("| 等级 | 价格 |")
                lines.append("|------|------|")
                for level, price in comp['price_range'].items():
                    lines.append(f"| {level} | {price} |")
                lines.append("")
            
            if comp['key_features']:
                lines.append("**核心特色**：")
                for feature in comp['key_features']:
                    lines.append(f"- {feature}")
                lines.append("")
            
            if comp['success_cases']:
                lines.append("**成功案例**：")
                for case in comp['success_cases']:
                    lines.append(f"- **{case['name']}**（{case['type']}）")
                    lines.append(f"  - 销量：{case['sales']}")
                    lines.append(f"  - 关键成功因素：{case['key']}")
                lines.append("")
            
            if comp['insights']:
                lines.append("**💡 洞察要点**：")
                for insight in comp['insights']:
                    lines.append(f"- {insight}")
                lines.append("")
            
            if comp['reference_links']:
                lines.append("**参考链接**：")
                for link in comp['reference_links']:
                    lines.append(f"- {link}")
                lines.append("")
        
        # 美术内容
        lines.append("## 🎨 美术内容规划")
        lines.append("")
        art_content = self.results.get('art_content', {})
        for category_name, category_data in art_content.items():
            lines.append(f"### {category_name}")
            lines.append("")
            desc = category_data.get('description', '')
            if desc:
                lines.append(f"*{desc}*")
                lines.append("")
            
            dimensions = category_data.get('dimensions', [])
            if dimensions:
                lines.append("| 维度 | 选项 | 说明 |")
                lines.append("|------|------|------|")
                for dim in dimensions:
                    name = dim.get('name', '')
                    options = dim.get('options', [])
                    spec = dim.get('spec', '')
                    options_str = ', '.join(options[:4]) if options else ''
                    lines.append(f"| {name} | {options_str} | {spec} |")
                lines.append("")
            
            ref_search = category_data.get('reference_search', [])
            if ref_search:
                lines.append("**🔍 搜索参考**：")
                for search in ref_search:
                    lines.append(f"- {search}")
                lines.append("")
        
        # 运营策略
        lines.append("## 📊 运营策略建议")
        lines.append("")
        operation = self.results.get('operation', {})
        for feature_name, feature_data in operation.items():
            lines.append(f"### {feature_name}")
            lines.append("")
            desc = feature_data.get('description', '')
            if desc:
                lines.append(f"*{desc}*")
                lines.append("")
            
            recommendations = feature_data.get('recommendations', [])
            for rec in recommendations:
                lines.append(f"- {rec}")
            lines.append("")
        
        # 思考框架
        lines.append("## 💭 商业化判断框架")
        lines.append("")
        thinking = self.results.get('thinking', {})
        if thinking:
            desc = thinking.get('description', '')
            if desc:
                lines.append(f"*{desc}*")
                lines.append("")
            
            dimensions = thinking.get('dimensions', [])
            for dim in dimensions:
                name = dim.get('name', '')
                questions = dim.get('questions', [])
                lines.append(f"### {name}")
                lines.append("")
                for q in questions:
                    lines.append(f"- [ ] {q}")
                lines.append("")
        
        # 风险检查
        lines.append("## ⚠️ 风险检查清单")
        lines.append("")
        risks = self.results.get('risks', {})
        if risks:
            desc = risks.get('description', '')
            if desc:
                lines.append(f"*{desc}*")
                lines.append("")
            
            risk_categories = risks.get('risk_categories', [])
            for risk in risk_categories:
                name = risk.get('name', '')
                level = risk.get('level', '')
                items = risk.get('items', [])
                
                level_emoji = {'严重': '🔴', '高': '🟠', '中': '🟡', '低': '🟢'}.get(level, '⚪')
                
                lines.append(f"### {level_emoji} {name}（风险等级：{level}）")
                lines.append("")
                for item in items:
                    lines.append(f"- [ ] {item}")
                lines.append("")
        
        # 方案框架
        lines.append("## 📋 方案框架")
        lines.append("")
        lines.append("### 完成事项")
        lines.append("- [ ] 确定目标角色/武器")
        lines.append("- [ ] 确定主题方向")
        lines.append("- [ ] 确定品质等级")
        lines.append("- [ ] 完成美术设计稿")
        lines.append("- [ ] 确定定价策略")
        lines.append("- [ ] 制定上线排期")
        lines.append("- [ ] 准备运营方案")
        lines.append("")
        lines.append("### 待办事项")
        lines.append("- [ ] 内部评审")
        lines.append("- [ ] 用户测试")
        lines.append("- [ ] 技术验证")
        lines.append("- [ ] 法务审核")
        lines.append("- [ ] 上线准备")
        lines.append("- [ ] 数据监控方案")
        lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append("*本报告由外观商业化思考小工具 v2.0 自动生成*")
        lines.append("*适用对象：美术策划运营复合型岗位*")
        lines.append("")
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='外观商业化思考小工具 v2.0 - 美术策划运营复合型岗位专用',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python appearance_tool_v2.py --game moba --appearance skin
  python appearance_tool_v2.py -g fps -a weapon_skin --theme 科幻 --quality 传说
  python appearance_tool_v2.py -g simulation -a home_decor -o ./reports

支持的游戏品类:
  moba       - MOBA（多人在线战术竞技）
  fps        - FPS（第一人称射击）
  simulation - 模拟经营

支持的外观类型:
  moba: skin(皮肤), decoration(装饰), vfx(特效), animation(动画), sound(音效)
  fps: weapon_skin(武器皮肤), character_skin(角色皮肤), vfx(特效)
  simulation: character_skin(角色皮肤), home_decor(家园装饰), mount(坐骑), theme(主题套装)
        """
    )
    
    parser.add_argument('-g', '--game', required=True,
                        choices=['moba', 'fps', 'simulation'],
                        help='游戏品类')
    
    parser.add_argument('-a', '--appearance', required=True,
                        help='外观类型')
    
    parser.add_argument('-t', '--theme', default=None,
                        help='主题方向（可选）')
    
    parser.add_argument('-q', '--quality', default=None,
                        help='品质等级（可选）')
    
    parser.add_argument('-o', '--output', default=None,
                        help='输出目录（默认为 ./output）')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🎨 外观商业化思考小工具 v2.0")
    print("   面向美术策划运营复合型岗位")
    print("=" * 70)
    print()
    
    # 运行工具
    tool = AppearanceCommerceToolV2()
    results = tool.run(
        game_type=args.game,
        appearance_type=args.appearance,
        theme=args.theme,
        quality=args.quality
    )
    
    if 'error' in results:
        print(f"❌ {results['error']}")
        return
    
    print(f"📌 游戏品类：{tool.config.get(args.game, {}).get('name', args.game)}")
    print(f"🎨 外观类型：{args.appearance}")
    if args.theme:
        print(f"🎭 主题方向：{args.theme}")
    if args.quality:
        print(f"⭐ 品质等级：{args.quality}")
    print()
    
    # 生成报告
    print("📝 生成方案报告...")
    filepath = tool.generate_report(args.output)
    print(f"   ✓ 报告已保存：{filepath}")
    print()
    
    # 显示摘要
    print("=" * 70)
    print("📊 竞品分析摘要")
    print("=" * 70)
    print()
    
    for comp in results.get('competitors', [])[:3]:
        print(f"• {comp['name']}（{comp['company']}）")
        for insight in comp.get('insights', [])[:2]:
            print(f"  └ {insight}")
    print()
    
    print(f"📄 完整报告：{filepath}")
    print()
    print("✅ 完成！")


if __name__ == '__main__':
    main()
