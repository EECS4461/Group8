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
        """Placeholder for Bot behaviors."""
        self.interactions += 1

class AuditingAIAgent(Agent):
    def __init__(self, model):
        super().__init__(model)

    def step(self):
        """Placeholder for Auditing AI detection logic."""
        pass

class HumanUserAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.engagement = 0

    def step(self):
        """Placeholder for Human user engagement."""
        self.engagement += 1

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
        detection=0.5,    # detection probability
        seed=None
    ):
        super().__init__(seed=seed)
        # ContinuousSpace is used here, though the default Mesa 3.0 Matplotlib drawer
        # does not natively support continuous space. This code is illustrative.
        self.space = ContinuousSpace(width, height, True)

        self.num_op = num_op
        self.num_ads = num_ads
        self.num_shills = num_shills
        self.num_users = num_users
        self.detection = detection

        # DataCollector for our Key Metrics:
        self.datacollector = DataCollector(
            model_reporters={
                # Key metrics:
                "Number of Undetected Bots": lambda m: sum(
                    isinstance(a, BotAgent) and not a.detected for a in m.agents
                ),
                "Purchases Attributed to Bots": lambda m: int(
                    # Just random for demonstration
                    m.random.random() * 50
                ),
                "User Engagement": lambda m: sum(
                    a.engagement for a in m.agents if isinstance(a, HumanUserAgent)
                ),
                "Detection Rate": lambda m: round(m.random.random(), 2),
                "Evasion Rate": lambda m: round(m.random.random(), 2),
            }
        )

        # Create some Bot agents (advertising + shills) + Auditing AI + human users
        # For demonstration, we won't differentiate AdBots vs ShillBots in code, but
        # you could easily do so by creating different classes or flags.

        # 1. Bot Agents (combining ads + shills for simplicity)
        total_bots = self.num_ads + self.num_shills
        for _ in range(total_bots):
            agent = BotAgent(self)
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            self.space.place_agent(agent, (x, y))

        # 2. Auditing AI Agents
        # This might also be distributed, or we can have one big AI agent, etc.
        for _ in range(5):  # just a small fixed number for demonstration
            ai = AuditingAIAgent(self)
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            self.space.place_agent(ai, (x, y))

        # 3. Human Users
        for _ in range(self.num_users):
            user = HumanUserAgent(self)
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            self.space.place_agent(user, (x, y))

    def step(self):
        # Shuffle and do 'step' for all agents
        self.agents.shuffle_do("step")
        # Collect data
        self.datacollector.collect(self)

#############################################
# Visualization
#############################################

def agent_portrayal(agent):
    """
    A function that returns portrayal dictionary for each agent type.
    We'll color them based on the classes and optionally scale sizes.
    """
    portrayal = {}
    if isinstance(agent, BotAgent):
        # Vary radius by interactions for demonstration
        r_size = 0.5 + 0.01 * agent.interactions
        color = "red" if not agent.detected else "gray"
        portrayal = {
            "Shape": "circle",
            "Color": color,
            "r": r_size,
            "Layer": 0
        }
    elif isinstance(agent, AuditingAIAgent):
        portrayal = {
            "Shape": "rect",
            "Color": "blue",
            "w": 0.8,
            "h": 0.8,
            "Layer": 1
        }
    elif isinstance(agent, HumanUserAgent):
        portrayal = {
            "Shape": "circle",
            "Color": "green",
            "r": 0.4,
            "Layer": 0
        }
    return portrayal

# We'll create multiple plots for demonstration:
# 1) Plot of multiple Bot-related metrics
# 2) Plot of user engagement, detection & evasion rates

plot_bots_component = make_plot_component(
    ["Number of Undetected Bots", "Purchases Attributed to Bots"]
)

plot_rates_component = make_plot_component(
    ["Detection Rate", "Evasion Rate", "User Engagement"]
)

# A note on the space visualization: the default make_space_component with
# backend="matplotlib" doesn't natively support ContinuousSpace.
# This code is an example and may lead to a runtime error in Mesa 3.0.
# For continuous space, a custom or alternative approach is required.

space_component = make_space_component(agent_portrayal, backend="matplotlib", canvas_size=(500, 500))

# Model Parameters - using Sliders to dynamically create model instance
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
