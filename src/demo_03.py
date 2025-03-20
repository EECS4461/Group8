import numpy as np
from mesa import Model, Agent
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from mesa.visualization import SolaraViz, make_space_component, make_plot_component, Slider
from sklearn.cluster import DBSCAN
import random

# 二维空间维度配置
SPACE_DIMENSIONS = {
    'x_max': 200,  # 水平空间
    'y_max': 200,  # 垂直空间
}

class OriginalPostAgent(Agent):
    """原始帖子，固定在随机位置"""
    def __init__(self, model):
        super().__init__(model)
        self.likes = np.random.randint(1, 10)  # 初始点赞数
        self.heat = 1.0  # 初始热度

    def step(self):
        # 热度随时间自然衰减
        self.heat = max(1.0, self.heat * 0.95)
        
        # 统计周围的广告机器人和水军数量来增加热度
        neighbors = self.model.space.get_neighbors(self.pos, 5)
        bots = [a for a in neighbors if isinstance(a, (AdBotAgent, ShillBotAgent))]
        
        # 热度增长与bot数量和平台热度修饰符相关
        self.heat += len(bots) * 0.1 * self.model.heat_modifier
        self.likes += len([a for a in neighbors if isinstance(a, ShillBotAgent)]) // 3  # 水军点赞


class AdBotAgent(Agent):
    """广告机器人，寻找热门帖子并发布广告"""
    def __init__(self, model):
        super().__init__(model)
        self.speed = 2.0
        self.target_post = None
        self.attached = False
        self.cluster_size = 1
    
    def find_target(self):
        """寻找周围点赞最高的帖子作为目标"""
        neighbors = self.model.space.get_neighbors(self.pos, 10)
        posts = [agent for agent in neighbors if isinstance(agent, OriginalPostAgent)]
        
        if posts:
            # 根据点赞数和热度寻找目标
            weights = [post.likes * post.heat * np.random.rand() for post in posts]
            self.target_post = posts[np.argmax(weights)]
            return True
        return False
    
    def move(self):
        if self.attached:
            # 已附着到帖子，小范围随机移动模拟评论区位置
            offset = np.random.uniform(-1, 1, 2)
            new_pos = np.array(self.pos) + offset
            # Add boundary check
            new_pos = np.clip(new_pos, [0, 0], [SPACE_DIMENSIONS['x_max'], SPACE_DIMENSIONS['y_max']])
            self.model.space.move_agent(self, tuple(new_pos))
        elif self.target_post:
            # 向目标帖子移动
            target_vec = np.array(self.target_post.pos) - np.array(self.pos)
            distance = np.linalg.norm(target_vec)
            
            if distance < 2:  # 足够接近时附着
                self.attached = True
            else:
                direction = target_vec / distance
                new_pos = np.array(self.pos) + direction * self.speed
                # Add boundary check
                new_pos = np.clip(new_pos, [0, 0], [SPACE_DIMENSIONS['x_max'], SPACE_DIMENSIONS['y_max']])
                self.model.space.move_agent(self, tuple(new_pos))
        else:
            # 随机游走
            new_pos = np.array(self.pos) + np.random.uniform(-2, 2, 2)
            new_pos = np.clip(new_pos, [0, 0], [SPACE_DIMENSIONS['x_max'], SPACE_DIMENSIONS['y_max']])
            self.model.space.move_agent(self, tuple(new_pos))
    
    def step(self):
        # 更新集群大小（用于可视化）
        neighbors = self.model.space.get_neighbors(self.pos, 5)
        self.cluster_size = 1 + len([a for a in neighbors if isinstance(a, AdBotAgent)])
        
        # 如果未附着且无目标，寻找目标
        if not self.attached and not self.target_post:
            if not self.find_target():
                self.move()
        else:
            self.move()
        
        # 检测是否被平台发现（基于detection强度和集群大小）
        detection_probability = self.model.detection_intensity * (0.05 + 0.02 * self.cluster_size)
        if np.random.random() < detection_probability:
            self.model.remove_agent(self)


class ShillBotAgent(Agent):
    """水军机器人，跟随广告机器人并增加互动"""
    def __init__(self, model):
        super().__init__(model)
        self.speed = 1.5
        self.target = None  # 可以是AdBot或OriginalPost
    
    def find_target(self):
        neighbors = self.model.space.get_neighbors(self.pos, 15)
        
        # 优先跟随广告机器人
        ad_bots = [a for a in neighbors if isinstance(a, AdBotAgent) and a.attached]
        if ad_bots:
            self.target = self.model.random.choice(ad_bots)
            return True
        
        # 其次寻找热门帖子
        posts = [a for a in neighbors if isinstance(a, OriginalPostAgent) and a.heat > 2]
        if posts:
            self.target = self.model.random.choice(posts)
            return True
            
        return False
    
    def move(self):
        if self.target:
            # 向目标移动（带有一点随机性）
            target_vec = np.array(self.target.pos) - np.array(self.pos)
            distance = np.linalg.norm(target_vec)
            
            # 如果距离适中，添加一些随机游走以形成群体行为
            if distance < 8:
                direction = target_vec / max(distance, 0.1)
                random_offset = np.random.uniform(-1, 1, 2)
                new_pos = np.array(self.pos) + direction * self.speed * 0.5 + random_offset
            else:
                direction = target_vec / max(distance, 0.1)
                new_pos = np.array(self.pos) + direction * self.speed
                
            # 确保在空间范围内
            new_pos = np.clip(new_pos, [0, 0], [SPACE_DIMENSIONS['x_max'], SPACE_DIMENSIONS['y_max']])
            self.model.space.move_agent(self, tuple(new_pos))
        else:
            # 随机游走
            new_pos = np.array(self.pos) + np.random.uniform(-1.5, 1.5, 2)
            new_pos = np.clip(new_pos, [0, 0], [SPACE_DIMENSIONS['x_max'], SPACE_DIMENSIONS['y_max']])
            self.model.space.move_agent(self, tuple(new_pos))
    
    def step(self):
        # 一定概率重新选择目标
        if not self.target or np.random.random() < 0.05:
            self.find_target()
        
        self.move()
        
        # 检测是否被平台发现
        # 水军更难被发现，除非聚集得很明显
        neighbors = self.model.space.get_neighbors(self.pos, 3)
        shill_cluster = len([a for a in neighbors if isinstance(a, ShillBotAgent)])
        
        detection_probability = self.model.detection_intensity * (0.01 + 0.03 * shill_cluster / 5)
        if np.random.random() < detection_probability:
            self.model.remove_agent(self)


class UserAgent(Agent):
    """真实用户，可能被广告影响"""
    def __init__(self, model):
        super().__init__(model)
        self.engagement = 0  # 参与度
        self.trust = 0.5     # 对平台的信任度
        self.deceived = 0    # 被欺骗次数
    
    def move(self):
        # 随机游走
        new_pos = np.array(self.pos) + np.random.uniform(-2, 2, 2)
        new_pos = np.clip(new_pos, [0, 0], [SPACE_DIMENSIONS['x_max'], SPACE_DIMENSIONS['y_max']])
        self.model.space.move_agent(self, tuple(new_pos))
    
    def update_engagement(self):
        # 查看周围的帖子和广告
        neighbors = self.model.space.get_neighbors(self.pos, 8)
        posts = [a for a in neighbors if isinstance(a, OriginalPostAgent)]
        bots = [a for a in neighbors if isinstance(a, (AdBotAgent, ShillBotAgent))]
        
        if not posts:
            return
        
        # 如果周围有帖子，增加参与度
        self.engagement += 1
        
        # 如果周围有很多广告和水军，可能被欺骗
        bot_ratio = len(bots) / max(1, len(neighbors))
        
        # 欺骗概率与bot比例、信任度有关
        deception_probability = bot_ratio * self.trust
        if np.random.random() < deception_probability:
            self.deceived += 1
            self.engagement += 2  # 被欺骗会有更多互动
            self.trust *= 0.95    # 信任度略微下降
        else:
            self.trust = min(1.0, self.trust * 1.01)  # 未被欺骗，信任度略增
    
    def step(self):
        self.move()
        self.update_engagement()


class RandomActivationByType:
    """A scheduler that activates each type of agent once per step, in random order."""
    def __init__(self, model):
        self.model = model
        self.agents_by_type = {}
        self.steps = 0
        self.time = 0

    def add(self, agent):
        agent_class = type(agent)
        if agent_class not in self.agents_by_type:
            self.agents_by_type[agent_class] = {}
        self.agents_by_type[agent_class][agent.unique_id] = agent

    def remove(self, agent):
        agent_class = type(agent)
        del self.agents_by_type[agent_class][agent.unique_id]

    def step(self):
        for agent_class in self.agents_by_type:
            agents = list(self.agents_by_type[agent_class].values())
            self.model.random.shuffle(agents)
            for agent in agents:
                agent.step()
        self.steps += 1
        self.time += 1


class SocialMediaModel(Model):
    """社交媒体平台模型"""
    def __init__(
        self,
        num_op=20,        # 原始帖子数
        num_ads=30,       # 广告机器人数
        num_shills=50,    # 水军机器人数
        num_users=100,    # 真实用户数
        detection=0.5,    # 平台检测强度
    ):
        super().__init__()
        self.space = ContinuousSpace(
            SPACE_DIMENSIONS['x_max'],
            SPACE_DIMENSIONS['y_max'],
            False  # 不使用环形空间
        )
        
        self.num_op = num_op
        self.num_ads = num_ads
        self.num_shills = num_shills
        self.num_users = num_users
        self.detection_intensity = detection
        self.heat_modifier = 1.0
        self.steps = 0  # 步数计数器
        
        # 创建调度器
        self.schedule = RandomActivationByType(self)
        self.running = True
        
        # 创建各类代理
        self.create_original_posts()
        self.create_ad_bots()
        self.create_shill_bots()
        self.create_users()
        
        # 数据收集器
        self.datacollector = DataCollector(
            model_reporters={
                "Active Ad Bots": lambda m: len([a for a in m.schedule.agents_by_type[AdBotAgent]]),
                "Active Shill Bots": lambda m: len([a for a in m.schedule.agents_by_type[ShillBotAgent]]),
                "User Engagement": lambda m: sum(a.engagement for a in m.schedule.agents_by_type[UserAgent]),
                "User Deception": lambda m: sum(a.deceived for a in m.schedule.agents_by_type[UserAgent]),
                "Average Post Heat": lambda m: np.mean([a.heat for a in m.schedule.agents_by_type[OriginalPostAgent]]) if any(isinstance(a, OriginalPostAgent) for a in m.schedule.agents) else 0
            }
        )
    
    def create_original_posts(self):
        """创建原始帖子"""
        for i in range(self.num_op):
            x = np.random.uniform(10, SPACE_DIMENSIONS['x_max']-10)
            y = np.random.uniform(10, SPACE_DIMENSIONS['y_max']-10)
            post = OriginalPostAgent(self)
            self.space.place_agent(post, (x, y))
            self.schedule.add(post)
    
    def create_ad_bots(self):
        """创建广告机器人"""
        for i in range(self.num_ads):
            x = np.random.uniform(0, SPACE_DIMENSIONS['x_max'])
            y = np.random.uniform(0, SPACE_DIMENSIONS['y_max'])
            bot = AdBotAgent(self)
            self.space.place_agent(bot, (x, y))
            self.schedule.add(bot)
    
    def create_shill_bots(self):
        """创建水军机器人"""
        for i in range(self.num_shills):
            x = np.random.uniform(0, SPACE_DIMENSIONS['x_max'])
            y = np.random.uniform(0, SPACE_DIMENSIONS['y_max'])
            bot = ShillBotAgent(self)
            self.space.place_agent(bot, (x, y))
            self.schedule.add(bot)
    
    def create_users(self):
        """创建真实用户"""
        for i in range(self.num_users):
            x = np.random.uniform(0, SPACE_DIMENSIONS['x_max'])
            y = np.random.uniform(0, SPACE_DIMENSIONS['y_max'])
            user = UserAgent(self)
            self.space.place_agent(user, (x, y))
            self.schedule.add(user)
    
    def remove_agent(self, agent):
        """从模型中移除代理"""
        self.space.remove_agent(agent)
        self.schedule.remove(agent)
    
    def analyze_clusters(self):
        """分析并处理可疑集群"""
        # 从所有类型的代理中获取机器人
        bots = []
        for agent_class in self.schedule.agents_by_type:
            if issubclass(agent_class, (AdBotAgent, ShillBotAgent)):
                bots.extend(self.schedule.agents_by_type[agent_class].values())
        
        if len(bots) <= 10:
            return  # 太少机器人，不进行聚类
            
        bot_positions = np.array([(a.pos[0], a.pos[1]) for a in bots])
        
        # 使用DBSCAN进行聚类分析
        clustering = DBSCAN(eps=8, min_samples=5).fit(bot_positions)
        clusters = {}
        
        # 统计每个集群中的机器人
        for i, label in enumerate(clustering.labels_):
            if label != -1:  # 忽略噪声点
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(i)
        
        # 处理可疑集群
        for cluster_id, indices in clusters.items():
            if len(indices) > 10:  # 大集群更可疑
                cluster_size = len(indices)
                # 大集群有更高的检测概率
                detection_prob = self.detection_intensity * (0.2 + 0.01 * cluster_size)
                
                if np.random.random() < detection_prob:
                    # 找出集群中的所有机器人 
                    cluster_bots = [bots[i] for i in indices]
                    
                    # 随机移除一部分
                    for bot in self.random.sample(cluster_bots, int(cluster_size * 0.3)):
                        self.remove_agent(bot)
    
    def update_heat_modifier(self):
        """更新热度修饰符"""
        # 简单的热度波动模式
        self.heat_modifier = 1.0 + 0.3 * np.sin(self.steps / 10)
    
    def step(self):
        """执行模型单步"""
        self.steps += 1
        self.update_heat_modifier()
        self.schedule.step()
        self.analyze_clusters()
        self.datacollector.collect(self)


# 可视化设置
def agent_portrayal(agent):
    """定义各类代理的可视化属性"""
    if isinstance(agent, OriginalPostAgent):
        size = 15 + agent.heat * 0.5  # 热度越高，星星越大
        return {
            "marker": "*", 
            "color": "#FF0000", 
            "size": size, 
            "alpha": min(1.0, max(0.5, agent.heat/10))
        }
    
    elif isinstance(agent, AdBotAgent):
        return {
            "marker": ".",
            "color": "#1E90FF",
            "size": 10 + agent.cluster_size,
            "alpha": 0.7
        }
    
    elif isinstance(agent, ShillBotAgent):
        neighbors = len(agent.model.space.get_neighbors(agent.pos, 5))
        return {
            "marker": "^",
            "color": "#00FF00" if neighbors < 5 else "#8A2BE2",
            "size": 8 + neighbors * 0.5,
            "alpha": 0.6
        }
    
    elif isinstance(agent, UserAgent):
        return {
            "marker": "o",
            "color": "#FFD700",
            "size": 8,
            "alpha": 0.8
        }
    
    return {"marker": "o", "color": "gray", "size": 5, "alpha": 0.5}


# 定义图表组件
plot_component = make_plot_component(
    ["Active Ad Bots", "Active Shill Bots", "User Engagement", "User Deception", "Average Post Heat"]
)

# 定义空间组件
space_component = make_space_component(agent_portrayal)

# 定义模型参数
model_params = {
    "num_op": Slider("Original Posts", 20, 10, 100, 1),
    "num_ads": Slider("Ad Bots", 30, 10, 100, 1),
    "num_shills": Slider("Shill Bots", 50, 10, 200, 5),
    "num_users": Slider("Users", 100, 50, 300, 10),
    "detection": Slider("Detection", 0.5, 0.1, 1.0, 0.1)
}

# 创建模型实例
model = SocialMediaModel()

# 创建单一的可视化实例
viz = SolaraViz(
    model,
    components=[space_component, plot_component],
    model_params=model_params,
    name="redNote ADBot Simulation"
)

# 最后返回可视化对象
viz  # noqa
# Added Page variable for SolaraViz page export
Page = viz