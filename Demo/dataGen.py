import random
import csv
from datetime import datetime, timedelta
from tqdm import tqdm

# Define factors
factors = ['Weather', 'Time', 'Date', 'Temp', 'Jam Factor', 'Price', 'Vacant Spot']
Weather_vals = ['Clear', 'Partly Cloudy', 'Cloudy', 'Overcast', 'Foggy', 'Hazy', 'Misty']

# Initial conditions
Total_spots = 40
vacantSpot = 40  # Total parking spots
start_time = datetime.combine(datetime.today(), datetime.min.time())  # 00:00 today
end_time = start_time + timedelta(days=1)  # 24-hour simulation
current_time = start_time

# Initialize weather
weather = random.choice(Weather_vals)  # Set an initial weather condition

base_price = int(input("Enter the base price for today: "))
price = base_price  # Initial price


def updatePrice():
    """Dynamically adjusts the parking price based on various factors."""
    global price

    # Dynamic multiplier calculations
    occupancy_factor = (Total_spots - vacantSpot) / Total_spots  # Higher means fewer vacant spots
    jam_factor = random.randint(0, 10)  # Simulate traffic congestion
    peak_hour_factor = 1.2 if 7 <= current_time.hour <= 9 or 17 <= current_time.hour <= 19 else 1.0  # Peak hours

    # Weather-based adjustments
    weather_discount = 0.9 if weather in ['Foggy', 'Overcast', 'Misty'] else 1.0  # Discount in bad weather

    # Temperature-based discount (Encourage parking in extreme conditions)
    temp = round(random.uniform(10, 40), 2)
    temp_adjustment = 0.9 if temp < 15 or temp > 35 else 1.0

    # Final price calculation
    price = base_price * (1 + occupancy_factor * 0.5) * (
                1 + jam_factor * 0.05) * peak_hour_factor * weather_discount * temp_adjustment
    price = round(price, 2)  # Keep it clean with 2 decimal places


def record(current_time, jamFactor, vacantSpot, weather, temp, price):
    """Records the data into a CSV file."""
    date = current_time.date()
    time_str = current_time.strftime("%H:%M")

    with open(f"parking_simulation_{date}.csv", mode='a', newline="") as file:
        writer = csv.writer(file)

        if file.tell() == 0:  # Write headers if the file is new
            writer.writerow(["Time", "Date", "Temperature (°C)", "Jam Factor", "Vacant Spots", "Weather", "Price"])

        writer.writerow([time_str, date, temp, jamFactor, vacantSpot, weather, price])


def enter():
    """Simulates a car entering the parking lot."""
    global vacantSpot
    if vacantSpot > 0:
        vacantSpot -= 1
        updatePrice()


def leave():
    """Simulates a car leaving the parking lot."""
    global vacantSpot
    if vacantSpot < 40:
        vacantSpot += 1
        updatePrice()


# Simulate the entire day
for _ in tqdm(range(1440), desc="Simulating Day (24 Hours)"):  # 1440 minutes in a day

    # Simulate changing conditions
    jamFactor = random.randint(0, 10)  # Random traffic congestion
    temp = round(random.uniform(10, 40), 2)  # Temperature variation
    weather = random.choice(Weather_vals) if random.random() < 0.1 else weather  # Change weather 10% of the time

    # Randomly decide whether a car enters or leaves
    random.choice([enter, leave])()

    # Record the data
    record(current_time, jamFactor, vacantSpot, weather, temp, price)

    # Increment time by 1 minute
    current_time += timedelta(minutes=1)

print("Simulation completed! Data saved.")

