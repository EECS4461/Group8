from discrete_space import CellAgent, FixedAgent

class OriginalPost(FixedAgent):
    """原始文章（红色五角星）"""
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell
        self.influence_radius = 3  # 初始影响范围

class AdPost(FixedAgent):
    """广告贴（蓝色网格）"""
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell
        self.likes = 0
        self.reports = 0
        self.influence_radius = 1
        self.is_blocked = False

class AdBot(CellAgent):
    """广告机器人（绿色三角）"""
    def __init__(self, model, energy=20,  **kwargs):
        super().__init__(model,  **kwargs)
        self.energy = energy
        self.target_posts = []  # 目标原始文章列表
        self.report_risk = 0

    def step(self):
        self.find_target_posts()
        self.publish_ads()
        self.collaborative_likes()
        self.avoid_detection()
        self.energy -= 1
        if self.energy < 0:
            self.remove()

    def find_target_posts(self):
        # 寻找周围3格内的原始文章
        nearby_cells = self.cell.get_neighbors(3)
        self.target_posts = [cell for cell in nearby_cells if isinstance(cell.agent, OriginalPost)]

    def publish_ads(self):
        if self.random.random() < self.publish_prob:
            # 在目标文章周围随机位置发布广告
            target_cell = self.random.choice(self.target_posts).get_random_adjacent_cell()
            AdPost(self.model, target_cell)

    def collaborative_likes(self):
        # 协作点赞最近的广告贴
        nearby_ads = self.find_nearby_ads()
        if nearby_ads:
            selected_ad = self.random.choice(nearby_ads)
            selected_ad.likes += 1
            self.model.update_ad_influence(selected_ad)

    def avoid_detection(self):
        # 根据举报风险调整行为
        if self.report_risk > 0.7:
            self.publish_prob *= 0.5  # 降低发布频率

class HumanUser(CellAgent):
    """人类用户（黄色圆点）"""
    def __init__(self, model,  **kwargs):
        super().__init__(model,  **kwargs)
        self.has_reported = False

    def step(self):
        self.random_move()
        self.interact_with_ads()
        self.check_ad_reports()

    def interact_with_ads(self):
        current_cell = self.cell
        ads_in_cell = [a for a in current_cell.agents if isinstance(a, AdPost)]
        if ads_in_cell:
            ad = self.random.choice(ads_in_cell)
            action = self.random.choices(['like', 'buy', 'report'],
                                        weights=[0.6, 0.3, 0.1])[0]
            if action == 'like':
                ad.likes += 1
            elif action == 'buy':
                self.model.purchase_count += 1
            elif action == 'report':
                ad.reports += 1
                self.has_reported = True

    def check_ad_reports(self):
        # 用户举报后可能触发连锁举报
        if self.has_reported and self.random.random() < 0.3:
            nearby_ads = self.find_nearby_ads()
            for ad in nearby_ads:
                ad.reports += 1
