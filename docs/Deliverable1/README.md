# Social Bot Simulation on Xiaohongshu  
ABM-based simulation of coordinated bot activities in e-commerce social platforms. 
Deliverable Documents are in `\docs`, while adapted measa modeling in `mesa-model`.
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
> ## Bot vs Guardian: Simulating Content Modression on Xiaohongshu
> Agent-based modeling of coordinated bot activities and AI moderation dynamics on Xiaohongshu's e-commerce platform.


## 🔍 About the Project
This repository contains the code, documentation, and simulation models for our **EECS 4461: Hypermedia and Multimedia Technology** team project.

Our focus is on simulating the **arms race between social media bots and content moderation systems** on **Xiaohongshu (RedNote)**—a popular Chinese social platform blending social networking with e-commerce.

### ⚡ **Phenomenon of Interest**

Automated bots engage in Xiaohongshu’s comment sections, promoting ads, counterfeit products, and even services like fortune-telling. These bots evolve rapidly, constantly adapting to moderation strategies, which leads to an **ongoing cat-and-mouse game** with platform security systems.

### 🔑 **Key Dynamics We Explore**

1. **Keyword-Based Information Extraction:**  Bots detect sensitive keywords to target specific posts.

2. **Automated Advertising & Fake Engagement:**  Bots create deceptive promotional content, sometimes posing as satisfied customers to boost credibility.

3. **Coordinated Interaction for Credibility:**  Bots engage in scripted conversations to create an illusion of organic, genuine discussions.

4. **The Arms Race:**  As moderation systems improve, bots adopt new evasion techniques:
   - **Adversarial Content Generation:** Context-aware word substitutions (e.g., *"sh!pping"* → *"shipping"*)  
   - **Dynamic Detection Evasion:** Using reinforcement learning to predict moderation updates  
   - **Countermeasure Adaptation:** Moderation AIs employing graph-based detection and behavioral fingerprinting  
   - **User-AI Symbiosis:** Human users inadvertently mimic bot-like patterns in their own behavior

## Features

- 🕵️ **Adversarial Bots**: Simulate keyword-targeted promotional campaigns
- 🛡️ **Platform AI**: Dynamic detection with DBSCAN clustering
- 😀 **User Behavior**: Emotion contagion model with trust decay
- 📊 **Visualization**: Real-time metrics dashboard

### Key Features  
- Multi-agent system modeling ad bots, shill bots, users, and platform AI  
- Dynamic detection-evasion mechanisms using reinforcement learning  
- Emotion contagion model for user trust decay  

## 🚀 How to Contribute

We welcome contributions from the community! Here’s how you can get involved:

1. **Fork** this repository  [**GitHub Repo URL →** *https://github.com/EECS4461/Group8*](https://github.com/EECS4461/Group8)
2. **Clone** it to your local machine  
3. **Create a new branch** for your feature or fix  
4. **Submit a pull request** with a clear description of your changes

💡 **Issues?** Feel free to open one if you spot a bug or have an idea for improvement.

## Installation

```bash
git clone https://github.com/EECS4461/Group8.git
cd Group8
cd mesa-model
pip install -r requirements.txt  # Create this file if needed
python run_simulation.py --config config.yaml
```

---

## 🎯 Goals for the Project

- [ ] Simulate bot behaviors and moderation strategies on Xiaohongshu  
- [ ] Analyze how bots evolve to bypass content moderation  
- [ ] Model the feedback loop between bot evolution and detection algorithm upgrades  
- [ ] Provide insights into the effectiveness of current moderation techniques  

---

## ⚡ Fun Fact

Did you know?  
Bots on social media can sometimes **mimic human behavior better than real users**—but they still can't decide what to eat for breakfast. 🥐☕  

---

## 📢 Stay Connected

For updates, follow this repo and check out our commits regularly. We’re excited to share our progress and findings!

---