#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:48:58 2019

@author: Mitchell
"""


import matplotlib.pyplot as plt
import gym
import random
import time
import numpy as np
from roboschool.scene_abstract import cpp_household
from roboschool.gym_forward_walker import RoboschoolForwardWalker

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter


init_time = time.time()
LR = 1e-3
env = gym.make('RoboschoolHopper-v1')
env.reset()
goal_steps = 500
score_requirement = 25.0
initial_games = 1000
epochs = 3


def some_random_games_first():
    for episode in range(5):
        env.reset()
        for t in range(goal_steps):
#            env.render()
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            print(reward)
            if done:
                break

def initial_population():
    training_data = []
    scores = []
    accepted_scores = []
    for _ in range(initial_games):
        if _ % 100 == 0:
            print(_)
        score = 0
        game_memory = []
        prev_observation = []
        for x in range(goal_steps):

            action = env.action_space.sample()

            observation, reward, done, info = env.step(action)


            if len(prev_observation) > 0:
                game_memory.append([prev_observation ,action])

            prev_observation = observation

            score += reward
#            if x > 15:
#                score += .5
#            if x > 10:
#                score += .3
#            if x> 5:
#                score += .1
#
            if done:
#                print(x)
                break
        scores.append(score)
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                training_data.append(data)
        env.reset()


    training_data_save = np.array(training_data)
    np.save('saved.npy', training_data_save)
    avg_untrained = sum(scores)/len(scores)
    print("Average of all scores: ", avg_untrained)
    print('Average accepted score:', mean(accepted_scores))
    print('Median accepted score:', median(accepted_scores))
    print(len(training_data))
    return training_data


def neural_network_model(input_size):

    network = input_data(shape=[None, input_size, 1], name='input')

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, 0.8)

#    network = fully_connected(network, 1024, activation='relu')
#    network = dropout(network, 0.8)
#
#    network = fully_connected(network, 2048, activation='relu')
#    network = dropout(network, 0.8)
#
#    network = fully_connected(network, 4096, activation='relu')
#    network = dropout(network, 0.8)
#
#    network = fully_connected(network, 2048, activation='relu')
#    network = dropout(network, 0.8)
#
#    network = fully_connected(network, 1024, activation='relu')
#    network = dropout(network, 0.8)
#
#    network = fully_connected(network, 512, activation='relu')
#    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 3, activation= 'linear')



    network = regression(network, optimizer='adam', learning_rate=LR,
                         loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(network, tensorboard_dir='log')

    return model


def train_model(training_data, model = False):

    x = np.array([i[0] for i in training_data])
    print(x.shape)

    X = x.reshape(-1, len(training_data[0][0]),1)
    print(X.shape)
#    X = np.array([i[0] for i in training_data])
    y = np.array([i[1] for i in training_data])
    print(y.shape)
    print(len(y))
    print(y[0])
#    print(X)
#    print(len(X))
#    print(X[0])

    if not model:
        model = neural_network_model(input_size = len(X[0]))

    model.fit({'input': X}, {'targets': y}, n_epoch= epochs, snapshot_step=500,
              show_metric=True, run_id='openai_learning')

    return model



training_data = initial_population()

model = train_model(training_data)

trained_time = time.time()

print('TOTAL TRAINING TIME: ', (trained_time - init_time))


scores = []
choices = []
f = open("actions_and_scores.txt", "w")
games_to_play = 50
for each_game in range(games_to_play):
    score = 0
    game_memory = []
    prev_obs = []
    env.reset()
    for _ in range(goal_steps):
        env.render()

        if len(prev_obs)==0:
            action = env.action_space.sample()
            f.write("EMPTY")
        else:
            action = model.predict(prev_obs.reshape(-1,len(prev_obs),1))[0]
            print(action)

        choices.append(action)


        new_observation, reward, done, info = env.step(action)
        prev_obs = new_observation
        game_memory.append([new_observation, action])
        score+=reward

        f.write("action: {},  score: {} \n".format(action, score))

        if done:
            env.reset()
            break

    scores.append(score)
f.close()
env.close()

print('TOTAL TRAINING TIME: ', (trained_time - init_time))
print('Average Score:',sum(scores)/len(scores))
#print('choice 1:{}  choice 0:{}'.format(choices.count(1)/len(choices),choices.count(0)/len(choices)))
print(score_requirement)
print('choice 1:{}  choice 0:{}'.format(choices[1],choices[0]))
