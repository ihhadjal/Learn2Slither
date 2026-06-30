from collections import defaultdict
import random
import json
from pathlib import Path
from datetime import datetime


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
            q_values = self.q_table[state]
            max_q = max(q_values)
            best_actions = [
                a for a, q in zip(self.actions, q_values) if q == max_q
            ]
            return random.choice(best_actions)

    def update(self, state, action, reward, next_state, done):
        if self.learning is False:
            return

        action_index = self.actions.index(action)
        actual_q_value = self.q_table[state][action_index]

        if done:
            target = reward
        else:
            target = reward + self.gamma * max(self.q_table[next_state])
        self.q_table[state][action_index] = (
            actual_q_value + self.alpha * (target - actual_q_value)
        )

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

    def save(self, file_path):
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_path = path.with_name(f"{path.stem}_{timestamp}{path.suffix}")

        data = {str(k): v for k, v in self.q_table.items()}

        with open(new_path, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self, file_path):
        self.epsilon = 0
        with open(file_path, 'r') as f:
            data = json.load(f)
        self.q_table = defaultdict(
            lambda: [0.0, 0.0, 0.0, 0.0],
            {eval(k): v for k, v in data.items()}
        )
