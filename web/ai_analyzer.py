#!/usr/bin/env python3
"""
外观商业化工具 - AI分析模块
集成Coze Web搜索和内容抓取能力
"""

import subprocess
import json
import re
from typing import Dict, List, Optional
from datetime import datetime


class AIAnalyzer:
    """AI驱动的竞品分析和参考生成"""

    def __init__(self):
        self.search_results_cache = {}

    def run_openclaw_tool(self, tool_name: str, args: List[str]) -> Dict:
        """
        通过命令行调用OpenClaw工具

        Args:
            tool_name: 工具名称，如 'coze_web_search'
            args: 工具参数列表

        Returns:
            工具执行结果的JSON数据
        """
        try:
            # 构建命令
            cmd = ['openclaw', 'tools', tool_name] + args

            # 执行命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                return {
                    'status': 'error',
                    'message': f'工具执行失败: {result.stderr}'
                }

            # 解析输出（假设工具返回JSON）
            output = result.stdout.strip()
            try:
                return json.loads(output)
            except json.JSONDecodeError:
                # 如果不是JSON，返回原始文本
                return {
                    'status': 'success',
                    'data': output
                }

        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'message': '工具执行超时'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def search_competitors(self, game_type: str, appearance_type: str) -> Dict:
        """
        搜索竞品信息

        Args:
            game_type: 游戏品类（moba/fps/simulation）
            appearance_type: 外观类型（skin/decoration/vfx等）

        Returns:
            竞品分析结果
        """
        # 构建搜索关键词
        game_type_map = {
            'moba': 'MOBA游戏',
            'fps': 'FPS游戏',
            'simulation': '模拟经营游戏'
        }

        appearance_type_map = {
            'skin': '皮肤商业化',
            'decoration': '装饰系统',
            'vfx': '特效设计',
            'animation': '动画动作',
            'mount': '载具坐骑',
            'sound': '音效语音',
            'theme': '主题选材'
        }

        keyword = f"{game_type_map.get(game_type, game_type)} {appearance_type_map.get(appearance_type, appearance_type)}"

        # 使用coze_web_search搜索
        result = self.run_openclaw_tool('coze_web_search', [
            '--query', keyword,
            '--need-summary', 'true',
            '--need-content', 'true',
            '--count', '10'
        ])

        return result

    def search_art_references(self, game_type: str, appearance_type: str, theme: Optional[str] = None) -> Dict:
        """
        搜索美术参考

        Args:
            game_type: 游戏品类
            appearance_type: 外观类型
            theme: 可选的主题方向

        Returns:
            美术参考结果
        """
        # 构建搜索关键词
        theme_suffix = f" {theme}" if theme else ""
        keyword = f"{game_type}游戏 {appearance_type}设计参考{theme_suffix}"

        result = self.run_openclaw_tool('coze_web_search', [
            '--query', keyword,
            '--need-summary', 'true',
            '--count', '8'
        ])

        return result

    def search_market_trends(self, game_type: str) -> Dict:
        """
        搜索市场趋势

        Args:
            game_type: 游戏品类

        Returns:
            市场趋势分析
        """
        keyword = f"{game_type}游戏商业化趋势 2025"

        result = self.run_openclaw_tool('coze_web_search', [
            '--query', keyword,
            '--need-summary', 'true',
            '--count', '5'
        ])

        return result

    def generate_business_plan(
        self,
        game_type: str,
        appearance_type: str,
        decisions: Dict,
        checklist: Dict
    ) -> Dict:
        """
        生成完整的商业化案子

        Args:
            game_type: 游戏品类
            appearance_type: 外观类型
            decisions: 决策树结果
            checklist: 检查清单结果

        Returns:
            完整的商业化方案
        """
        # 先搜索竞品和趋势
        competitor_result = self.search_competitors(game_type, appearance_type)
        trend_result = self.search_market_trends(game_type)

        # 整合信息
        plan = {
            'meta': {
                'game_type': game_type,
                'appearance_type': appearance_type,
                'generated_at': datetime.now().isoformat()
            },
            'competitor_analysis': competitor_result.get('data', {}),
            'market_trends': trend_result.get('data', {}),
            'decisions': decisions,
            'checklist': checklist,
            'recommendations': self._generate_recommendations(
                game_type,
                appearance_type,
                decisions,
                checklist
            )
        }

        return {
            'status': 'success',
            'data': plan
        }

    def _generate_recommendations(
        self,
        game_type: str,
        appearance_type: str,
        decisions: Dict,
        checklist: Dict
    ) -> List[Dict]:
        """
        生成具体建议

        Returns:
            建议列表
        """
        recommendations = []

        # 基于决策树结果生成建议
        for tree_key, result in decisions.items():
            if isinstance(result, dict) and 'actions' in result:
                for action in result['actions']:
                    recommendations.append({
                        'source': f"决策树_{tree_key}",
                        'type': 'action',
                        'content': action,
                        'priority': 'high'
                    })

        # 基于检查清单生成建议
        for checklist_type, items in checklist.items():
            for item_id, checked in items.items():
                if not checked:
                    recommendations.append({
                        'source': f"检查清单_{checklist_type}",
                        'type': 'todo',
                        'content': f"完成检查项 {item_id}",
                        'priority': 'medium'
                    })

        return recommendations

    def fetch_art_from_pinterest(self, search_term: str) -> Dict:
        """
        从Pinterest获取美术参考

        Args:
            search_term: 搜索关键词

        Returns:
            Pinterest参考结果
        """
        url = f"https://jp.pinterest.com/search/pins/?q={search_term}"

        result = self.run_openclaw_tool('coze_web_fetch', [
            '--urls', url,
            '--format', 'json'
        ])

        return result

    def fetch_art_from_eagle(self, search_term: str) -> Dict:
        """
        从Eagle获取美术参考

        Args:
            search_term: 搜索关键词

        Returns:
            Eagle参考结果
        """
        url = f"https://cn.eagle.cool/search?q={search_term}"

        result = self.run_openclaw_tool('coze_web_fetch', [
            '--urls', url,
            '--format', 'json'
        ])

        return result


# 导出
analyzer = AIAnalyzer()
