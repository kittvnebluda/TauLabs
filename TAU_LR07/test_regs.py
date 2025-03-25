import os
from ev3dev2.motor import LargeMotor, OUTPUT_A
from time import sleep, time
from math import cos

# --- Настройки ---
data_folder = "p_reg_data"
os.makedirs(data_folder, exist_ok=True)

# Параметры эксперимента
A = 1.0  # Амплитуда для g(t) = A
V = 1.0  # Скорость для g(t) = Vt
a = 1.0  # Ускорение для g(t) = at^2/2
A1, omega, phi1 = 2.0, 1.0, 3.14
Kp_values = [0.5, 1.0, 2.0]
Kp_Ki_values = [(0.5, 0.1), (1.0, 0.2), (2.0, 0.3)]
record_duration = 10  # Продолжительность записи в секундах

# --- Вспомогательные функции ---
def save_csv(file_path, headers, data):
    with open(file_path, 'w') as f:
        f.write(",".join(headers) + "\n")
        for row in zip(*data):
            f.write(",".join(map(str, row)) + "\n")

def pi_controller(Kp, Ki):
    global integral_error, time_prev
    integral_error = 0
    time_prev = time()
    def controller(target_angle, current_angle):
        global integral_error, time_prev
        error = target_angle - current_angle
        integral_error += error * (time() - time_prev)
        time_prev = time()
        return Kp * error + Ki * integral_error
    return controller

def special_controller():
    pass

def stationary_target(A):
    return lambda _: A

def const_vel_target(V):
    return lambda t: V * t

def const_accel_target(a):
    return lambda t: a * t^2 / 2

def sinusoidal_target(A1, omega, phi1):
    return lambda t: A1 * cos(omega * t + phi1)

# --- Основная функция записи данных ---
def record_experiment(target_function, controller, name):
    motor = LargeMotor(OUTPUT_A)
    motor.reset()

    time_data, angle_data, speed_data, error_angle_data = [], [], [], []
    start_time = time()

    while time() - start_time <= record_duration:
        current_time = time() - start_time
        target_angle = target_function(current_time)
        current_angle = motor.position / 180 * 3.14159  # Угол в радианах
        current_speed = motor.speed / 180 * 3.14159  # Скорость в рад/с
        control_signal = controller(target_angle, current_angle)

        motor.on(control_signal)

        time_data.append(current_time)
        angle_data.append(current_angle)
        speed_data.append(current_speed)
        error_angle_data.append(target_angle - current_angle)

        # sleep(0.01)  # Обновление каждые 10 мс

    motor.off()

    # Сохранение данных в файлы
    angle_file = os.path.join(data_folder, f"angle_{name}.csv")
    speed_file = os.path.join(data_folder, f"speed_{name}.csv")
    error_angle_file = os.path.join(data_folder, f"error_angle_{name}.csv")

    save_csv(angle_file, ["Time (s)", "Angle (rad)"], [time_data, angle_data])
    save_csv(speed_file, ["Time (s)", "Speed (rad/s)"], [time_data, speed_data])
    save_csv(error_angle_file, ["Time (s)", "Error (rad)"], [time_data, error_angle_data])

# --- Выполнение экспериментов ---
# П регулятор
for Kp in Kp_values:
    record_experiment(stationary_target(A), pi_controller(Kp, 0), f"g(t)={A}_Kp={Kp}")
    record_experiment(const_vel_target(V), pi_controller(Kp, 0), f"g(t)={V}*t_Kp={Kp}")

# ПИ регулятор
for Kp, Ki in Kp_Ki_values:
    record_experiment(const_vel_target(V), pi_controller(Kp, Ki), f"g(t)={V}*t_Kp={Kp}_Ki={Ki}")
    record_experiment(const_accel_target(a), pi_controller(Kp, Ki), f"g(t)={a}*t^2/2_Kp={Kp}_Ki={Ki}")

# Специальный регулятор
record_experiment(sinusoidal_target(A1, omega, phi1), special_controller(), f"g(t)={A1}*cos({omega}*t+{phi1})")
