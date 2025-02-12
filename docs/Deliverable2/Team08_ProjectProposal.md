The Deliverable DEL 2.B The Proposal

Header

* Title: Bots vs Guardians: Simulating Audits on Xiaohongshu (RedNote)  
* Team members: Xintong (Sylvia) LING, Huanrui (Saikoro) CAO, Jiayi (Jaye) CHEN  
* [GitHub repo URL](https://github.com/EECS4461/Group8):  [https://github.com/EECS4461/Group8](https://github.com/EECS4461/Group8)

Section 1: Phenomena of interest.

Our project focuses on the commenting ecology of automated robots (bots) on the Chinese social media and e-commerce platform Xiaohongshu (RedNote). Automated bots often appear under posts containing specific keywords, especially in areas related to logistics and specific product categories. These bots often coordinate their actions to promote advertisements, counterfeit goods, and services such as fortune-telling.

Xiaohongshu (RedNote) is a rapidly growing platform with over 200 million monthly active users, combining social media features with e-commerce. It is widely used in China for product recommendations, lifestyle sharing, and community discussions, making it an attractive target for automated bots aiming to manipulate content and trends.

Our simulation aims to explore the dynamics of bot-generated content and content moderation mechanisms on Xiaohongshu (RedNote). The core phenomena of interest include:

* Influence of Bots on Content Visibility: How AI-driven social bots manipulate trends, inflate engagement metrics, and shape public opinion.  
* Human-Bot Interaction Dynamics: The interplay between human users and bots, including content creation, sharing, and reactions.  
* Effectiveness of Content Moderation: The role of moderation algorithms in detecting, limiting, or removing manipulative content.

We seek to understand how these phenomena evolve through simple agent-based interactions, leading to emergent behaviours similar to flocking dynamics in the Boid model.

Section 2: Phenomena of interest.

To demonstrate the evolving challenges facing social media bot detection, we revisit the core phenomenon of our interest, the dynamic interplay between bot behavioural patterns and community structure in online networks, and consolidate this discussion with critical analyses of two important scholarly works.

Chen et al. (2024) introduce CACL, a framework for detecting social media bots using community-aware heterogeneous graph contrastive learning. The authors address the challenge of identifying bots in complex social networks by leveraging heterogeneous graph structures and contrastive learning techniques. CACL incorporates community information to enhance detection accuracy, as bots often exhibit distinct behaviours within communities. The proposed method outperforms existing approaches by effectively capturing both local and global patterns in the graph. The paper demonstrates the effectiveness of CACL through extensive experiments on real-world datasets, highlighting its potential for improving bot detection in social media platforms.

The article "Detecting Social Media Bots with Variational AutoEncoder and k-Nearest Neighbor" by Wang et al. (2021) proposes a method for identifying social media bots. The study introduces a detection framework that combines Variational AutoEncoders (VAE) with the k-Nearest Neighbor (k-NN) algorithm. The VAE is utilized to learn a compressed representation of user data, capturing essential features that distinguish genuine users from bots. Then the k-NN algorithm is applied to these representations to classify users based on their proximity to known bot or human profiles. Experimental results demonstrate that this hybrid approach enhances detection accuracy compared to traditional methods, offering a promising solution for mitigating the influence of bots on social media platforms.

References

Chen, S., Feng, S., Liang, S., Zong, C.-C., Li, J., & Li, P. (2024, June 3). *CACL: Community-aware heterogeneous graph contrastive learning for social media bot detection*. arXiv.org. https://arxiv.org/abs/2405.10558

Wang, X., Zheng, Q., Zheng, K., Sui, Y., Cao, S., & Shi, Y. (2021, June 13). *Detecting social media bots with variational AutoEncoder and K-nearest neighbor*. MDPI. https://www.mdpi.com/2076-3417/11/12/5482 

Section 3: Describe the Core Components of the Simulation

Instructions

Our simulation is most closely aligned with the Boid Flocking Model. This model effectively demonstrates how simple, local interaction rules can lead to complex, emergent group behaviours, which parallels the dynamics we aim to simulate on Xiaohongshu (RedNote). In our case, instead of birds, we are simulating the behaviours of human users and AI-driven social bots interacting within the platform's content ecosystem.

§3.1 Entities: 

* Bot: AI agent that automates ads, manipulates credibility, and circumvents detection.           
  Goal: increase the credibility of ad content by interacting and masquerading as real users.  
  Behavior: batch posting of comments, liking each other, and using variant text to avoid detection.  
* Auditing AI: Detection algorithm responsible for identifying and removing bot content.  
  Goal: accurately detect and remove bot content while reducing misjudgments.  
  Behavior: analysis of text patterns, user behavior, social network relationships.  
    
* Human users: real users whose behavior may be influenced by bots.  
  Goal: Obtain valuable information and engage in social interactions.  
  Behavior: Like, comment, share, report suspicious bots.


§3.2 Affordances:

* Bot-user interactions: bots mimic human user behaviors such as liking, commenting, and sharing to enhance the credibility of the content they post.  
* Confrontation between bots and auditing AI: Bots use semantic variants and social interactions to disguise themselves as real users to avoid AI detection.  
* Auditing AI's detection mechanism: Auditing AI analyzes features such as comment content, time interval, and account activity to identify bot behavior.  
* Impact of Recommendation Algorithms: Content with high interaction rates is more likely to be recommended, which may make bot content more widely distributed.

§3.3 Algorithms:

* Robot strategies:  
  Reinforcement Learning (RL) to adapt to review policies and optimize content publishing time.  
  Adversarial Text Generation to generate less detectable comments.  
  Social Graph Camouflage to increase interaction with real users.  
* Audit AI strategy:  
  Adopt Graph Neural Networks (GNNs) for bot clustering detection.  
  Combine with BERT semantic analysis to identify variant texts.  
  Time-series analysis to identify unusual posting patterns.  
* Recommender system impact:  
  Collaborative Filtering is used to decide what to recommend.  
  Content that is liked, commented, and shared by users is more likely to be recommended, potentially amplifying the influence of bots.


Section 4: Simulation Anticipated Outcomes

Instructions

Boid Flocking Model:

* Ideal for modelling the dynamic interactions of multiple subjects (bot, user, auditing AI) on a social platform.  
* Simple local rules (e.g. bot group behaviour) lead to complex global patterns (e.g. opinion manipulation on the platform).  
* We can customize rules such as “Obstacle Avoidance”, “Gathering”, “Alignment”, etc. to adjust the bot's action strategy.

What to include in this section:

A sketch or diagram of the simulation output using the mesa examples as analogy. This can be a preliminary draft version. Describe the components. You can even screen shot one of the Mesa apps and mark it up to indicate your intentions for your simulation outcome.

