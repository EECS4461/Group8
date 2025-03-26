import solara
from mesa.examples.advanced.wolf_sheep.agents import GrassPatch, Sheep, Wolf
from mesa.examples.advanced.wolf_sheep.model import WolfSheep
from mesa.experimental.devs import ABMSimulator
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "size": 25,
    }

    if isinstance(agent, Wolf):
        portrayal["color"] = "#FFD700"
        portrayal["marker"] = "o"
        portrayal["zorder"] = 2
    elif isinstance(agent, Sheep):
        portrayal["color"] = "#00FF00"
        portrayal["marker"] = "^"
        portrayal["zorder"] = 2
    elif isinstance(agent, GrassPatch):
        if agent.fully_grown:
            portrayal["color"] = "tab:red"
        else:
            portrayal["color"] = "tab:blue"
        portrayal["marker"] = "s"
        portrayal["size"] = 55

    return portrayal


model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "grass": {
        "type": "Select",
        "value": True,
        "values": [True, False],
        "label": "Platform AI detection disabled?",
    },
    "grass_regrowth_time": Slider("ADBot Engagement Rate", 20, 1, 50),
    "initial_sheep": Slider("Initial Number of ADBots", 100, 10, 300),
    "sheep_reproduce": Slider("ADBot Coordination Rate", 0.04, 0.01, 1.0, 0.01),
    "initial_wolves": Slider("Initial Human Users", 10, 5, 100),
    "wolf_reproduce": Slider(
        "Human Report Torlerance",
        0.05,
        0.01,
        1.0,
        0.01,
    ),
    "wolf_gain_from_food": Slider("User Payment Rate from AD", 20, 1, 50),
    "sheep_gain_from_food": Slider("ADBot Evasion strategy", 4, 1, 10),
}


def post_process_space(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def post_process_lines(ax):
    handles, labels = ax.get_legend_handles_labels()
    # 映射原始字段名到新标签
    label_mapping = {
        "Wolves": "Purchases driven by AD",
        "Sheep": "Number of Undetected Bots",
        "Grass": "Number of Detected ADPost"
    }
    # 替换图例文本
    ax.legend(
        handles,
        [label_mapping.get(l, l) for l in labels],
        loc="center left",
        bbox_to_anchor=(1, 0.9)
    )


space_component = make_space_component(
    wolf_sheep_portrayal, draw_grid=False, post_process=post_process_space
)



lineplot_component = make_plot_component(
    {"Wolves": "tab:orange", "Sheep": "tab:cyan", "Grass": "tab:green"},
    post_process=post_process_lines,
)

simulator = ABMSimulator()
model = WolfSheep(simulator=simulator, grass=True)


page = SolaraViz(
    model,
    components=[space_component, lineplot_component],
    model_params=model_params,
    name="REDNote ADBot Eco Simulation",
    simulator=simulator,
)
page  # noqa
