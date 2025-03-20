from mesa import Agent
import numpy as np


class OriginPost(Agent):
    """代表一个静态的原始帖子，记录交互热度和点赞量。"""

    def __init__(self, unique_id, model, pos, base_heat=10):
        super().__init__(model)  # 只传递 model 参数
        self.unique_id = unique_id  # 手动设置 unique_id
        self.pos = pos
        self.heat = base_heat

    def step(self):
        # 根据机器人、用户的互动动态调整热度
        self.heat = max(0, self.heat)  # 防止负值，保持非负数


class AdBotAgent(Agent):
    """广告机器人，吸附到热点帖子并增加热度，同时吸引ShillBots。"""

    def __init__(self, unique_id, model, pos, speed=1):
        super().__init__(model)  # 只传递 model 参数
        self.unique_id = unique_id  # 手动设置 unique_id
        self.pos = np.array(pos)
        self.speed = speed
        self.target_post = None  # 瞄准目标原始帖子

    def find_target(self):
        # 搜索范围内的最近OriginPost
        posts = [agent for agent in self.model.agents if isinstance(agent, OriginPost)]
        if posts:
            self.target_post = min(posts, key=lambda p: np.linalg.norm(self.pos - np.array(p.pos)))

    def move(self):
        # 移动逻辑，向目标前进
        if self.target_post:
            direction = np.array(self.target_post.pos) - self.pos
            distance = np.linalg.norm(direction)
            if distance > 0:
                direction /= distance
            self.pos += direction * self.speed
            self.pos = np.clip(self.pos, 0, self.model.space.width)

    def step(self):
        if not self.target_post or np.linalg.norm(self.pos - np.array(self.target_post.pos)) < 1:
            self.find_target()
        self.move()
        # 增加目标帖子的热度
        if self.target_post:
            self.target_post.heat += 5


class ShillBotAgent(Agent):
    """水军机器人，跟随广告机器人行动，同时模拟点踩行为。"""

    def __init__(self, unique_id, model, pos, speed=1):
        super().__init__(model)  # 只传递 model 参数
        self.unique_id = unique_id  # 手动设置 unique_id
        self.pos = np.array(pos)
        self.speed = speed
        self.target = None

    def find_target(self):
        # 寻找附近的AdBot或热门帖子
        adbots = [agent for agent in self.model.agents if isinstance(agent, AdBotAgent)]
        if adbots:
            self.target = min(adbots, key=lambda a: np.linalg.norm(self.pos - np.array(a.pos)))

    def move(self):
        if self.target:
            direction = np.array(self.target.pos) - self.pos
            distance = np.linalg.norm(direction)
            if distance > 0:
                direction /= distance
            self.pos += direction * self.speed
            self.pos = np.clip(self.pos, 0, self.model.space.width)

    def step(self):
        self.find_target()
        self.move()


class UserAgent(Agent):
    """用户代理，可能被广告机器人和ShillBots欺骗，增加交互热度。"""

    def __init__(self, unique_id, model, pos, engagement=0.5):
        super().__init__(model)  # 只传递 model 参数
        self.unique_id = unique_id  # 手动设置 unique_id
        self.pos = np.array(pos)
        self.engagement = engagement  # 初始交互程度
        self.trust = 0.5  # 用户的初始信任

    def move(self):
        # 随机游走
        # 修正随机游走的实现方式
        x_move = self.model.random.uniform(-1, 1)
        y_move = self.model.random.uniform(-1, 1)
        self.pos += np.array([x_move, y_move])
        self.pos = np.clip(self.pos, 0, self.model.space.width)

    def update_engagement(self):
        # 如果附近有吸附的ShillBot，欺骗用户增加engagement
        nearby_shills = [
            agent for agent in self.model.agents
            if isinstance(agent, ShillBotAgent) and np.linalg.norm(self.pos - agent.pos) < 5
        ]
        if nearby_shills:
            self.engagement += 0.1  # 增加交互度

    def step(self):
        self.move()
        self.update_engagement()
