import numpy as np
import mlflow
import matplotlib.pyplot as plt

class AirlineEnvironment:
    def __init__(self, base_price=2000, total_seats=100, features=None):
        self.base_price = base_price
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.max_days = 30
        self.current_day = 0
        self.features = features or {
            "wifi": 200, 
            "in_flight_meals": 500, 
            "extra_legroom": 1000,
            # Add more features here...
        }
        self.active_features = {feature: False for feature in self.features}

    def reset(self):
        self.available_seats = self.total_seats
        self.current_day = 0
        self.active_features = {feature: False for feature in self.features}
        return self.get_state()

    def get_state(self):
        active_feature_count = sum(self.active_features.values())
        return (self.max_days - self.current_day, self.available_seats, active_feature_count)

    def step(self, action):
        if action < 3:
            price_change = [-200, 0, 200][action]
            current_price = self.base_price + price_change
        else:
            feature = list(self.features.keys())[action - 3]
            self.active_features[feature] = not self.active_features[feature]
            current_price = self.base_price + self.get_feature_price()

        booking_probability = max(0.05, 1.0 - (current_price - self.base_price) / 200)
        booked = np.random.random() < booking_probability
        revenue = current_price if booked and self.available_seats > 0 else 0
        if booked and self.available_seats > 0:
            self.available_seats -= 1

        self.current_day += 1
        done = self.current_day >= self.max_days or self.available_seats == 0
        next_state = self.get_state()

        # Calculate Profit/Loss (P&L)
        cost = sum(self.features[feature] for feature in self.active_features if self.active_features[feature])
        profit_loss = revenue - cost
        
        return next_state, revenue, booked, done, profit_loss

    def get_feature_price(self):
        return sum(price for feature, price in self.features.items() if self.active_features[feature])


class QLearningAgent:
    def __init__(self, environment, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0):
        self.env = environment
        self.q_table = np.zeros((environment.max_days + 1, environment.total_seats + 1, len(environment.features) + 3))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = 0.99
        self.training_rewards = []
        self.total_bookings = []  # Track total bookings per episode
        self.total_revenue = []   # Track total revenue per episode
        self.profit_loss = []     # Track profit/loss per episode

    def choose_action(self, state):
        if np.random.random() < self.exploration_rate:
            return np.random.choice(range(self.q_table.shape[2]))
        else:
            days_left, seats_left, _ = state
            return np.argmax(self.q_table[days_left, seats_left])

    def train(self, episodes=500):
        with mlflow.start_run():
            mlflow.log_param("learning_rate", self.learning_rate)
            mlflow.log_param("discount_factor", self.discount_factor)
            mlflow.log_param("episodes", episodes)

            for episode in range(episodes):
                state = self.env.reset()
                total_reward = 0
                total_booking = 0
                total_revenue = 0
                total_profit_loss = 0  # Track total profit/loss for the episode
                while True:
                    action = self.choose_action(state)
                    next_state, reward, booked, done, profit_loss = self.env.step(action)
                    days_left, seats_left, _ = state
                    next_days_left, next_seats_left, _ = next_state

                    old_value = self.q_table[days_left, seats_left, action]
                    next_max = np.max(self.q_table[next_days_left, next_seats_left])

                    new_value = old_value + self.learning_rate * (reward + self.discount_factor * next_max - old_value)
                    self.q_table[days_left, seats_left, action] = new_value

                    state = next_state
                    total_reward += reward
                    total_booking += booked
                    total_revenue += reward
                    total_profit_loss += profit_loss  # Accumulate profit/loss
                    if done:
                        break

                self.training_rewards.append(total_reward)
                self.total_bookings.append(total_booking)
                self.total_revenue.append(total_revenue)
                self.profit_loss.append(total_profit_loss)  # Store profit/loss for the episode
                self.exploration_rate *= self.exploration_decay
                np.save("q_table.npy", self.q_table)
                mlflow.log_artifact("q_table.npy")

            self.plot_training_rewards()

    def plot_training_rewards(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.training_rewards, label='Total Reward per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Total Reward')
        plt.title('Training Rewards over Episodes')
        plt.legend()
        plt.grid()
        plot_path = "training_rewards_plot.png"
        plt.savefig(plot_path)
        plt.close()
        mlflow.log_artifact(plot_path)
