from collections import defaultdict
import random
import json


class Agent:

    actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def __init__(self,
                 q_table: dict = None,
                 alpha: float = 0.1,
                 gamma: float = 0.9,
                 epsilon: float = 1.0,
                 epsilon_min: float = 0.01,
                 epsilon_decay: float = 0.995,
                 learning: bool = True):

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning = learning

        self.q_table = defaultdict(
            lambda: [0.0, 0.0, 0.0, 0.0],
            q_table if q_table is not None else {}
        )

    def choose_action(self, state):
        rand = random.random()

        if self.epsilon > rand:
            return random.choice(self.actions)
        else:
            max_q_value = self.q_table[state].index(max(self.q_table[state]))
            return self.actions[max_q_value]

    def update(self, state, action, reward, next_state):
        if self.learning is False:
            exit(1)

        action_index = self.actions.index(action)
        actual_q_value = self.q_table[state][action_index]
        target = reward + self.gamma * max(self.q_table[next_state])

        self.q_table[state][action_index] = (
            actual_q_value + self.alpha * (target - actual_q_value)
        )

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

    def save(self, file_path):
        data = {str(k): v for k, v in self.q_table.items()}
        with open(file_path, "w") as f:
            json.dump(data, f)

    def load(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        self.q_table = defaultdict(
            lambda: [0.0, 0.0, 0.0, 0.0],
            {eval(k): v for k, v in data.items()}
        )
