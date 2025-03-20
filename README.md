# Social Bot Simulation on Xiaohongshu

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> ## Bot vs Guardian: Simulating Content Modression on redNote
>
> Agent-based modeling of coordinated bot activities and AI moderation dynamics on Xiaohongshu's e-commerce platform.

## 🔍 About the Project

This repository contains the code, documentation, and simulation models for our **EECS 4461: Hypermedia and Multimedia Technology** team project.

Our focus is on simulating the **arms race between social media bots and content moderation systems** on **Xiaohongshu (RedNote)**—a popular Chinese social platform blending social networking with e-commerce.

# Interim Prototype (Partial) - README

## §A. Overview of the Current Implementation State

This project provides a staged, partially functional prototype for the selected phenomenon, developed using Python and the Mesa library. The current development phase is at a stage where different functional modules are demonstrated separately and have not yet been fully integrated into a unified single application. The specific details are as follows:

### Implemented Main Features:

- **Data Collection and Visualization**:
  - `src/demo1.py` has implemented basic data collection and the data visualization features provided by Mesa, such as data charts and log collection.

- **Different Agent Behaviors and Visual Representations**:
  - `src/demo2.py` and `src/demo3.py` have respectively implemented different forms of agent model behavior definitions and visual representations, including but not limited to basic functionalities of different types of agents, such as interactions between behaviors and visual presentations (colors, shapes, etc.).

### Modules Not Yet Fully Integrated:

Currently, there are several folders and modules under the `src/` directory (e.g., `agents`, `app`, `model`) that are still under development. These modules will be integrated based on the Mesa official example `boid_flocker` and the initial draft of our previously designed `rednote_bot` as reference frameworks, incorporating the rules and mechanisms from the demos. They are currently in a partially completed state but have not yet been fully integrated.

Since the integration work is not yet complete, it is recommended that users temporarily run each demo separately using the methods below to observe the effects of the different modules.

## §B. How to Run the Simulation

### 1. Install Dependencies
Please ensure you have Python version 3.10 or higher installed, and execute the following commands to set up the environment:
```bash
git clone https://github.com/EECS4461/Group8.git
cd Group8
pip install -r requirements.txt
```

### 2. Run Each Demo Module Separately (Recommended to run separately)

- Run the data collection and chart visualization demo (`demo_01.py`):
```bash
solara run ./src/demo_01.py
```

- Run the module showcasing interactions of agents with different colors and shapes (`demo_02.py`):
```bash
solara run ./src/demo_02.py
```

- To run the more complex agent behavior demonstration in `demo_03.py`:
```bash
solara run ./src/demo_03.py
```

## §C. Limitations and Planned Improvements

### Current Limitations:

- The modules have not yet been unified into a single runtime environment and need to be launched and evaluated separately, making it temporarily impossible to reflect the fully designed interactive system.
- Some advanced features have not been fully implemented (e.g., advanced interaction logic, refinement of multi-type agent interaction mechanisms, complete integration of audit detection mechanisms, and recommendation algorithms).

### Planned Next Steps for Improvement:

- Integrate the currently separate demo modules (`demo1.py`, `demo2.py`, `demo3.py`, etc.) into a unified application entry point.
- Enhance the model's interaction mechanisms, further refining the basic behaviors and rules already present in the demos.
- Expand the dimensions and depth of data collection to enable more in-depth statistical analysis, advanced data visualization, and interactive charts.
- Introduce audit agents (e.g., ModAI type) and further develop the recommendation system and audit mechanisms to achieve a more realistic and unified simulation effect.

For more detailed explanations and full progress updates, please refer to the project documentation (`docs/Deliverable3/OPT_GUIDE_EN.md`).