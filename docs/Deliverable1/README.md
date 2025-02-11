# Social Bot Simulation on Xiaohongshu  
ABM-based simulation of coordinated bot activities in e-commerce social platforms.

## Bot vs Guardian: Simulating Content Modression on Xiaohongshu

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Agent-based modeling of coordinated bot activities and AI moderation dynamics on Xiaohongshu's e-commerce platform.

Deliverable Documents are in `\docs`, while adapted measa modeling in `mesa-model`.

## Features

- 🕵️ **Adversarial Bots**: Simulate keyword-targeted promotional campaigns
- 🛡️ **Platform AI**: Dynamic detection with DBSCAN clustering
- 😀 **User Behavior**: Emotion contagion model with trust decay
- 📊 **Visualization**: Real-time metrics dashboard

### Key Features  
- Multi-agent system modeling ad bots, shill bots, users, and platform AI  
- Dynamic detection-evasion mechanisms using reinforcement learning  
- Emotion contagion model for user trust decay  



## Installation

```bash
git clone https://github.com/EECS4461/Group8.git
cd Group8
cd mesa-model
pip install -r requirements.txt  # Create this file if needed
python run_simulation.py --config config.yaml
```