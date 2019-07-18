#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 11:53:50 2019

@author: Mitchell
"""
from cffi import FFI
ffi = FFI()

import numpy as np
import os



import wx
from wxmplot import ImageFrame



#width = int(input("input the width of the array: "))
#length = int(input("input the depth of the array: "))
#width = 4
#length = 4






#self.width = 0
#self.depth = 0
#self.tribes = 0
#self.noffspring = 0 
#self.sub_generations = 0
#self.age_threshold = 0
#self.batch_size = 0
#self.q_steps = 0
#self.x_weight = 0
#self.angle_weight = 0
#self.tip_acc_weight = 0
#self.x_acc_weight = 0
#self.mut_rate_wb = 0
#self.mut_low_rate_wb = 0
#self.mut_super_low_rate_wb = 0 
#self.mut_rate_nesw = 0
#self.mut_low_rate_nesw = 0
#self.mut_super_low_rate_nesw = 0
#self.loss_threshold
#self.loss_threshold_2
#self.minimum_lenght = 0
#self.continuous_mode = 0
#self.latency_mod = 0
#self.opt_latency = 0
#self.noutput_pipelined = 0
#self.random_seed
#self.extinction_rate
#self.tau = 

            
#        self.TBwidth.GetValue() = 0
#        self.TBdepth.GetValue() = 0
#        self.TBtribes.GetValue() = 0
#        self.TBnoffspring.GetValue() = 0 
#        self.TBsub_generations.GetValue() = 0
#        self.TBage_threshold.GetValue() = 0
#        self.TBbatch_size.GetValue() = 0
#        self.TBq_steps.GetValue() = 0
#        self.TBx_weight.GetValue() = 0
#        self.TBangle_weight.GetValue() = 0
#        self.TBtip_acc_weight.GetValue() = 0
#        self.TBx_acc_weight.GetValue() = 0
#        self.TBmut_rate_wb.GetValue() = 0
#        self.TBmut_low_rate_wb.GetValue() = 0
#        self.TBmut_super_low_rate_wb.GetValue() = 0 
#        self.TBmut_rate_nesw.GetValue() = 0
#        self.TBmut_low_rate_nesw.GetValue() = 0
#        self.TBmut_super_low_rate_nesw.GetValue() = 0
#        self.TBloss_threshold.GetValue()= 0
#        self.TBloss_threshold_2.GetValue() = 0
#        self.TBminimum_lenght.GetValue() = 0
#        self.TBcontinuous_mode.GetValue() = 0
#        self.TBlatency_mod.GetValue() = 0
#        self.TBopt_latency.GetValue() = 0
#        self.TBnoutput_pipelined.GetValue() = 0
#        self.TBrandom_seed.GetValue() = 0
#        self.TBextinction_rate.GetValue() = 0
#        self.TBtau.GetValue() = 0


#
#macros_tuple = 
#(('BBNN_WIDTH', 0),
#('BBNN_DEPTH' , 0),
#('TRIBES', 5), 
#('NOFFSPRING', 5),
#('SUB_GENERATIONS', 5),
#('AGE_THRESHOLD', 5),
#('BATCH_SIZE', 5),
#('Q_STEPS', 5),
#('X_WEIGHT', 5),
#('ANGLE_WEIGHT', 5),
#('TIP_ACC_WEIGHT' , 5),
#('X_ACC_WEIGHT' , 5),
#('MUT_RATE_WB' , 5),
#('MUT_LOW_RATE_WB', 5),
#('MUT_SUPER_LOW_RATE_WB', 5),
#('MUT_RATE_NESW' , 5),
#('MUT_LOW_RATE_NESW' , 5),
#('MUT_SUPER_LOW_RATE_NESW' , 5),
#('LOSS_THRESHOLD' , 5),
#('LOSS_THRESHOLD_2' , 5),
#('MINIMUN_LENGHT' , 5),
#('CONTINUOUS_MODE' , 5),
#('LATENCY_MODE' , 5),
#('OPT_LATENCY', 5),
#('NOUTPUT_PIPELINED', 5),
#('RANDOM_SEED', 0),
#('EXTINCTION_RATE', 1),
#('TAU',0.02)
#)

def create_macros(macros_tuple):
    f = open("macros.h", "w")
    f.write("#ifndef MACROS_H_ \n")
    f.write("#define MACROS_H_ \n \n")
            
    for variable_tuple in macros_tuple:
        f.write("#define {}   {} \n".format(variable_tuple[0],variable_tuple[1]))
        
    f.write("#define CARTPOLE \n")    
    f.write("\n#endif \n")
    
    f.close()            


# ----------------build library------------------

def build_library():
    ffi.cdef("int fakemain();")
    
    
    ffi.set_source("_BBNNbuild1",  # name of the output C extension
    """
        #include "config.h"
        #include "acrobot.h"
        #include "bbnn_evolution.h"
        #include "cartpole.h"
        #include "continuous_mountaincar.h"
        #include "macros.h"
        #include "modes.h"
        #include "mountaincar.h"
        #include "physic_models.h"
        #include "q_training.h"
        
    """,
        sources=['main.c','acrobot.c','bbnn_evolution.c','cartpole.c',
                 'config.c','continuous_mountaincar.c', 'mountaincar.c',
                 'physic_models.c', 'q_training.c'],
        libraries = ['m'])  
    
#    ffi.compile(verbose=True)
        

# ---------------creates graph-----------
def create_graph(east,south,rows,columns, iteration, data_width = 32):
    import matplotlib.pyplot as plt
    
    
    
    plot_width = (100*columns) + ((columns+1)*50)
    plot_height = (100*rows) + ((rows+1)*50)

    fig, ax = plt.subplots(1)

    plt.xlim(0,plot_width)   #sets coordinates up 
    plt.ylim(plot_height,0)
    draw_arrows(east,south,rows,columns,data_width)
    plt.axis('off')         # turns axes off!
    ax.add_collection(draw_boxes(rows,columns))
    plt.savefig('BBNNimages/BBNNimage{}.png'.format(iteration+1), dpi=1000)
    plt.show()
    
    

#--------------------draws boxes on graph-------------
def draw_boxes(num_rows,num_columns):
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Rectangle
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
    import matplotlib.pyplot as plt
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
                
    

#---------------makes list of parameter tuples given the saved file-------------
def make_param_lists(file,rows,columns,data_width = 32):
    
    
    coord_list = []
    for x, line in enumerate(file):
        line.replace("\n","")
        
        split_li = line.split("  ")
    
        
        E_bin = str(bin(abs(int(split_li[0]))))[2:]
        S_bin = str(bin(abs(int(split_li[1]))))[2:]
        
        E_short = E_bin[-(rows*columns):]
        S_short = S_bin[-(rows*columns - columns):]
        
        final_E = E_short.rjust(data_width,"0")
        final_S = S_short.rjust(data_width,"0")
        
        
        clean_tup = (final_E,final_S)
        
        coord_list.append(clean_tup)
        
    file.close()   
    return coord_list

        





class FirstScreen(wx.Frame):
    def __init__(self, parent,id):
        wx.Frame.__init__(self, parent, id, "BBNN Generator", size = (500,500))
        
        self.panel_1 = wx.Panel(self)
 
       
        
#        width_txt = wx.TextEntryDialog(None, "Type BBNN Width:", "Width:","0")
#        if width_txt.ShowModal() == wx.ID_OK:
#            answer = width_txt.GetValue()
        
        self.g_button = wx.Button(self.panel_1,label = "Generate", pos = (350,440),size = (100,40))
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.g_button)
        
        
# ----------------------------------- create captions ---------------------------        
        wx.StaticText(self.panel_1,-1,"Width of BBNN:",pos = (30,20))
        wx.StaticText(self.panel_1,-1,"Depth of BBNN:",pos = (30,50))
        wx.StaticText(self.panel_1,-1,"Tribes:",pos = (30,80))
        wx.StaticText(self.panel_1,-1,"Noffspring:",pos = (30,110))
        wx.StaticText(self.panel_1,-1,"Sub Generations:",pos = (30,140))
        wx.StaticText(self.panel_1,-1,"Age Threshold:",pos = (30,170))
        wx.StaticText(self.panel_1,-1,"Batch Size:",pos = (30,200))
        wx.StaticText(self.panel_1,-1,"Q Steps:",pos = (30,230))
        wx.StaticText(self.panel_1,-1,"X Weight:",pos = (30,260))
        wx.StaticText(self.panel_1,-1,"Angle Weight:",pos = (30,290))
        wx.StaticText(self.panel_1,-1,"Tip Acc Weight:",pos = (30,320))
        wx.StaticText(self.panel_1,-1,"X Acc Weight:",pos = (30,350))
        wx.StaticText(self.panel_1,-1,"Mut Rate WB:",pos = (30,380))
        wx.StaticText(self.panel_1,-1,"Mut Low Rate Wb:",pos = (30,410))
        wx.StaticText(self.panel_1,-1,"Mut Super Low Rate WB:",pos = (220,20))
        wx.StaticText(self.panel_1,-1,"Mut Rate NESW:",pos = (220,50))
        wx.StaticText(self.panel_1,-1,"Mut Low Rate NESW:",pos = (220,80))
        wx.StaticText(self.panel_1,-1,"MUT Super Low Rate NESW:",pos = (220,110))
        wx.StaticText(self.panel_1,-1,"Loss Threshold:",pos = (220,140))
        wx.StaticText(self.panel_1,-1,"Loss Threshold 2:",pos = (220,170))
        wx.StaticText(self.panel_1,-1,"Minimum Lenght:",pos = (220,200))
        wx.StaticText(self.panel_1,-1,"Continuous Mode:",pos = (220,230))
        wx.StaticText(self.panel_1,-1,"Latency Mode:",pos = (220,260))
        wx.StaticText(self.panel_1,-1,"Opt latency:",pos = (220,290))
        wx.StaticText(self.panel_1,-1,"Noutput Pipelined:",pos = (220,320))
        wx.StaticText(self.panel_1,-1,"Random Seed:",pos = (220,350))
        wx.StaticText(self.panel_1,-1,"Extinction Rate:",pos = (220,380))
        wx.StaticText(self.panel_1,-1,"Tau:",pos = (220,410))
        
        
# ---------------------------  Create buttons and map them to "self.TBvariable" -----------
        self.TBwidth = wx.TextCtrl(self.panel_1, -1,'5',pos = (150,20), size = (50,-1))
        self.TBdepth = wx.TextCtrl(self.panel_1, -1,'4',pos = (150,50), size = (50,-1))
        self.TBtribes = wx.TextCtrl(self.panel_1, -1,'5',pos = (150,80), size = (50,-1))
        self.TBnoffspring = wx.TextCtrl(self.panel_1, -1,'2',pos = (150,110), size = (50,-1)) 
        self.TBsub_generations = wx.TextCtrl(self.panel_1, -1,'3',pos = (150,140), size = (50,-1))
        self.TBage_threshold = wx.TextCtrl(self.panel_1, -1,'5',pos = (150,170), size = (50,-1))
        self.TBbatch_size = wx.TextCtrl(self.panel_1, -1,'5',pos = (150,200), size = (50,-1))
        self.TBq_steps = wx.TextCtrl(self.panel_1, -1,'5',pos = (150,230), size = (50,-1))
        self.TBx_weight = wx.TextCtrl(self.panel_1, -1,'5',pos = (150,260), size = (50,-1))
        self.TBangle_weight = wx.TextCtrl(self.panel_1, -1,'5',pos = (150,290), size = (50,-1))
        self.TBtip_acc_weight = wx.TextCtrl(self.panel_1, -1,'5',pos = (150,320), size = (50,-1))
        self.TBx_acc_weight = wx.TextCtrl(self.panel_1, -1,'5',pos = (150,350), size = (50,-1))
        self.TBmut_rate_wb = wx.TextCtrl(self.panel_1, -1,'.4',pos = (150,380), size = (50,-1))
        self.TBmut_low_rate_wb = wx.TextCtrl(self.panel_1, -1,'.2',pos = (150,410), size = (50,-1))
        self.TBmut_super_low_rate_wb = wx.TextCtrl(self.panel_1, -1,'0.1',pos = (400,20), size = (50,-1))
        self.TBmut_rate_nesw = wx.TextCtrl(self.panel_1, -1,'.4',pos = (400,50), size = (50,-1))
        self.TBmut_low_rate_nesw = wx.TextCtrl(self.panel_1, -1,'.2',pos = (400,80), size = (50,-1))
        self.TBmut_super_low_rate_nesw = wx.TextCtrl(self.panel_1, -1,'0.1',pos = (400,110), size = (50,-1))
        self.TBloss_threshold = wx.TextCtrl(self.panel_1, -1,'5000',pos = (400,140), size = (50,-1))
        self.TBloss_threshold_2 = wx.TextCtrl(self.panel_1, -1,'500',pos = (400,170), size = (50,-1))
        self.TBminimum_lenght = wx.TextCtrl(self.panel_1, -1,'2000',pos = (400,200), size = (50,-1))
        self.TBcontinuous_mode = wx.TextCtrl(self.panel_1, -1,'5',pos = (400,230), size = (50,-1))
        self.TBlatency_mode = wx.TextCtrl(self.panel_1, -1,'5',pos = (400,260), size = (50,-1))
        self.TBopt_latency = wx.TextCtrl(self.panel_1, -1,'5',pos = (400,290), size = (50,-1))
        self.TBnoutput_pipelined = wx.TextCtrl(self.panel_1, -1,'5',pos = (400,320), size = (50,-1))
        self.TBrandom_seed = wx.TextCtrl(self.panel_1, -1,'1',pos = (400,350), size = (50,-1))
        self.TBextinction_rate = wx.TextCtrl(self.panel_1, -1,'3',pos = (400,380), size = (50,-1))
        self.TBtau = wx.TextCtrl(self.panel_1, -1,'0.005',pos = (400,410), size = (50,-1))
        
        frame2 = SecondScreen(parent = None, id = -1)
        frame2.Show()
            
        
        
        
        
    
    def OnClose(self, event):
        
        macros_tuple = (('BBNN_WIDTH', int(self.TBwidth.GetValue())), 
                ('BBNN_DEPTH' , int(self.TBdepth.GetValue())),
                ('TRIBES', int(self.TBtribes.GetValue())), 
                ('NOFFSPRING', int(self.TBnoffspring.GetValue())),
                ('SUB_GENERATIONS', int(self.TBsub_generations.GetValue())),
                ('AGE_THRESHOLD', int(self.TBage_threshold.GetValue())),
                ('BATCH_SIZE', int(self.TBbatch_size.GetValue())),
                ('Q_STEPS', int(self.TBq_steps.GetValue())),
                ('X_WEIGHT', int(self.TBx_weight.GetValue())),
                ('ANGLE_WEIGHT', int(self.TBangle_weight.GetValue())),
                ('TIP_ACC_WEIGHT' , int(self.TBtip_acc_weight.GetValue())),
                ('X_ACC_WEIGHT' , int(self.TBx_acc_weight.GetValue())),
                ('MUT_RATE_WB' , float(self.TBmut_rate_wb.GetValue())),
                ('MUT_LOW_RATE_WB', float(self.TBmut_low_rate_wb.GetValue())),
                ('MUT_SUPER_LOW_RATE_WB', float(self.TBmut_super_low_rate_wb.GetValue())),
                ('MUT_RATE_NESW' , float(self.TBmut_rate_nesw.GetValue())),
                ('MUT_LOW_RATE_NESW' , float(self.TBmut_low_rate_nesw.GetValue())),
                ('MUT_SUPER_LOW_RATE_NESW' , float(self.TBmut_super_low_rate_nesw.GetValue())),
                ('LOSS_THRESHOLD' , int(self.TBloss_threshold.GetValue())),
                ('LOSS_THRESHOLD_2' , int(self.TBloss_threshold_2.GetValue())),
                ('MINIMUN_LENGHT' , int(self.TBminimum_lenght.GetValue())),
                ('CONTINUOUS_MODE' , int(self.TBcontinuous_mode.GetValue())),
                ('LATENCY_MODE' ,  int(self.TBlatency_mode.GetValue())),
                ('OPT_LATENCY', int(self.TBopt_latency.GetValue())),
                ('NOUTPUT_PIPELINED',  int(self.TBnoutput_pipelined.GetValue())),
                ('RANDOM_SEED', int(self.TBrandom_seed.GetValue())),
                ('EXTINCTION_RATE', int(self.TBextinction_rate.GetValue())),
                ('TAU', float(self.TBtau.GetValue()))
        )
                            
        
        create_macros(macros_tuple)
        build_library()
        ffi.compile(verbose=True)
        from _BBNNbuild1.lib import fakemain
        fakemain()
        outputs = open("outputs.txt","r")
        generated_list = make_param_lists(outputs,int(self.TBwidth.GetValue()),int(self.TBdepth.GetValue()),32)
#        os.remove("outputs.txt")
        for i, x in enumerate(generated_list):
        
        
            create_graph(x[0],x[1], int(self.TBwidth.GetValue()), int(self.TBdepth.GetValue()), i)
            print("E_param: {},  S_param:{}".format(x[0],x[1]))
            print("\n\n\n")
        
        
        
#        

            
#        img_frame = ImageFrame(mode='intensity')
#        img_frame.display(data, x=x0, y=y0)
#        img_frame.Show()
#            
        self.Close(True)
##        
        

class SecondScreen(wx.Frame):
    def __init__(self, parent,id):
        wx.Frame.__init__(self, parent, id, "Generated Graphs", size = (800,500))
        
        
#        self.Img = wx.Image("BBNNimages/BBNNimage{}.png".format(1), wx.BITMAP_TYPE_ANY)
#        W = self.Img.GetWidth()
#        H = self.Img.GetHeight()
        
        self.panel_1 = wx.Panel(self)
        
        self.img = wx.StaticBitmap(self, -1, wx.Bitmap("BBNNimages/BBNNimage1.png", wx.BITMAP_TYPE_ANY))
        
        
        self.next_button = wx.Button(self.panel_1,label = "next", pos = (420,440),size = (100,40))
        self.Bind(wx.EVT_BUTTON, self.forward, self.next_button)
       
        self.back_button = wx.Button(self.panel_1,label = "back", pos = (280,440),size = (100,40))
        self.Bind(wx.EVT_BUTTON, self.back, self.back_button)
        
        

                  
    
    def forward():
        pass
    def back():
        pass
        
#     
        
        
        

    
    
  
#    
#    def closebutton(self, event):
#        self.Close(True)
#    def closewindow(self, event):
#        self.Destroy()
#        
#        self.togglebuttonstart = wx.ToggleButton(id = -1, label = "generate", pos = (550,550))
        
        
        
        
#        entry = wx.TextEntryDialog.Create(self, parent = None,message = "test 1", caption = "caption")
        
#        
#class Main(wx.Frame):
#    def __init__(self):
#        wx.Frame.__init__(self, parent = None, title = "BBNN Generator", size = (600,600))
#        
#       
#        
#        wx.Button(self,label = "Generate BBNN",pos = (200,500))
#        wx.Button(self,id = wx.ID_FORWARD)
#        
#        wx.Button(self,id = wx.ID_FORWARD)
#        self.SetBackgroundColour

        

        
        
    
        
if __name__ == '__main__':
    

    
    app = wx.App(False)
    frame1 = FirstScreen(parent = None, id = -1)
    frame1.Show()
    
    
   
#    while frame1.width != 0 and frame1.depth != 0 and frame1.data_size != 0:
    
    
    app.MainLoop()
    
    
    
    
#if __name__ == '__main__':  
#    ffi.compile(verbose=True)
#    
#    fakemain()
#    outputs = open("outputs.txt","r")
#    generated_list = make_param_lists(outputs,width,length,32)
#    
#    for x in generated_list:
#        
#        
#        create_graph(x[0],x[1], width, length,32)
#        print("E_param: {},  S_param:{}".format(x[0],x[1]))
#        print("\n\n\n")
#    
#    
