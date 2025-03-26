import numpy as np
from mesa.visualization import SolaraViz, make_space_component, make_plot_component, Slider
from mesa.visualization.components import SpaceMatplotlib

from model import SocialMediaModel
from agents import OriginPost, AdBotAgent, ShillBotAgent, UserAgent


def agent_portrayal(agent):
    """根据代理类型返回不同的可视化效果"""
    if isinstance(agent, OriginPost):
        # 根据热度调整颜色深浅
        heat_color = min(1.0, agent.heat / 50.0)
        return {
            "color": "red",  # 使用字符串颜色名称
            "size": 25,
            "marker": "s",  # 使用字符串标记 (square)
            "layer": 0,
        }
    elif isinstance(agent, AdBotAgent):
        return {
            "color": "blue",
            "size": 15,
            "marker": "^",  # 使用字符串标记 (triangle up)
            "layer": 1,
        }
    elif isinstance(agent, ShillBotAgent):
        return {
            "color": "orange",
            "size": 15,
            "marker": "v",  # 使用字符串标记 (triangle down)
            "layer": 1,
        }
    elif isinstance(agent, UserAgent):
        # 根据engagement和trust调整颜色
        engagement_color = min(1.0, agent.engagement)
        return {
            "color": "green",
            "size": 15,
            "marker": "o",  # 使用字符串标记 (circle)
            "layer": 1,
        }


# 创建空间组件
space_component = SpaceMatplotlib(agent_portrayal, 500, 500)

# 创建图表组件
plot_heat_component = make_plot_component(
    ["Average Post Heat"],
    "帖子热度随时间变化",
    "matplotlib"
)

plot_bots_component = make_plot_component(
    ["Active Bots"],
    "活跃机器人数量随时间变化",
    "matplotlib"
)

# 模型参数
model_params = {
    "num_op": Slider("Original Posts", 20, 10, 100, 1),
    "num_ads": Slider("Ad Bots", 30, 10, 100, 1),
    "num_shills": Slider("Shill Bots", 50, 10, 200, 5),
    "num_users": Slider("Users", 100, 50, 300, 10),
    "detection": Slider("Detection", 0.5, 0.1, 1.0, 0.1)
}

model = SocialMediaModel()

# 创建SolaraViz实例 - 使用新的参数结构
viz = SolaraViz(
    model,
    components=[space_component, plot_bots_component, plot_heat_component],
    model_params=model_params,
    name="rednote ADbot Simulation"
)

# 最后返回可视化对象
viz  # noqa
# Added Page variable for SolaraViz page export
Page = viz
