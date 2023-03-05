# Post Indicator Valve Optimization Project

## Please visit the following link for the complete article.
[Visit My Github Repository](https://medium.com/@sainthokim/post-indicator-valve-optimization-d25d4a390b68)

## Problem Introduction
<img src=screenshots/sp.jpg width="600" />

Post indicator valves (PIVs) are above-ground access and operator valves used for automatic sprinkler systems and wet standpipe systems whose main water supply valves are located underground. PIVs may be placed in either a paved or a landscaped area and are often close to the fire department connection. A post indicator valve makes it far easier to read and operate a control valve that has been placed underground. Should a leak or break occur, the PIV can help quickly shut off the water so that no serious damage is done. For a large plant site, local regulations or the plant owner often require PIVs at multiple locations to isolate maximum 3~5 users. Users include fire hydrant, standpipe, sprinkler system, water spray system, and foam system. 

Engineering such a system often requires the engineer to manually count users and place PIVs. This is a painfully simple and repeated task for a large system of more than 100 users. Besides, the manual task makes it difficult to have an optimal number of valves as the number of possible scenarios is huge. For example, let's assume 100 users has 100 potential valve locations and the number of scenarios would follow a binormial law or two to the 100th power without a proper pruning, which is impossible to solve with a laptop computer.  

Reinforcement Learning (RL) is very robust ans fast for such a problem, giving the optimal solution based on the reward. Among various RL models, we will use Actor-Critic model with neural network. 

## Strategy to solve the problem
<img src=screenshots/p1.jpg width="600" />

The sketch above show a simplified pipeline system. The potential PIV locations are between users (nodes). For example, a PIV is marked in blue between User 12 and User 10. We can find another PIV between User 13 and User 14. Those two PIVs can isolate User 12 and 13 for emergency or maintenance. Joints are also numbered and found in the line junctions; for example, nodes 1, 3, 18, etc. This P&ID satisfies a ‘no more than 4 users between PIVs’ rule. Let’s examine the middle area. The 3 users 20, 9, and 7 can be effectively isolated by PIVs. We can approach the solution as follows.

- WebApp (app/): The web app page gets the user numbers of each pipe loop. The original format was borrowed from Udacity Data Scientist Nanodegree program and modified for PIV explanation page. Under app/templates/, find master.html that explains what Post Indicator Valve is and takes query for the valve input. In the same folder, find go.html that show the RL result of which locations a valve should be installed at.
- class Loops in loopOps.py: The method get_joints identifies the joint numbers. Joints are not counted when the users are counted between valves.
                             The method initiate_valves identifies the valve locations as tuples and put into a list: e.g., valve betwen user 13 and 14-> (13,14)
- class PIValve in pivalve.py for RL environment: From the valve list, try to drop a valve (see the method step() in the class PIValve) -> check if the rule (herein, max. 3 users between valves) is satisfied (see the method valve_checkup())-> if satisfied, return reward=1, otherwise, put a valve back in the location as in the method step(). For RL algorithm, the state is a list of valve installment (1 for installed, 0 for not installed). The state is the list of values in the dictionary self.valves.
- Do the previous step for all valve locations in the valve list -> isdone()
- Repeat the steps above utilizing Actor-Critic algorithm for a 100s epoches. See total_episodes in the piv_main.py

## Metrics
The Actor-Critic algorithm was designed to maximize the average sum of rewards (or returns). The convergence can be obtained by comparing the average sum of rewards of one epoch and that of the next and reaching to a certain threshold. The value of each state is averaged based on approximation of Belman's Equation.

## EDA
Explanatory Data Analysis was not performed for this problem as RL is not a supervised learning. The model learns more as more scenarios are explored.

## Modelling
The Actor-Critic model of MinimalRL was adapted in this modelling. Visit https://github.com/seungeunrho/minimalRL. The Actor-Critic model in this example has two neural networks: one for policy network and the other for value network. The policy network contains the input layer of size 28, the hidden layer of size 256, and the output layer of 2. The value network contains the similar network but the output layer of 1. 

The state, the list of valve installment status, is the input to those networks. The agent (Actor-Critic) returns, then, the policy of 0 (installed) or 1 (not installed) and the value of the average of total number of valves.

The environment of PIV and solution algorithm was newly introduced in this example. See the strategy above. 

## Hyperparameter tuning
The learning_rate was set to 0.0002. The decay factor gamma was set to 0.98. The number of rollout for each scenario was 10.

## Results
In the check-up process, the number of users (except joints) between PIVs are counted and compared with the limit, in this example, 3. The actions are valve placement-1; or empty-0 through the dictionary keys of valve locations in order. The following shows the solution. No PIV between User 1 and 2, 2 and 3, … and PIVs between User 7 and 21, 10 and 11, … Total number of PIVs that are used to successfully integrate the system is 11 out of total 28 potential locations.
```
{(1, 2): 0, (2, 3): 0, (3, 4): 0, (4, 6): 0, (6, 21): 0, (7, 21): 1, (7, 8): 0, (8, 9): 0, (9,20): 0, (10, 20): 0, (10, 11): 1, (1, 11): 1, (6, 17): 1, (17, 18): 0, (18, 19): 0, (15, 19): 0, (15, 16): 0, (8, 16): 1, (10, 12): 1, (14, 15): 0, (13, 14): 1, (12, 13): 0, (100, 101): 0, (3, 101): 1, (1, 100): 1, (19, 110): 1, (110, 111): 0, (14, 111): 1}
```
The following is the episode result. The 1000 episodes was examined to obtain the optimal solution; it suggests only 100 episodes would work, too. The average score converged fast; i.e., only after 20 episodes.
```
# of episode :20, avg score : 15.3
# of episode :40, avg score : 15.5
# of episode :60, avg score : 16.1
# of episode :80, avg score : 16.3
# of episode :100, avg score : 16.8
# of episode :120, avg score : 16.6
# of episode :140, avg score : 16.4
# of episode :160, avg score : 16.6
# of episode :180, avg score : 16.7
# of episode :200, avg score : 16.9
# of episode :220, avg score : 16.6
# of episode :240, avg score : 16.9
# of episode :260, avg score : 16.8
# of episode :280, avg score : 16.8
# of episode :300, avg score : 16.9
# of episode :320, avg score : 16.8
# of episode :340, avg score : 17.1
# of episode :360, avg score : 16.7
# of episode :380, avg score : 16.8
# of episode :400, avg score : 16.9
# of episode :420, avg score : 16.9
# of episode :440, avg score : 17.1
# of episode :460, avg score : 16.7
# of episode :480, avg score : 16.9
# of episode :500, avg score : 16.7
# of episode :520, avg score : 16.8
# of episode :540, avg score : 16.9
# of episode :560, avg score : 16.9
# of episode :580, avg score : 17.1
# of episode :600, avg score : 16.9
# of episode :620, avg score : 16.9
# of episode :640, avg score : 16.9
# of episode :660, avg score : 16.9
# of episode :680, avg score : 16.9
# of episode :700, avg score : 16.9
# of episode :720, avg score : 16.9
# of episode :740, avg score : 16.9
# of episode :760, avg score : 16.9
# of episode :780, avg score : 16.9
# of episode :800, avg score : 17.0
# of episode :820, avg score : 17.1
# of episode :840, avg score : 16.9
# of episode :860, avg score : 17.0
# of episode :880, avg score : 17.1
# of episode :900, avg score : 17.1
# of episode :920, avg score : 17.0
# of episode :940, avg score : 16.9
# of episode :960, avg score : 16.9
# of episode :980, avg score : 16.9
```

## Conclusion/Reflection
The RL algorithm works very well, leading to a fast and optimized result. Without such an algorithm, only a simulation would be a solution, which would result in a just fine optimized number of valves. 

## Improvements
This study is only a starting point to the PIV optimization problem. A further improvement would be explored: e.g., different valve prices, computer vision approach for the drawing recognition and automatic node numbering, etc.

## Application Explanation
A web application utilizing Flask is written under the folder app. This will take the valve list as the input and return the optimized valve locations: i.e., 
1. Web App to enter the Pipeline information and show Optimization result.
2. Reinforcement Learning Option on the back-end. 

## Installing
Clone this GIT repository:
```
git clone https://github.com/skim21/Udacity_Capstone_Project_ReinforcementLearning.git
```

## Dependencies
Please run the following on your terminal to install the required libraries.
1. Install virtual environment and activate it.
2. 'pip install -r requirements.txt' for installing the relevant packages.

## Instructions:
1. Run your web app: `python main.py`.
2. Open your browser and type `0.0.0.0:3000` in the address bar to open the homepage
3. Follow the instruction on the web app.

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Screenshot4
This is an example of a message you can type to test Machine Learning model performance.
Click **Classify Message** and the categories predicted will be highlighted in green.

<img src=screenshots/page.png width="600" />
