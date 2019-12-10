import gym
import gym_song
import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median

LR = 1e-3

env = gym.make('song-v1')

env.reset()

goal_moves = 40

score_requirement = -50
initial_games = 100000

def some_random_games():
    for episode in range(5):
        env.reset()
        for t in range(goal_moves):
            action = random.randint(0, 2)
            observation, reward, done, info = env.step(action)
            if done:
                break

def initial_population():
    training_data = []
    scores = []
    accepted_scores = []
    for _ in range(initial_games):
        score = 0
        game_memory = []
        prev_observation = []
        for _ in range(goal_moves):
            action = random.randint(0, 2)
            observation, reward, done, info = env.step(action)
            game_memory.append([observation, action])

            score += reward

            if done:
                break

        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                if data[1] == 1:
                    output = [0, 1]

                elif data[1] == 0:
                    output = [1, 0]

                training_data.append([data[0], output])

        env.reset()
        scores.append(score)

    training_data_save = np.array(training_data)
    np.save("saved.npy", training_data_save)

    print("average accepted score:", mean(accepted_scores))

    return training_data

def neural_network_model(input_size):
    network = input_data(shape=[None, input_size, 1], name='input')

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, .8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, .8)
    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, .8)
    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, .8)
    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, .8)

    network = fully_connected(network, 2, activation='softmax')

    network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')
    model = tflearn.DNN(network, tensorboard_dir='log')

    return model

def train_model(training_data, model=False):
    X = np.array([i[0] for i in training_data]).reshape(-1, 1, 1)
    Y = [i[1] for i in training_data]

    if not model:
        model = neural_network_model(input_size = len(X[0]))

    model.fit({'input': X}, {'targets': Y}, n_epoch = 1, snapshot_step = 500, show_metric=True, run_id='openAI')

    return model

training_data = initial_population()
model = train_model(training_data)


scores = []
choices = []
for each_game in range(10):
    score = 0
    game_memory = []
    prev_obs = 0
    env.reset()
    for _ in range(goal_moves):
        

        if prev_obs == 0:
            action = random.randrange(0,2)
        else:
            action = np.argmax(model.predict(np.array(prev_obs).reshape(-1, 1, 1))[0])

        choices.append(action)
                
        new_observation, reward, done, info = env.step(action)
        prev_obs = new_observation
        game_memory.append([new_observation, action])
        score+=reward
        if done: break

    scores.append(score)

print('Average Score:',sum(scores)/len(scores))
