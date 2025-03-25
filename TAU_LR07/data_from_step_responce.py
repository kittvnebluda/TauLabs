#!/usr/bin/env python3
import time
import csv
import os

from math import radians

from ev3dev2.motor import LargeMotor, OUTPUT_A

# --- Параметры ---
RECORDING_TIME = 10  # Время записи в секундах
CSV_PATH = "motor_data.csv"  # Путь для сохранения файла
MOTOR_PORT = OUTPUT_A  # Порт, к которому подключён мотор
ENV_NAME = "MOTOR_VOLT_PERCENT"

# --- Инициализация ---
motor = LargeMotor(MOTOR_PORT)

# Установка напряжения (скорость в процентах от максимума)
# Для модели EV3 максимальное напряжение 9В, 1В соответствует ~11%
motor.on(11 if os.getenv(ENV_NAME) is None else int(os.getenv(ENV_NAME)))

print("Начало записи данных...")

# --- Сбор данных ---
start_time = time.time()
data = []

try:
    while True:
        current_time = time.time() - start_time
        angle = radians(motor.position)  # Угол поворота в радианах

        # Сохраняем время и угол
        data.append((current_time, angle))

        # Завершаем запись, если вышло время
        if current_time >= RECORDING_TIME:
            break

        # time.sleep(0.01)  # Пауза для уменьшения нагрузки на процессор

finally:
    # Останавливаем мотор
    motor.off()

    # --- Сохранение данных ---
    with open(CSV_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time (s)", "Angle (radians)"])
        writer.writerows(data)

    print(f"Данные записаны в файл {CSV_PATH}")
