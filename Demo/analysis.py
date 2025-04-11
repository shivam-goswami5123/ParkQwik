import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("parking_simulation_2025-04-03.csv")

# Convert 'Time' column to datetime format and extract hours
df['Hour'] = pd.to_datetime(df['Time'], format="%H:%M").dt.hour

# Group by hour and calculate averages
df_grouped = df.groupby("Hour")[["Vacant Spots", "Price", "Jam Factor", "Temperature (°C)"]].mean()

# Smooth Price using rolling average
df_grouped["Smoothed Price"] = df_grouped["Price"].rolling(window=3, min_periods=1).mean()

# Create a figure with two subplots
fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# 📌 Plot 1: Price vs Vacant Spots
axs[0].plot(df_grouped.index, df_grouped["Vacant Spots"], marker='o', linestyle='-', color='b', markersize=5, label="Vacant Spots")
axs[0].set_ylabel("Vacant Spots", color='b')
axs[0].tick_params(axis='y', labelcolor='b')

# Secondary Y-axis for price
ax2 = axs[0].twinx()
ax2.plot(df_grouped.index, df_grouped["Smoothed Price"], marker='D', linestyle='-', color='g', markersize=5, label="Price (Smoothed)")
ax2.set_ylabel("Price (INR)", color='g')
ax2.tick_params(axis='y', labelcolor='g')

axs[0].set_title("Price vs Vacant Spots")
axs[0].legend(loc="upper left")
ax2.legend(loc="upper right")

# 📌 Plot 2: Price vs Jam Factor & Temperature
axs[1].plot(df_grouped.index, df_grouped["Jam Factor"], marker='s', linestyle='--', color='r', markersize=5, label="Jam Factor")
axs[1].plot(df_grouped.index, df_grouped["Temperature (°C)"], marker='^', linestyle='-.', color='orange', markersize=5, label="Temperature (°C)")
axs[1].set_ylabel("Jam Factor / Temperature")
axs[1].legend(loc="upper left")
axs[1].set_title("Price Influences: Jam & Temperature")

# X-axis formatting
axs[1].set_xlabel("Hour of the Day")
axs[1].set_xticks(range(0, 24))  # Show only whole hours
axs[1].grid(True, linestyle="--", alpha=0.5)

# Show the plots
plt.tight_layout()
plt.show()
