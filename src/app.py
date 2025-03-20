import os
import sys
import numpy as np

from matplotlib.markers import MarkerStyle

sys.path.insert(0, os.path.abspath("../../../.."))

from mesa.visualization import Slider, SolaraViz, make_space_component
from agents import OriginPost, AdBotAgent, ShillBotAgent, UserAgent
from model import SocialMediaModel

# 预计算不同图标的缓存
MARKER_CACHE = {}
# 为原始帖子创建圆形标记
marker_post = MarkerStyle('o')
MARKER_CACHE['post'] = marker_post

# 为广告机器人创建三角形标记
marker_ad = MarkerStyle('^')
MARKER_CACHE['ad'] = marker_ad

# 为水军机器人创建方形标记
marker_shill = MarkerStyle('s')
MARKER_CACHE['shill'] = marker_shill

# 为用户创建菱形标记
marker_user = MarkerStyle('D')
MARKER_CACHE['user'] = marker_user


def agent_portrayal(agent):
    """根据代理类型返回不同的可视化效果"""
    if isinstance(agent, OriginPost):
        # 根据热度调整颜色深浅
        heat_color = min(1.0, agent.heat / 50.0)
        return {
            "color": [1.0, 0.6 * (1 - heat_color), 0.6 * (1 - heat_color)],
            "size": 25,
            "marker": MARKER_CACHE['post'],
            "layer": 0,
        }
    elif isinstance(agent, AdBotAgent):
        return {
            "color": "blue",
            "size": 15,
            "marker": MARKER_CACHE['ad'],
            "layer": 1,
        }
    elif isinstance(agent, ShillBotAgent):
        return {
            "color": "orange",
            "size": 15,
            "marker": MARKER_CACHE['shill'],
            "layer": 1,
        }
    elif isinstance(agent, UserAgent):
        # 根据engagement和trust调整颜色
        engagement_color = min(1.0, agent.engagement)
        return {
            "color": [0.2, 0.6, 0.2 + 0.4 * engagement_color],
            "size": 15,
            "marker": MARKER_CACHE['user'],
            "layer": 1,
        }


model_params = {
    "num_posts": Slider(
        label="num_op",
        value=5,
        min=1,
        max=20,
        step=1,
    ),
    "num_ads": Slider(
        label="num_ads",
        value=10,
        min=0,
        max=50,
        step=5,
    ),
    "num_shills": Slider(
        label="num_shills",
        value=15,
        min=0,
        max=50,
        step=5,
    ),
    "num_users": Slider(
        label="num_users",
        value=20,
        min=5,
        max=100,
        step=5,
    ),
    "width": 100,
    "height": 100,
}

# 创建模型实例
model = SocialMediaModel()

# 创建可视化页面
page = SolaraViz(
    model,
    components=[make_space_component(agent_portrayal=agent_portrayal, backend="matplotlib")],
    model_params=model_params,
    name="redNote ADBot Simulation",
)
page  # noqa
