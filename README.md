# BBNN Python Code

Cartpole.py
  ----runs BBNN with custom cartpole envrionment, draws block diagrams and plots fitness at end of each epoch. This is the complete program which pretty much handles everything for the BBNN on the custom cartpole environment. Of course, this has to use your specific cartpole edits.

wxBBNN.py
  ---- A pretty GUI which allows user to input all parameters to BBNN and then draws them. Not yet integrated with the C code for the FPGA, right now it just generates random numbers for the parameters in python. But it might be helpful if you want to integrate the pretty wxPython stuff into your code.
  
  
BasicNN -- A collection of environments trained with a simple tflearn neural network, to varying levels of success
  
 --HopperBasic.py
            ---- The hopper environment trained with a simple feed forward tflearn neural network. It doesn't really work, but        it illustrates the limits of the standard neural network when it comes to continuous control. The same network is able        to train the cartpole environment with no problem.

 --Cartpole Basic
          ---- The cartpole environment trained with a basic feed forward neural network. This should achieve relative success         on this environment provided the parameters are sufficiently tuned.

Continuous Control --  A collection of different machine learning/neural network algortihms more suited for continuous control, i.e. for the roboschool hopper env.

   --DDPG--- A folder with an implementation of the Deep Deterministic Policy Gradient (DDPG) Algorithm, originally                 created by Ignacio Carlucho and tested on the continuous mountain car env. I have added code for running the same             algorithm on the hopper. Over a long period of testing this algorithm is able to train the hopper to jump rather               quickly https://github.com/IgnacioCarlucho/DDPG_MountainCar.git  
                --- for the roboschool hopper implementation, run hopperDDPG.py while in the DDPG folder
                
   --RL_experiments ---- a big folder with a bunch of reinforcement learning algorithms I found via Andre Sprenger-                 https://github.com/asprenger/rl-experiments.git  
          I used it to test OpenAi's PPO (Proximal Policy Optimization) algorithm on the hopper, which might be the best                 algorithm for continuous control. To run the hopper on this algorithm, call "rlexperiments/ppo/train_mujoco.py"               while in the RL_experiments folder.
          
          
          

