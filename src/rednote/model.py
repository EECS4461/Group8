import math

from mesa import Model
from mesa.datacollection import DataCollector
from discrete_space import OrthogonalVonNeumannGrid
from agents import AdBot
from mesa.experimental.devs import ABMSimulator

# model.py 修改建议：
class SocialMediaModel(Model):
    # 新增参数
    def __init__(self, width, height, num_bots, report_threshold=5, detection_interval=100):
        super().__init__()
        # 新增数据收集指标
        self.detection_interval = detection_interval
        self.report_threshold = report_threshold
        self.height = height
        self.width = width
        self.num_bots = num_bots
        self.datacollector = DataCollector(
            model_reporters={
                "Active_Bots": lambda m: len(m.agents_by_type[AdBot]),
                "Purchases": lambda m: m.purchase_count,
                "Detection_Rate": lambda m: m.detection_count / max(1, m.total_reports),
                "Ad_Influence": lambda m: sum(a.influence_radius for a in m.ads)
            }
        )

    def step(self):
        super().step()
        # 平台检测机制
        if self.schedule.steps % self.detection_interval == 0:
            self.detect_suspicious_actors()
        # 动态调整广告影响范围
        for ad in self.ads:
            ad.influence_radius = 1 + ad.likes // 10
            if ad.reports > self.report_threshold:
                ad.is_blocked = True
                ad.influence_radius = max(1, ad.influence_radius//2)

    def detect_suspicious_actors(self):
        for bot in self.ad_bots:
            if bot.reports > 3 * self.report_threshold:
                bot.remove()
                self.detection_count += 1
        for ad in self.ads:
            if ad.reports > 5 * self.report_threshold:
                ad.remove()
