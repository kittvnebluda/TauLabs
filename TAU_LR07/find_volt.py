import time
from ev3dev2.motor import LargeMotor, OUTPUT_A
from ev3dev2.power import PowerSupply
import os

# --- Константы ---
MOTOR_PORT = OUTPUT_A  # Порт мотора
TARGET_VOLTAGE = 1.0  # Целевое напряжение (Вольты)
STEP_PERCENT = 1  # Шаг изменения мощности (%)
MAX_PERCENT = 100  # Максимальная мощность (%)
EPS = 0.05  # Погрешность, В
DELAY = 0.5  # Пауза между изменениями мощности, c
ENV_NAME = "MOTOR_VOLT_PERCENT"  # Имя переменной среды для результата

# --- Инициализация ---
motor = LargeMotor(MOTOR_PORT)
power_supply = PowerSupply()


# --- Функция подбора мощности ---
def find_target_power():
    print("Начало подбора мощности для достижения 1В потребления...")
    for percent in range(0, MAX_PERCENT + 1, STEP_PERCENT):
        try:
            motor.on(percent)
            time.sleep(DELAY)  # Дать мотору стабилизироваться

            # Считывание текущего напряжения
            volts = power_supply.measured_volts
            print(f"Скважность: {percent}%, Напряжение: {volts:.2f} В")

            if abs(volts - TARGET_VOLTAGE) < EPS:
                print(f"Найдена подходящая мощность: {percent}% при напряжении {volts:.2f} В")
                return percent

        except KeyboardInterrupt:
            print("Подбор мощности остановлен пользователем.")
            break

    print("Подходящая мощность не найдена.")
    return None


if __name__ == "__main__":
    try:
        target_power = find_target_power()

        if target_power is not None:
            # Сохраняем результат в переменную среды
            os.environ[ENV_NAME] = str(target_power)
            print(f"Результат записан в переменную среды: {ENV_NAME}={target_power}")
        else:
            print("Не удалось найти подходящую мощность.")

    finally:
        motor.off()
        print("Мотор остановлен.")
