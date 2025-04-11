import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from tqdm import tqdm
import json

# Constants
Total_spots = 40
base_price = int(input("Enter the base price: "))
Weather_vals = ['Clear', 'Partly Cloudy', 'Cloudy', 'Overcast', 'Foggy', 'Hazy', 'Misty']
actions = [-10, 0, 10]

# Q-learning hyperparameters
Q_table = {}
alpha = 0.1
gamma = 0.9
epsilon = 0.1

# Reward tracking
daily_rewards = []
monthly_rewards = [0] * 12  # 12 months

def get_state(hour, vacant, jam, temp, weather_idx, price):
    return (hour, vacant // 5, jam, int(temp) // 5, weather_idx, int(price) // 10)

def get_weather_index(w):
    return Weather_vals.index(w)

def update_Q(state, action, reward, next_state):
    old_q = Q_table.get((state, action), 0)
    next_q = max([Q_table.get((next_state, a), 0) for a in actions])
    new_q = old_q + alpha * (reward + gamma * next_q - old_q)
    Q_table[(state, action)] = new_q
    return new_q

def enter(vacant):
    return max(0, vacant - 1)

def leave(vacant):
    return min(Total_spots, vacant + 1)

# Simulate 1 year (365 days)
start_date = datetime(2024, 1, 1)
print("\n📅 Starting year-long simulation...\n")

for day in tqdm(range(365), desc="Simulating 365 days"):
    current_time = start_date + timedelta(days=day)
    vacantSpot = 40
    price = base_price
    weather = random.choice(Weather_vals)
    total_reward_today = 0

    while current_time.date() == (start_date + timedelta(days=day)).date():
        jam = random.randint(0, 10)
        temp = round(random.uniform(10, 40), 2)
        if random.random() < 0.1:
            weather = random.choice(Weather_vals)
        weather_idx = get_weather_index(weather)
        hour = current_time.hour

        state = get_state(hour, vacantSpot, jam, temp, weather_idx, price)

        # Choose action
        if random.random() < epsilon:
            action = random.choice(actions)
        else:
            action = max(actions, key=lambda a: Q_table.get((state, a), 0))

        price = max(10, price + action)

        before = vacantSpot
        vacantSpot = random.choice([enter, leave])(vacantSpot)
        parked = max(0, before - vacantSpot)
        revenue = parked * price
        penalty = 20 if vacantSpot < 5 or vacantSpot > 35 else 0
        reward = revenue - penalty
        total_reward_today += reward

        next_state = get_state(hour, vacantSpot, jam, temp, weather_idx, price)
        update_Q(state, action, reward, next_state)

        current_time += timedelta(minutes=1)

    # Save daily & monthly rewards
    daily_rewards.append(total_reward_today)
    month_index = (start_date + timedelta(days=day)).month - 1
    monthly_rewards[month_index] += total_reward_today

# Final Q-table summary and saving
print("\n✅ Simulation complete.")
print("🏁 Top 5 most valuable (state, action) pairs learned:")
top_q = sorted(Q_table.items(), key=lambda x: x[1], reverse=True)[:5]
for (state, action), value in top_q:
    print(f"State={state}, Action={action} ➝ Q={round(value, 2)}")

# Save Q-table as JSON
serializable_Q = {str(k): v for k, v in Q_table.items()}
with open("q_table.json", "w") as f:
    json.dump(serializable_Q, f, indent=4)
print("💾 Q-table saved as 'q_table.json'")

# Plotting Monthly Rewards
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

plt.figure(figsize=(12, 6))
plt.bar(months, monthly_rewards, color='skyblue')
plt.title("📊 Monthly Total Reward - RL Parking System (1 Year)", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Total Reward")
plt.grid(axis='y')
plt.tight_layout()
plt.show()
