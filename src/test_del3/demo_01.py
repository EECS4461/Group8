import numpy as np
from mesa import Model, Agent
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from mesa.visualization import SolaraViz, make_space_component, make_plot_component, Slider

#############################################
# Agents
#############################################

class BotAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.interactions = 0
        self.detected = False

    def step(self):
        """Example of Bot behaviors."""
        # For demonstration, just increment interactions
        self.interactions += 1
        # 其他可选：Boid运动、协同点赞等

class HumanUserAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.engagement = 0

    def step(self):
        """Example of Human user engagement."""
        self.engagement += 1
        # 其他可选：查看广告帖，可能举报等


#############################################
# Model
#############################################

class SocialMediaModel(Model):
    def __init__(
        self,
        width=50,
        height=50,
        num_op=20,        # e.g., origin posts or other content
        num_ads=20,       # e.g., advertising bots
        num_shills=15,    # e.g., shill bots
        num_users=50,     # real human users
        detection=0.5,    # detection probability or "audit strength"
        seed=None
    ):
        super().__init__(seed=seed)
        # ContinuousSpace 仍然保留
        self.space = ContinuousSpace(width, height, torus=True)

        self.num_op = num_op
        self.num_ads = num_ads
        self.num_shills = num_shills
        self.num_users = num_users
        self.detection = detection  # 用于控制全局检测概率或强度

        # DataCollector for Key Metrics:
        self.datacollector = DataCollector(
            model_reporters={
                "Number of Undetected Bots": lambda m: sum(
                    isinstance(a, BotAgent) and not a.detected for a in m.agents
                ),
                "Purchases Attributed to Bots": lambda m: int(
                    # Just a random placeholder
                    m.random.random() * 50
                ),
                "User Engagement": lambda m: sum(
                    a.engagement for a in m.agents if isinstance(a, HumanUserAgent)
                ),
                # 下面两项也只是演示
                "Detection Rate": lambda m: round(m.random.random(), 2),
                "Evasion Rate": lambda m: round(m.random.random(), 2),
            }
        )

        # 1) Create Bot Agents (Ad Bots + Shill Bots)
        total_bots = self.num_ads + self.num_shills
        for _ in range(total_bots):
            agent = BotAgent(self)
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            self.space.place_agent(agent, (x, y))

        # 2) Create Human Users
        for _ in range(self.num_users):
            user = HumanUserAgent(self)
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            self.space.place_agent(user, (x, y))

        # （可选）如果不需要“审核员Agent”，可注释掉所有 AuditingAIAgent 相关
        # 否则保留，但仅作展示或别的用途

    def step(self):
        """Single step of the overall simulation."""
        # 让所有 Agent 各自执行其 step
        self.agents.shuffle_do("step")

        # 全局环境级审核过程
        self.global_detection_step()

        # 收集数据
        self.datacollector.collect(self)

    def global_detection_step(self):
        """
        A global check for all BotAgents in the environment.
        Instead of having an AuditingAIAgent, we do a single pass here.
        """
        for agent in self.agents:
            if isinstance(agent, BotAgent):
                if not agent.detected:
                    # 示例：以 self.detection 作为基础概率
                    # 也可结合 agent.interactions、位置等更复杂逻辑
                    if self.random.random() < self.detection:
                        agent.detected = True


#############################################
# Visualization
#############################################

def agent_portrayal(agent):
    """
    Returns portrayal dict for each agent type.
    """
    if isinstance(agent, BotAgent):
        r_size = 0.5 + 0.01 * agent.interactions
        color = "red" if not agent.detected else "gray"
        portrayal = {
            "Shape": "circle",
            "Color": color,
            "r": r_size,
            "Layer": 0
        }
    elif isinstance(agent, HumanUserAgent):
        portrayal = {
            "Shape": "circle",
            "Color": "green",
            "r": 0.4,
            "Layer": 0
        }
    else:
        portrayal = {}
    return portrayal

plot_bots_component = make_plot_component(
    ["Number of Undetected Bots", "Purchases Attributed to Bots"]
)
plot_rates_component = make_plot_component(
    ["Detection Rate", "Evasion Rate", "User Engagement"]
)

# ContinuousSpace在 Mesa 3.0 用 matplotlib backend 可能有兼容性问题，仅做示例
space_component = make_space_component(agent_portrayal, backend="matplotlib", canvas_size=(500, 500))

model_params = {
    "width": 50,
    "height": 50,
    "num_op": Slider("Origin Post", 20, 10, 100, 1),
    "num_ads": Slider("Ad Bots", 20, 10, 100, 1),
    "num_shills": Slider("Shill Bots", 15, 5, 50, 1),
    "num_users": Slider("Users", 50, 20, 200, 10),
    "detection": Slider("Detection", 0.5, 0.1, 1.0, 0.1)
}

model = SocialMediaModel()

page = SolaraViz(
    model,
    components=[space_component, plot_bots_component, plot_rates_component],
    model_params=model_params,
    name="rednote ADbot Simulation"
)

page  # noqa
