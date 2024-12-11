import pandas as pd
import matplotlib.pyplot as plt
import argparse

# --- Аргументы командной строки ---
parser = argparse.ArgumentParser(description="Visualize motor data from a CSV file.")
parser.add_argument("csv_file", type=str, help="Path to the CSV file")
args = parser.parse_args()

# --- Параметры ---
CSV_PATH = args.csv_file  # Путь к CSV-файлу

# --- Чтение данных из CSV с помощью pandas ---
df = pd.read_csv(CSV_PATH)
df.set_index("Time (s)", inplace=True)

print(df.head())

df.plot()
plt.title("Motor Data Visualization")
plt.grid()
plt.show()
