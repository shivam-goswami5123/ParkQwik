import random
from datetime import datetime, timedelta
from tqdm import tqdm

# Define factors
Weather_vals = ['Clear', 'Partly Cloudy', 'Cloudy', 'Overcast', 'Foggy', 'Hazy', 'Misty']

# Initial settings
Total_spots = 40
vacantSpot = 40
days_to_simulate = 365
start_time = datetime.combine(datetime.today(), datetime.min.time())
current_time = start_time

# User input
base_price = int(input("Enter the base price for today: "))
price = base_price
weather = random.choice(Weather_vals)
gross_sales = 0.0

def updatePrice():
    global price

    occupancy_factor = (Total_spots - vacantSpot) / Total_spots
    jam_factor = random.randint(0, 10)
    peak_hour_factor = 1.2 if 7 <= current_time.hour <= 9 or 17 <= current_time.hour <= 19 else 1.0
    weather_discount = 0.9 if weather in ['Foggy', 'Overcast', 'Misty'] else 1.0
    temp = round(random.uniform(10, 40), 2)
    temp_adjustment = 0.9 if temp < 15 or temp > 35 else 1.0

    price = base_price * (1 + occupancy_factor * 0.5) * (
        1 + jam_factor * 0.05) * peak_hour_factor * weather_discount * temp_adjustment
    price = round(price, 2)

def enter():
    global vacantSpot, gross_sales
    if vacantSpot > 0:
        vacantSpot -= 1
        gross_sales += price
        updatePrice()

def leave():
    global vacantSpot
    if vacantSpot < Total_spots:
        vacantSpot += 1
        updatePrice()

# Run the simulation
total_minutes = days_to_simulate * 1440
for _ in tqdm(range(total_minutes), desc="Simulating Year (365 Days)"):
    jamFactor = random.randint(0, 10)
    temp = round(random.uniform(10, 40), 2)

    if random.random() < 0.1:
        weather = random.choice(Weather_vals)

    random.choice([enter, leave])()
    current_time += timedelta(minutes=1)

# Final output
print(f"\nSimulation completed for {days_to_simulate} days!")
print(f"Gross sales for the year: ₹{round(gross_sales, 2)}")
