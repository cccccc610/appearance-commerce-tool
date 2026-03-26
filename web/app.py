#!/usr/bin/env python3
"""
外观商业化思考小工具 - Web后端服务
提供API接口和静态文件服务
"""

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import os

# 导入AI分析模块
from ai_analyzer_mvp import analyzer

# 初始化Flask应用
app = Flask(__name__, static_folder='.')
CORS(app)

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


def load_json(filename):
    """加载JSON数据文件"""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


# ==================== 页面路由 ====================

@app.route('/')
def index():
    """主页"""
    return send_from_directory('.', 'index.html')


# ==================== API路由 ====================

@app.route('/api/game-types', methods=['GET'])
def get_game_types():
    """获取游戏品类列表"""
    return jsonify({
        'status': 'success',
        'data': {
            'moba': {'name': 'MOBA', 'fullName': '多人在线战术竞技'},
            'fps': {'name': 'FPS', 'fullName': '第一人称射击'},
            'simulation': {'name': '模拟经营', 'fullName': '经营养成类游戏'}
        }
    })


@app.route('/api/appearance-types', methods=['GET'])
def get_appearance_types():
    """获取外观类型列表"""
    return jsonify({
        'status': 'success',
        'data': {
            'skin': '皮肤',
            'decoration': '装饰',
            'vfx': '特效',
            'animation': '动画/动作',
            'mount': '载具/坐骑',
            'sound': '音效',
            'theme': '主题选材'
        }
    })


@app.route('/api/decision-trees/<game_type>', methods=['GET'])
def get_decision_trees(game_type):
    """获取指定品类的决策树"""
    try:
        trees = load_json('decision_trees.json')
        # 过滤适用于该品类的决策树
        filtered = {
            k: v for k, v in trees.items()
            if game_type in v.get('applicable', [])
        }
        return jsonify({
            'status': 'success',
            'data': filtered
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/checklists', methods=['GET'])
def get_checklists():
    """获取检查清单"""
    try:
        checklists = load_json('checklists.json')
        return jsonify({
            'status': 'success',
            'data': checklists
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/competitors/<game_type>', methods=['GET'])
def get_competitors(game_type):
    """获取竞品数据"""
    try:
        competitors = load_json('competitors.json')
        data = competitors.get(game_type, [])
        return jsonify({
            'status': 'success',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/art-content', methods=['GET'])
def get_art_content():
    """获取美术内容参考"""
    try:
        art_content = load_json('art_content.json')
        return jsonify({
            'status': 'success',
            'data': art_content
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """
    生成完整商业化案子（MVP版本）
    整合竞品分析、美术参考、市场趋势等AI分析能力
    """
    try:
        data = request.get_json()

        game_type = data.get('game_type')
        appearance_type = data.get('appearance_type')
        decisions = data.get('decisions', {})
        checklist = data.get('checklist', {})

        if not game_type or not appearance_type:
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数：game_type 和 appearance_type'
            }), 400

        # 使用AI分析模块生成完整方案
        result = analyzer.generate_business_plan(
            game_type=game_type,
            appearance_type=appearance_type,
            decisions=decisions,
            checklist=checklist
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'生成方案失败: {str(e)}'
        }), 500


@app.route('/api/analyze-competitors', methods=['POST'])
def analyze_competitors():
    """
    分析竞品

    请求体：
        {
            "game_type": "moba|fps|simulation",
            "appearance_type": "skin|decoration|vfx|..."
        }
    """
    try:
        data = request.get_json()
        game_type = data.get('game_type')
        appearance_type = data.get('appearance_type')

        if not game_type or not appearance_type:
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数'
            }), 400

        result = analyzer.analyze_competitors(game_type, appearance_type)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/generate-art-references', methods=['POST'])
def generate_art_references():
    """
    生成美术参考

    请求体：
        {
            "game_type": "moba|fps|simulation",
            "appearance_type": "skin|decoration|...",
            "theme": "可选主题"
        }
    """
    try:
        data = request.get_json()
        game_type = data.get('game_type')
        appearance_type = data.get('appearance_type')
        theme = data.get('theme')

        if not game_type or not appearance_type:
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数'
            }), 400

        result = analyzer.generate_art_references(game_type, appearance_type, theme)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/market-trends', methods=['POST'])
def get_market_trends():
    """
    获取市场趋势

    请求体：
        {
            "game_type": "moba|fps|simulation"
        }
    """
    try:
        data = request.get_json()
        game_type = data.get('game_type')

        if not game_type:
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数'
            }), 400

        result = analyzer.get_market_trends(game_type)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(e):
    """404处理"""
    return jsonify({
        'status': 'error',
        'message': '资源未找到'
    }), 404


@app.errorhandler(500)
def server_error(e):
    """500处理"""
    return jsonify({
        'status': 'error',
        'message': '服务器内部错误'
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🎨 外观商业化思考小工具 - Web服务")
    print("=" * 60)
    print()
    print("服务已启动，访问地址：")
    print("  http://localhost:5001")
    print()
    print("API接口：")
    print("  GET  /api/game-types           - 获取游戏品类")
    print("  GET  /api/appearance-types     - 获取外观类型")
    print("  GET  /api/decision-trees/<game_type> - 获取决策树")
    print("  GET  /api/checklists           - 获取检查清单")
    print("  GET  /api/competitors/<game_type>    - 获取竞品数据")
    print("  GET  /api/art-content          - 获取美术内容")
    print("  POST /api/generate-report      - 生成报告")
    print()
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    
    # 启动服务
    app.run(host='0.0.0.0', port=5001, debug=True)
