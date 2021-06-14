import numpy as np
import gym
import torch as T
from time import time

from ExperienceReplay import ExperienceReplay
from DDQN import DeepQNetwork
import config

LEARNING_RATE = 1e-3
REFRESH_MODEL_FREQ = 50

def run(agentId):
    experienceReplay = ExperienceReplay(agentId, config.HOST, config.USER, config.PASSWORD, config.DATABASE)

    env = gym.make("LunarLander-v2")

    model = DeepQNetwork(LEARNING_RATE, n_actions=4, input_dims=8, fc1_dims=256, fc2_dims=256)
    model.load_state_dict(T.load('/mnt/share/model.pt', map_location='cpu'), strict=False)

    counter = 0
    ep_counter = 0
    while True:
        timeStart = time()
        s = env.reset()
        done = False
        step_counter = 0
        ep_reward = 0

        while not done:

            state = T.tensor([s]).to(model.device)
            actions = model.forward(state)
            a = T.argmax(actions).item()

            s_, r, done, _ = env.step(a)

            experienceReplay.remember(s, a, r, s_, done)

            s = s_

            step_counter += 1
            ep_reward += r
            counter += 1
            if counter % REFRESH_MODEL_FREQ:
                while True:
                    if experienceReplay.databaseHandler.isReadyToRead():
                        experienceReplay.databaseHandler.updateRWStatus(agentId, True)
                        model.load_state_dict(T.load('/mnt/share/model.pt', map_location='cpu'), strict=False)
                        experienceReplay.databaseHandler.updateRWStatus(agentId, False)
                        break

        ep_counter += 1
        timeTaken = time() - timeStart
        res = f'Ep {ep_counter} | Rew: {ep_reward:.2f} | Len: {step_counter} | Dur: {timeTaken:.2f}s'
        print(res)


if __name__ == "__main__":
    agentId = input("Agent ID: ")
    print(f"Running as Agent {agentId}")
    run(agentId)



