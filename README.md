# BBNN Python Code

  Cartpole.py
  ----runs BBNN with custom cartpole envrionment, draws block diagrams and plots fitness at end of each epoch. This is the complete program which pretty much handles everything for the BBNN on the custom cartpole environment. Of course, this has to use your specific cartpole edits.

  wxBBNN.py
  ---- A pretty GUI which allows user to input all parameters to BBNN and then draws them. Not yet integrated with the C code for the FPGA, right now it just generates random numbers for the parameters in python. But it might be helpful if you want to integrate the pretty wxPython stuff into your code.
  
  
  BasicNN -- A collection of environments trained with a simple tflearn neural network, to varying levels of success
  
         HopperBasic.py
            ---- The hopper environment trained with a simple feed forward tflearn neural network. It doesn't really work, but        it illustrates the limits of the standard neural network when it comes to continuous control. The same network is able        to train the cartpole environment with no problem.

        Cartpole Basic
          ---- The cartpole environment trained with a basic feed forward neural network. This should achieve relative success         on this environment provided the parameters are sufficiently tuned.


  


