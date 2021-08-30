# Smart-Cab-with-Qlearning-and-SARSA

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

## REWARD FUNCTION
```math
𝑅𝑒𝑤𝑎𝑟𝑑(𝑠,𝑎)=−1𝑓𝑜𝑟𝑒𝑣𝑒𝑟𝑦𝑠𝑡𝑒𝑝−10𝑝𝑖𝑐𝑘𝑢𝑝𝑓𝑟𝑜𝑚𝑤𝑟𝑜𝑛𝑔𝑙𝑜𝑐𝑎𝑡𝑖𝑜𝑛−10𝑑𝑟𝑜𝑝𝑜𝑓𝑓𝑎𝑡𝑤𝑟𝑜𝑛𝑔𝑙𝑜𝑐𝑎𝑡𝑖𝑜𝑛+30𝑜𝑟0𝑝𝑖𝑐𝑘𝑢𝑝𝑓𝑟𝑜𝑚𝑟𝑖𝑔ℎ𝑡𝑙𝑜𝑐𝑎𝑡𝑖𝑜𝑛+20𝑑𝑟𝑜𝑝𝑜𝑓𝑓𝑎𝑡𝑟𝑖𝑔ℎ𝑡𝑙𝑜𝑐𝑎𝑡𝑖𝑜𝑛
```

<img src="https://render.githubusercontent.com/render/math?math=e^{i \pi} = -1">


![formula](https://render.githubusercontent.com/render/math?math=e^{i \pi} = -1)
