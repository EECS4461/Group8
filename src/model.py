from mesa import Model
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from agents import OriginPost, AdBotAgent, ShillBotAgent, UserAgent


class SocialMediaModel(Model):
    """模拟代理模型，包括AdBots、ShillBots、UserAgent以及对OriginPost的操作。"""

    def __init__(self, num_op=5, num_ads=10, num_shills=15, num_users=20, detection=0.5, width=100, height=100):
        super().__init__()
        self.space = ContinuousSpace(width, height, True)
        self.num_op = num_op
        self.num_ads = num_ads
        self.num_shills = num_shills
        self.num_users = num_users
        self.detection = detection

        # 添加原始帖子
        for i in range(num_op):
            # 为每个维度单独生成随机值
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            post = OriginPost(i, self, pos=(x, y))
            self.space.place_agent(post, post.pos)

        # 创建广告机器人
        start_id = num_op
        for i in range(num_ads):
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            adbot = AdBotAgent(start_id + i, self, pos=(x, y))
            self.space.place_agent(adbot, adbot.pos)

        # 创建水军机器人
        start_id += num_ads
        for i in range(num_shills):
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            shill = ShillBotAgent(start_id + i, self, pos=(x, y))
            self.space.place_agent(shill, shill.pos)

        # 创建用户代理
        start_id += num_shills
        for i in range(num_users):
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            user = UserAgent(start_id + i, self, pos=(x, y))
            self.space.place_agent(user, user.pos)

        # 创建数据收集器
        self.datacollector = DataCollector(
            model_reporters={
                "Average Post Heat": self.calculate_average_heat,
                "Active Bots": self.count_active_bots
            }
        )

        # 初始收集一次数据
        self.datacollector.collect(self)

    def calculate_average_heat(self):
        """计算所有原始帖子的平均热度"""
        posts = [agent for agent in self.agents if isinstance(agent, OriginPost)]
        if not posts:
            return 0
        return sum(post.heat for post in posts) / len(posts)

    def count_active_bots(self):
        """计算活跃的机器人数量（广告机器人和水军机器人）"""
        ad_bots = [agent for agent in self.agents if isinstance(agent, AdBotAgent)]
        shill_bots = [agent for agent in self.agents if isinstance(agent, ShillBotAgent)]
        return len(ad_bots) + len(shill_bots)

    def step(self):
        """执行模型的一个步骤"""
        # 原本的步骤执行代码
        for agent in self.agents:
            if hasattr(agent, "step"):
                agent.step()

        # 收集数据
        self.datacollector.collect(self)
