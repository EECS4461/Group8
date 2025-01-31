# Bot vs Guardian: Simulating Content Moderation Arms Race on Social Platforms

This **README** provides an overview of our Mesa-based simulation project, focusing on the escalating cycle of **content moderation** and **evasion tactics** in online social platforms. We adapt existing agent-based models (ABMs) from the Mesa framework—particularly those inspired by  **Epstein’s Civil Violence** ,  **Virus on Network** , and  **Schelling’s Segregation** —to model how automated moderation (guardian) and adversarial bots evolve and interact in a dynamic arms race. Our primary application scenario is a platform like  *Xiaohongshu (RedNote)* , but the design is sufficiently general to fit many social media ecosystems.

---

## 1. Research Motivation

Modern social media platforms face continual challenges in  **moderating illicit or rule-breaking content** . Whenever the platform updates detection rules (e.g., for spam, fake reviews, malicious links), adversarial **bot** strategies evolve to bypass these new constraints. Likewise, each wave of bot evasion triggers more sophisticated moderation tactics. This phenomenon mirrors an **“arms race”** or **“cat-and-mouse”** cycle, where both sides perpetually adapt and escalate.

### Key Dynamics

1. **Adaptive Bot Generation**
   * Bots employ techniques like adversarial keyword obfuscation (e.g., “sh!pping” instead of “shipping”) and AI-generated text to evade detection.
2. **Content Moderation Upgrades**
   * Moderators refine detection algorithms using graph-based analysis, advanced ML classifiers, or heuristic rules triggered by suspicious behavior.
3. **Feedback Loops**
   * Each moderation improvement prompts new bot strategies, creating cyclical spikes in evasion.
4. **User-AI Symbiosis**
   * Real users may unintentionally adopt “bot-like” posting styles or circumvent detection through coded language, further complicating detection.

---

## 2. Base Models and Adaptations

We build on **Mesa’s** **existing model library** and well-known ABM patterns to represent these social platform interactions. Below is a summary of three primary models we adapt, along with suggested modifications.

### 2.1 Epstein’s Civil Violence Model

**Original Mechanics**

* Agents (citizens) interact with authority figures (police) in a grid or network.
* Each citizen has a certain grievance/risk perception that determines whether they rebel or comply.
* Authority legitimacy influences citizens’ decisions over time.

**Proposed Adaptation**

* **Citizen Agents** → *BotAgents* that post (or refrain from posting) illicit content.
* **Police Agents** → *ModeratorAgents* that apply rules or sanctions.
* **Legitimacy** →  *Platform Trust Score* , indicating how users perceive the fairness/effectiveness of moderation.
* **Rebellion Probability** →  *Violation Probability* , i.e., how likely a bot is to post illegal/spam content.

**Additional Features**

* **Dynamic Rule Updates** : The platform (akin to “government” or “law”) periodically adjusts detection thresholds.
* **RNN-Based Violation Prediction** : Use a minimal RNN or NN-based classifier for bots to sense patterns of prior sanctions.
* **Evolutionary Tuning** : Bot behaviors evolve each cycle to maximize evasion.

---

### 2.2 Virus on Network Model

**Original Mechanics**

* A graph-based model where each node can be in susceptible/infected/recovered states.
* Infection spreads through edges until the system intervenes or nodes recover.

**Proposed Adaptation**

* **Virus** → *Illicit Content* (spam, disinformation).
* **Infection** →  *Propagation of Bot Posts* .
* **Recovery/Immunity** → *User- or AI-driven removal* of bad content.
* **Network** → *Social Graph* of user connections.

**Additional Features**

* **Multi-level Intervention** : Mitigation triggers at the user, community, and platform levels.
* **Content Mutation** : Illicit content can “mutate” (e.g., altering keywords, sentence structures) to bypass filters.
* **Dynamic Quarantines** : The model can isolate certain communities or users if infection (spam) levels get too high.

---

### 2.3 Schelling’s Segregation Model

**Original Mechanics**

* Agents (residents) move on a grid based on satisfaction thresholds tied to neighbors’ similarity.
* Clusters of like agents form over time, illustrating self-organization.

**Proposed Adaptation**

* **Residents** →  *Mixed Human-Bot Agents* .
* **Satisfaction** → *Content Match Score* (the alignment between agent interest and community norms).
* **Movement/Relocation** →  *Migration Between Communities* , as bots or users shift to other sub-forums/platforms for better infiltration or acceptance.

**Additional Features**

* **Inter-Community Influence** : Cross-platform movement or infiltration.
* **Polarization Metrics** : Track echo-chamber formation and group radicalization.
* **Hidden Preferences** : Agents might conceal real preferences to avoid detection or ostracism.

---

## 3. Secondary Reference Models

| Model                            | Mechanism to Borrow          | Use Case in Our Context                 |
| -------------------------------- | ---------------------------- | --------------------------------------- |
| **Boid Flocking**          | Coordinated group motion     | Bot swarms coordinating mass-posting    |
| **Wolf-Sheep Predation**   | Resource competition         | Mimicking “attention economy” clashes |
| **Conway’s Game of Life** | Cellular automaton evolution | Content life-cycle prediction           |

---

## 4. Technical Implementation in Mesa

Below is a code snippet showing how we might set up **ModeratorAgent** and **BotAgent** in Mesa, reflecting the **Epstein** style adaptation. The pseudo-code demonstrates:

1. **Moderator** adjusting detection rules and scanning for suspicious activity
2. **Bot** evolving its post strategies over time

```python
import mesa
import random

class ModeratorAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.detection_threshold = 0.5

    def step(self):
        self.adapt_rules()
        # Identify potential violators
        for agent in self.model.schedule.agents:
            if isinstance(agent, BotAgent):
                risk_score = self.evaluate_risk(agent)
                if risk_score > self.detection_threshold:
                    self.enforce_penalty(agent)

    def adapt_rules(self):
        # Periodically adjust detection threshold 
        if self.model.schedule.steps % self.model.rule_update_interval == 0:
            self.detection_threshold *= 1.05  # e.g., slightly tighter every update

    def evaluate_risk(self, bot):
        # Could integrate ML-based or heuristic scoring 
        return bot.behavior_score * random.random()

    def enforce_penalty(self, bot):
        bot.muted = True  # simplified penalty action
        bot.increase_evasion_pressure()

class BotAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.behavior_score = 0.3
        self.muted = False

    def step(self):
        if not self.muted:
            self.adaptive_post()

    def adaptive_post(self):
        # Generate content with some probability of detection 
        content = self.generate_adversarial_content()
        # ... post content
        self.model.record_content_posted(self, content)

    def increase_evasion_pressure(self):
        # Mimic an evolutionary strategy
        self.behavior_score += 0.1  # become more extreme in subsequent steps

    def generate_adversarial_content(self):
        # Simple placeholder for AI-based text generation
        return f"Buy now! Using code s.h!pping..."

```

---

## 5. Integration Strategy

1. **Multi-Layer Architecture**
   * **Micro-Level** : *Epstein Model* for direct agent interactions (bot vs. moderator).
   * **Meso-Level** : *Virus Model* for content spread across a social graph.
   * **Macro-Level** : *Schelling Model* for larger-scale community shift and segregation.
2. **Hybrid Network**
   ```python
   from mesa.space import NetworkGrid, ContinuousSpace

   class HybridSpace:
       def __init__(self):
           self.social_graph = NetworkGrid(...)       # Social relationships
           self.content_space = ContinuousSpace(...)  # Content attribute space
   ```
3. **Adaptive Environment**
   ```python
   class AdaptiveEnvironment:
       def __init__(self):
           self.detection_intensity = 0.7
           self.rule_update_interval = 24

       def adjust_parameters(self, performance_metrics):
           # Example dynamic update
           if performance_metrics["recall_rate"] > 0.9:
               self.detection_intensity *= 0.95
           else:
               self.detection_intensity = min(1.0, self.detection_intensity * 1.1)
   ```

---

## 6. Visualization

A possible  **multi-layer architecture diagram** :

```
+--------------------+
| Macro Layer        |  <- Schelling-based clustering
| - Community shifts |
+--------------------+
         |
         v
+--------------------+
| Meso Layer         |  <- Virus-like content spread
| - Social Graph     |
+--------------------+
         |
         v
+--------------------+
| Micro Layer        |  <- Epstein-based bot vs. moderator
| - Individual Agents|
+--------------------+
```

### Suggested Metrics for the Simulation Dashboard

1. **Oscillation Frequency** : How often bot tactics and moderator rules cycle back and forth.
2. **Strategy Evolution Entropy** : Complexity or diversity of evasive tactics over time.
3. **Detection vs. Evasion Efficiency Ratio** : Relative gains by moderation vs. adversaries each turn.
4. **System “Dissipation” Rate** : Overall cost or resource usage in the arms race.

---

## 7. How to Run

1. **Installation**

   * Clone this repository:
     ```bash
     git clone https://github.com/EECS4461/Group8.git
     cd Group8/mesa-model
     ```
   * Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
2. **Launch the Model**

   ```bash
   mesa runserver
   ```

   * Access the local web interface at [http://127.0.0.1:8521](http://127.0.0.1:8521/)
   * Configure the simulation parameters (detection thresholds, update intervals) in the UI panel
3. **Observe & Tweak**

   * Watch agent behaviors, real-time charts, and logs.
   * Adjust environment parameters to experiment with different arms-race intensities.

---

## 8. References

* **[Epstein Civil Violence Model]**

  * [Joshua M. Epstein (2002). Modeling Civil Violence: An Agent-Based Computational Approach.](https://doi.org/10.1073/pnas.092080199)
* **[Virus on Network Model]**

  * [Past Mesa example references in the official Mesa library.](https://github.com/projectmesa/mesa-examples)
* **[Schelling Segregation Model]**

  * [Thomas C. Schelling (1971). Dynamic Models of Segregation. Journal of Mathematical Sociology.
    ](https://www.tandfonline.com/doi/abs/10.1080/0022250X.1971.9989794)

---

## 9. Future Extensions

* **Cross-Modal Detection** : Incorporate image-based or video content detection.
* **Evolutionary Bot Swarms** : Extend BotAgents with group-level coordination logic akin to *Boids* or  *Wolf-Sheep Predation* .
* **User Involvement** : Model how legitimate users adapt to platform changes or inadvertently aid evasion (e.g., using coded language).

This simulation environment aims to capture the  **spiral of ban-and-breakthrough** —the never-ending cycle of moderation upgrades and adversarial strategies in content moderation on social platforms. By adapting multiple Mesa models, we hope to provide insights into emergent patterns, best-practice moderation strategies, and potential vulnerabilities.

Feel free to create issues and pull requests to refine or extend these models further!
