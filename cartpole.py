import gym
import serial
import matplotlib.pyplot as plt
import time
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import random
import os
import wx
from wxmplot import ImageFrame
import threading


training_time = 0.0

# width and depth, set to match up with modes.h

BBNN_WIDTH = 3
BBNN_DEPTH = 2

#output of board in form :F63\x00000000

def byteoutput_to_bin(raw_param, param_id, string_len = 32): 
    #clipped = hex_output[1:3]
  #  if clipped[1] == "\\":
   #     clipped = clipped[0]
    #integer = int(clipped)
    #print(integer)
    #binary_output = bin(integer)[2:]
    #full_param =  binary_output.zfill(string_len)




    if str(raw_param)[2] == param_id:
        right_of_id = str(raw_param).split(param_id)[1]
        left_of_slash = right_of_id.split('\\x')[0]
    else:
        right_of_idid = str(raw_param).split(param_id*2)[1]
        print(right_of_idid)
        left_of_slash = right_of_idid.split('\\x')[0]
    
    integer = int(left_of_slash)
    print(integer)
    binary_output = bin(integer)[2:]
    full_param =  binary_output.zfill(string_len)
        
    print(param_id, "param: ", full_param)


    
    return full_param
    

def move_cartpole():
    flag = ser.read()
    moved = 0
    
    #print('Waiting for moving flag')
    while (flag != b'M'):
        flag = ser.read()
    #print('moving flag received')    
    ser.write(b'K') #acknoledge
    
    while moved == 0:
        
        if (ser.read() == b'1'):
            #print('move right')
            env.step(1)
            ser.write(b'K') #acknoledge
            moved = 1
          
        if(ser.read() == b'0'):
            #Sprint('move left')
            env.step(0)
            ser.write(b'K') #acknoledge
            moved = 1
    
    moved = 0
    
def read_fitness(iteration):
    
    eol_flag = 0
    
    flag = ser.read()
    
    #print('Waiting for fitness flag')
    while (flag != b'F'):
        flag = ser.read()
    #print('fitness flag received')    
    ser.write(b'K') #acknoledge
    
    fitness = ser.read(10)
    #print(fitness)
    #fitness = fitness.decode('utf-8')
    
    fitness_read = list(fitness)
    #print(fitness_read)
    for i, char in enumerate(fitness_read):
        
        if fitness_read[i] == 0: #EOL
            if eol_flag == 0:
                eol_flag = 1                
                null_index = i
            #print(null_index)
            fitness_read[i] = 0

        
        if fitness_read[i] == 70: #F
            fitness_read[i] = 0
    
        if fitness_read[i] == 48:
            fitness_read[i] = 0
 
        if fitness_read[i] == 49:
            fitness_read[i] = 1
 
        if fitness_read[i] == 50:
            fitness_read[i] = 2
 
        if fitness_read[i] == 51:
            fitness_read[i] = 3
 
        if fitness_read[i] == 52:
            fitness_read[i] = 4
 
        if fitness_read[i] == 53:
            fitness_read[i] = 5
 
        if fitness_read[i] == 54:
            fitness_read[i] = 6
 
        if fitness_read[i] == 55:
            fitness_read[i] = 7
 
        if fitness_read[i] == 56:
            fitness_read[i] = 8
            
        if fitness_read[i] == 57:
            fitness_read[i] = 9

            
    #print(fitness_read)

    fitness_str = "".join(str(x) for x in fitness_read)    
    #print(fitness_str)    
    
    
    fitness_int = int(fitness_str)
    #print(null_index)
    print( fitness_int / (10 ** (10 - null_index) ) )
    fitness_int = fitness_int / (10 ** (10 - null_index) )
    update_plot(episode_length, fitness_int, iteration = iteration)
    
    #print('Fitness value received')  




def is_episode_end(done):
    flag = ser.read()
    #print('Waiting for checking flag')
    while (flag != b'C'):
        flag = ser.read()
    #print('checking flag received')
    
    if done == True:
        ser.write(b'D1') #Cartpole is done
        #print('Episode done')
        return True
    else:
        ser.write(b'D0') #Cartpole is not done
        #print('Episode not done')
        return False


def send_episode_length(episode_length):
    flag = ser.read()
    
    #print('Waiting for episode length flag')
    while (flag != b'E'):
        flag = ser.read()
    #print('episode length flag received')    
    
    length_string = str(episode_length).encode()
    
   
    ser.write(b'S') #START TRANSMISSION FLAG
    ser.write(b'E')
    ser.write(length_string)
    ser.write(b'E')
    
    
    #print('Trie:',tries, '. Episode length:', episode_length)
    if (trained == 0):
        #print('Generation :', generations, '\t Episode length: ', episode_length)
        print(episode_length)
        #update_plot(episode_length, fitness)
    if (trained == 1):
        print('Episode length: ', episode_length)
    
def send_new_params(pole_length):
    flag = ser.read()
    
    #print('Waiting for episode length flag')
    while (flag != b'N'):
        flag = ser.read()
    #print('episode length flag received')    
    
    pole_length_encoded =  str(round((pole_length)  ,3)).encode() #In degrees
    print(pole_length_encoded)
    
    ser.write(b'S') #START TRANSMISSION FLAG
    #ser.write(b'E')
    ser.write(pole_length_encoded)
    ser.write(b'EEEEEEEEEEEEEEE')
    
    
            

def send_status(state):
    
    #print('Waiting for listening flag')
    while (ser.read() != b'L'):
        ser.read()
        #print(ser.read())
    #print('listening flag received')   
	
    #pos_string = str(math.floor('{:.4}'.format(state[0]))).encode()
    #vel_string = str(math.floor('{:.4}'.format(state[1]))).encode()
    #angle_string = str(math.floor('{:.4}'.format(state[0]))).encode()
    
    #state0 = state[0]/2.4
    #print('X0: ', state0)
    #state1 = state[1]/10
    #print('X1: ', state1)
    #state2 = state[2]/0.419
    #print('X2: ', state2)
    #state3 = state[3]/10
    #print('X3: ', state3)
    #print('\n')
    
    pos_string =    str(round(  (state[0]/2.4)     ,4)).encode() #In degrees
    vel_string =    str(round(  (state[1]/10.0)     ,4)).encode() #In degrees
    angle_string =  str(round(  (state[2]/0.419)     ,4)).encode() #In degrees
    tip_string =    str(round(  (state[3]/10.0)        ,4)).encode() #In degrees

    #print('Send start flag')   
    ser.write(b'S') #START TRANSMISSION FLAG
    #print('Send position flag')   
    ser.write(b'P')  #next data is the position
    ser.write(pos_string)
    #print('Send velocity flag')   
    ser.write(b'V')  #next data is the speed (velocidad)
    ser.write(vel_string)
    #print('Send angle flag')   
    ser.write(b'A')  #next data is the angle
    ser.write(angle_string)
    #print('Send tip flag')   
    ser.write(b'T')  #next data is the angle
    ser.write(tip_string)
    #print('Send end flag')   
    ser.write(b'E') #END FLAG
    #print('Status sent')   


value_arrays_created = False
def update_plot(episode_length, fitness, iteration = ''):
    global value_arrays_created
    if value_arrays_created is False:
        global xVal
        global y1Val
        global y2Val
        xVal = []
        y1Val = []
        y2Val = []
        value_arrays_created = True

    plt.figure(1)
    
    xVal.append(int(generations))
    y1Val.append(int(episode_length))
    y2Val.append(int(fitness))
    
    ax1.plot(xVal, y1Val, marker='o',linestyle='--', color='r')
    ax1.tick_params(axis='y', color='r')
    ax2.plot(xVal, y2Val, marker='o',linestyle='--', color='b')
    ax2.tick_params(axis='y', color='b')        
    
    plt.savefig('fitnessgraphs/fitnessgraph{}.png'.format(generations))
 #   plt.pause(0.01)


#-----------------------creates graph----------------------

def create_graph(east,south,rows,columns,data_width = 32, iteration = ""):   #iteration is epoch
    plt.figure(2)
    plot_width = (100*columns) + ((columns+1)*50)
    plot_height = (100*rows) + ((rows+1)*50)

    fig, ax = plt.subplots(1)

    plt.xlim(0,plot_width)   #sets coordinates up 
    plt.ylim(plot_height,0)
    draw_arrows(east,south,rows,columns,data_width)
    plt.axis('off')         # turns axes off!
    ax.add_collection(draw_boxes(rows,columns))
#    plt.savefig('test.png', dpi=1000)
    plt.savefig('boxdiagrams/boxdiagram{}.png'.format(iteration))
    
    

#--------------------draws boxes on graph-------------
def draw_boxes(num_rows,num_columns):
    boxes_li = []
    for rows in range(num_rows):
        for columns in range(num_columns):
            
            xy = ( float(50 + 150*columns) , float(50 + 150*rows) )
            rect = Rectangle(xy,100.0,100.0, color = "B") 
            boxes_li.append(rect)
            
    pc = PatchCollection(boxes_li)
    return pc


#--------------------draws arrows on graph-----------    
def draw_arrows(east,south,num_rows,num_columns,data_width = 32):
    for column in range(num_columns):
        plt.arrow((100+150*column),0,0,50, head_width = 10,length_includes_head = True) #top bank of arrows
        
    index = 1
     
    for row in range(num_rows):
        for column in range(num_columns):
                
            if east[data_width - index] == '0':
                E_pos_correction = 50
                dx = - 50
            else:
                E_pos_correction = 0
                dx = 50
            E_x = (150 + 150*column + E_pos_correction)
            E_y = (100 + 150*row)
            plt.arrow(E_x,E_y,dx,0, head_width = 10,length_includes_head = True)
            
            
            if south[data_width - index] == '0':
                S_pos_correction = 0
                dy = 50
            else:
                S_pos_correction = 50
                dy = -50
            S_x = (100 + 150*column)
            S_y = (150 + 150*row + S_pos_correction)
            plt.arrow(S_x,S_y,0,dy, head_width = 10,length_includes_head = True)
            
            index += 1


def read_east():
    
    eol_flag = 0
    
    flag = ser.read()
    
    print('Waiting for east flag')
    while (flag != b'E'):
        flag = ser.read()
    print('east flag received')    
    ser.write(b'K') #acknoledge
    raw_east = ser.read(60)
    print(raw_east)
    
    east_param = byteoutput_to_bin(raw_east, 'E')
    

    return east_param

def read_south():
    string_len = 32
    eol_flag = 0
    
    flag = ser.read()
    
    print('Waiting for south flag')
    #k = 0
    while (flag != b'S' ):  #and k < 2
        flag = ser.read()
      #  if flag == b'S':
      #      k += 1
    print('south flag received')    
    ser.write(b'K') #acknoledge

    raw_south = ser.read(60)
    
    print(raw_south)
    print('raw_south type:  ', type(raw_south))

    south_param = byteoutput_to_bin(raw_south, 'S')
    
    #if str(raw_south)[2] == 'S':
    #    right_of_S = str(raw_south).split('S')[1]
    #    left_of_slash = right_of_S.split('\\x')[0]
    #else:
    #    right_of_SS = str(raw_south).split('SS')[1]
    #    print(right_of_SS)
    #    left_of_slash = right_of_SS.split('\\x')[0]
    
    #integer = int(left_of_slash)
    #print(integer)
    #binary_output = bin(integer)[2:]
    #south_param =  binary_output.zfill(string_len)
        
    #print("south param: ", south_param)

    return south_param


ser = serial.Serial('/dev/ttyUSB1', 115200)  # open serial port
print('Connected to ', ser.name)         # check which port was really used
print('\n')



print('TRAINING INITIALIZED...')         # check which port was really used
print('\n')

print('Pole length: 0.5m')

env = gym.make('CartPole-v0')

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Generation')

ax1.set_ylabel('Steps', color=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'

ax2.set_ylabel('Fitness', color=color)  # we already handled the x-label with ax1

ax1.set_ylim(0, 600)
ax2.set_ylim(0, 10000)

env.reset()
start = time.time()

env.render(mode='rgb_array')

state = env.env.state


trained = 0
trained_tries = 0
generations = 0
training = 1

episode_length = 0
fitness_int = 3500.0
fitness = 0
tries = 0
evals = 0
generations = 0
evolution_mode = 'Population'

training_time = 0.0


pole_length = 0.5
def threaded_function():
    while True:
        raw_in = input("type r and then enter to change pole length randomly")
        if raw_in == "r":
            global pole_length
    #        pole_length = random.uniform(0.5,2.0)
    #        print("NEW POLE LENGTH: ", pole_length)

            env.env.new_pole_length()
            pole_length = env.env.length

input_func = threading.Thread(target = threaded_function, daemon = True)
input_func.start()

epoch = 0 
while True:
    
    while( not env.env.done ):
        
        state = env.env.state
        
        #print('sending status')
        send_status(state = state)
        if training == 1:
            end = time.time()
            training_time = training_time + (end - start)
            #print('Training time: ', round(training_time, 1), 'seconds')
            training = 0
        
        #print('moving pole')
        move_cartpole()
        #print("pole moved")
        env.render(mode='rgb_array')
        
        #print('check episode')
        is_episode_end(env.env.done)
        episode_length += 1

    send_episode_length(episode_length)
    read_fitness(generations)
    create_graph(read_east(),read_south(), BBNN_DEPTH, BBNN_WIDTH, iteration = generations)
    print("current_pole_length: ", pole_length)
    send_new_params(pole_length)
    start = time.time()
    training = 1
    

    if (episode_length <= 2000) :
         if trained == 1:
             generations = 0
             print('System failed, retrain!')
         trained = 0
         #send_new_params()
         
    if (episode_length > 2000):
        #new pole lenght
        if trained == 0:
            print('TRAINING COMPLETE!')
            trained = 1
            
    if trained == 1:
        trained_tries += 1
            
    if trained_tries == 2 :
        trained_tries = 0
        time1 = time.time()
        
        env.env.new_pole_length()
        print('New pole length: ', round( (env.env.length), 2) )

    episode_length = 0
    
    tries += 1
    generations += 1
   
    
    
    env.reset()
    
    env.render(mode='rgb_array')    
    
    
env.env.close()
ser.close()             # close port





    







	
