# Smart-Cab-with-Qlearning-and-SARSA

This project was associated with "[MAT-DSAM3A] Advanced Data Assimilation and Modeling A: Reinforcement Learning", Summer Semester 2021, for my Masters of Science: Data Science, University of Potsdam, Germany.

The folder, "Smart Cab RL" contains 4 subfolder: "Smart Cab Q-learning", "Smart Cab Q-Learning REWARD=0", "Smart Cab SARSA", "Smart Cab SARSA REWARD=0".
Each of these folder contains the file for running or training the smart cab using Q-learning and SARSA algorithm with different reward function.

To run/train the smart cab:
1) Open command prompt, cmd.
2) Change the directory to whichever smart cab you want to run/train.
3) type: "python RL.py", and hit enter.
4) It will the ask for your input: "Enter 'TRAIN' to train or 'RUN' to run the game:"
5) type 'RUN' or 'TRAIN' and it will do the required task.

## MOTIVATION
• To study and compare Q Learning and SARSA algorithm. <Br/>
• Model free and Model based RL algorithm. <Br/>
• Approach Temporal difference learning learns how to predict a quantity that depends on future values of a
given signal learns from experience. <Br/>
• Temporal difference update step: <Br/>
  
      𝑁𝑒𝑤𝐸𝑠𝑡𝑖𝑚𝑎𝑡𝑒 ← 𝑂𝑙𝑑𝐸𝑠𝑡𝑖𝑚𝑎𝑡𝑒 + 𝑆𝑡𝑒𝑝𝑠𝑖𝑧𝑒[𝑇𝑎𝑟𝑔𝑒𝑡 − 𝑜𝑙𝑑𝐸𝑠𝑡𝑖𝑚𝑎𝑡𝑒]

## SMART CAB GAME

• Inspired from OpenAI gym environment. <Br/>
• 2D grid 5x5 cells. <Br/>
• Agent Cab <Br/>
• Drop off and pick up locations. <Br/>
• Objective of the game: <Br/>
1. pick up the passenger.
2. drop off the passenger at the right location.
3. take as minimum time as possible. <Br/>

• Coordinate System: See Screenshot. <Br/>
• Pickup positions: [0, 0], [0, 4], [4, 0] and [4, 3]. <Br/>
• Dropoff positions: [0, 0], [0, 4], [4, 0] and [4, 3]. <Br/>
• Rules: <Br/>
1. Drop off location should not be equal to Pickup location in one episode.
2. Cab cannot go through the walls.
3. Cab can move “UP”, “DOWN”, “LEFT”, and “RIGHT. No Diagonal
4. Cannot go beyond the extreme rows and columns.

## Grid
![Grid](https://user-images.githubusercontent.com/31696557/131404076-1858a8a4-fa64-4ab0-9535-1f0af25221b3.png)

## STATE SPACES

![State space 4](https://user-images.githubusercontent.com/31696557/131404807-073b7ba4-fa27-4a3d-9630-97bdd941741f.PNG) <Br/>
Total number of States = 52 + 336 = 388


![State Space 2](https://user-images.githubusercontent.com/31696557/131404856-2c37d751-ad6a-4c66-8abc-389cb240ce81.PNG) <Br/>
21x16 = 336 States


![State Space](https://user-images.githubusercontent.com/31696557/131404928-9931e3cc-321a-4f7a-a5b0-abcf36e28f9b.PNG) <Br/>
13x4 = 52 States


## SARSA
• On policy learning.  <Br/>
• Learning rate, **𝛼=0.1**  <Br/>
• Discount factor, **𝛾=1**  <Br/>
• 𝜀 greedy algorithm, **𝜀=0.4**(Slightly more chances for exploitation than exploration).  <Br/>
• Balances exploitation and exploration.  <Br/>
• Tries to go to each states.  <Br/>
• Trained for 500,000 episodes.  <Br/>
• Total average cumulative reward, **25.12** , with reward = 0 for picking up from the right location.  <Br/>
• Total average cumulative reward, **5.72** , with reward = 30 for picking up from the right location.  <Br/>

## 
![Cumulative Reward per episode SARSA (REWARD=0) Top 1000](https://user-images.githubusercontent.com/31696557/131405523-fe5ed24d-90e1-4d2a-b0f1-757f1e36b38e.jpg)

![Cumulative Reward per episode SARSA Top 1000](https://user-images.githubusercontent.com/31696557/131405581-fd3a5d57-d7bb-4881-8f42-c664740c3e8a.jpg)

## Q-LEARNING
• Off policy learning.  <Br/>
• Learning rate, **𝛼=0.1**.  <Br/>
• Discount factor, **𝛾=1**.  <Br/>
• Trained for **500,000** episodes.  <Br/>
• Total average cumulative reward **10.92** , with reward = 0 for picking up from the right location.  <Br/>
• Total average cumulative reward **0.9812** , with reward = 30 for picking up from the right location.  <Br/>

![Cumulative Reward per episode Q-Learning (Reward=0) Top 1000](https://user-images.githubusercontent.com/31696557/131405891-2e318c43-1112-4be9-8b95-33b95c14af20.jpg)  <Br/>


![Cumulative Reward per episode Q-Learning Top 1000](https://user-images.githubusercontent.com/31696557/131405960-3c867a9b-5da9-4390-adf1-06e1bf44e9fd.jpg)  <Br/>

## SARSA Vs. Q-LEARNING

![Average Cumulative  reward per 500 episode - SARSA Vs  Q Learning (REWARD = 0)](https://user-images.githubusercontent.com/31696557/131406241-64f126e9-7593-4617-8024-be58015cae0d.jpg)  <Br/>

![Average Cumulative  reward per 500 episode - SARSA Vs  Q Learning](https://user-images.githubusercontent.com/31696557/131406272-4c888f39-8c9f-4a15-965e-59b5384e554a.jpg)
