from mesa import Model
from mesa.space import ContinuousSpace
from agents import OriginPost, AdBotAgent, ShillBotAgent, UserAgent


class SocialMediaModel(Model):
    """模拟代理模型，包括AdBots、ShillBots、UserAgent以及对OriginPost的操作。"""

    def __init__(self, num_posts=5, num_ads=10, num_shills=15, num_users=20, width=100, height=100):
        super().__init__()
        self.space = ContinuousSpace(width, height, True)

        # 添加原始帖子
        for i in range(num_posts):
            # 为每个维度单独生成随机值
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            post = OriginPost(i, self, pos=(x, y))
            self.space.place_agent(post, post.pos)

        # 创建广告机器人
        start_id = num_posts
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

    def step(self):
        self.agents.shuffle_do("step")
