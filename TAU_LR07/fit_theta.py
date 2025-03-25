import argparse

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scipy.optimize import curve_fit

# --- Аргументы командной строки ---
parser = argparse.ArgumentParser(description="Visualize motor data from a CSV file and fit a model.")
parser.add_argument("csv_file", type=str, help="Path to the CSV file")
args = parser.parse_args()

# --- Параметры ---
CSV_PATH = args.csv_file  # Путь к CSV-файлу

# --- Чтение данных из CSV с помощью pandas ---
data = pd.read_csv(CSV_PATH)

# --- Модель для аппроксимации ---
def theta_model(t, k, T):
    return k * (T * np.exp(-t / T) + t - T)

# --- МНК для определения параметров k и T ---
if "Time (s)" in data.columns and "Angle (radians)" in data.columns:
    time = data["Time (s)"].values
    angle = data["Angle (radians)"].values

    # Инициализация параметров и аппроксимация
    initial_guess = [1.0, 1.0]  # Начальные значения для k и T
    popt, _ = curve_fit(theta_model, time, angle, p0=initial_guess)
    k, T = popt

    # Расчёт аппроксимированной функции
    fitted_angle = theta_model(time, k, T)

    # Вывод параметров
    print(f"Оптимальные параметры: k = {k:.4f}, T = {T:.4f}")

    # --- Визуализация ---
    plt.figure(figsize=(10, 6))

    # Оригинальные данные
    plt.plot(time, angle, label="Original Data", linestyle='-', marker='o')

    # Аппроксимированные данные
    plt.plot(time, fitted_angle, label=f"Fitted Model (k={k:.4f}, T={T:.4f})", linestyle='--')

    plt.xlabel("Time (s)")
    plt.ylabel("Angle (radians)")
    plt.title("Motor Angle Data and Fitted Model")
    plt.legend()
    plt.grid()
    plt.show()
else:
    print("Ошибка: В CSV-файле должны быть колонки 'Time (s)' и 'Angle (radians)'.")
