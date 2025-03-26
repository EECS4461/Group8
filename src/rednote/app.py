# app.py 修改建议：
from agents import OriginalPost, AdPost, HumanUser, AdBot
from model import SocialMediaModel
from mesa.experimental.devs import ABMSimulator
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)

def social_media_portrayal(agent):
    if isinstance(agent, OriginalPost):
        return {"Shape": "star", "Color": "red", "r": 8}
    elif isinstance(agent, AdPost):
        return {
            "Shape": "rect",
            "Color": "blue",
            "Filled": True,
            "Layer": 2,
            "w": agent.influence_radius*2,
            "h": agent.influence_radius*2
        }
    elif isinstance(agent, AdBot):
        return {"Shape": "triangle", "Color": "green", "r": 6}
    elif isinstance(agent, HumanUser):
        return {"Shape": "circle", "Color": "yellow", "r": 4}

# 新增控制参数
model_params = {
    "report_threshold": Slider("举报阈值", 5, 1, 20),
    "detection_interval": Slider("检测间隔", 100, 50, 200),
    "initial_bots": Slider("初始机器人数量", 20, 5, 50),
    "initial_humans": Slider("初始用户数量", 50, 10, 100)
}


def post_process_space(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def post_process_lines(ax):
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.9))

space_component = make_space_component(
    social_media_portrayal, draw_grid=False, post_process=post_process_space
)

# 新增统计组件
lineplot_component = make_plot_component({
    "Active_Bots": "tab:green",
    "Purchases": "tab:orange",
    "Detection_Rate": "tab:red",
    "Ad_Influence": "tab:purple"
})


simulator = ABMSimulator()
model = SocialMediaModel()

page = SolaraViz(
    model,
    components=[space_component, lineplot_component],
    model_params=model_params,
    name="redNote ADBot",
    simulator=simulator,
)
page  # noqa
