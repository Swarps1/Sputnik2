import krpc
import math
import time
import matplotlib.pyplot as plt
import numpy as np

all_fuel_for_curr_stage = {
    0: 341,  # Количество топлива для первой ступени
    1: 0,    # Вторая ступень (отсутствует)
}

# Данные для графиков
x_data = []
y_data = []
z_data = []

speed_data = []
speed_x_data = []
speed_y_data = []
speed_z_data = []

altitude_data = []
mass_data = []
time_data = []
pitch_data = []

def main():
    conn = krpc.connect(name='AutoPilot')
    vessel = conn.space_center.active_vessel
    ap = vessel.auto_pilot
    control = vessel.control

    # Контрольные параметры
    control.sas = False
    control.rcs = False
    ap.engage()

    # Опорные координаты
    body = conn.space_center.bodies['Kerbin']
    position = vessel.position(body.reference_frame)
    x0, y0, z0 = position

    # Проверка топлива в ступени
    def enough_fuel(stage):
        return vessel.resources.amount('LiquidFuel') >= all_fuel_for_curr_stage[stage]

    # Смена ступени
    def change_stage(stage):
        control.throttle = 0.0
        time.sleep(1)
        control.activate_next_stage()
        control.throttle = 1.0
        time.sleep(1)
        print(f'{stage} stage out')
        return stage + 1

    # Добавление данных о скорости
    def add_spd(spd_x, spd_y, spd_z):
        speed_data.append(math.sqrt(spd_x**2 + spd_y**2 + spd_z**2))
        speed_x_data.append(spd_x)
        speed_y_data.append(spd_y)
        speed_z_data.append(spd_z)

    # Добавление координатных данных
    def add_point(x, y, z):
        x_data.append(math.sqrt(x**2 + y**2))
        y_data.append(y)
        z_data.append(z)

    # Добавление информации о полете
    def add_inf(altit, mass, curr_time, ptch):
        altitude_data.append(altit)
        mass_data.append(mass)
        time_data.append(curr_time)
        pitch_data.append(ptch)

    # Подготовка к запуску
    control.throttle = 1.0
    print(vessel.name)
    for i in range(3, 0, -1):
        print(f'{i} секунд до старта...')
        time.sleep(1)
    print('Поехали!')

    # Запуск
    control.activate_next_stage()
    ap.target_pitch_and_heading(90, 0)
    apoapsis_flag = False
    throttle_flag = 0

    t0 = time.time()
    altitude = vessel.flight().surface_altitude
    add_inf(round(altitude), vessel.mass, 0, 90)
    add_point(0, 0, 0)
    add_spd(0, 0, 0)

    surface_velocity_stream = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), "velocity")

    curr_stage = 0
    while True:
        surface_velocity = surface_velocity_stream()
        curr_speed = math.sqrt(sum(v**2 for v in surface_velocity))
        altitude = vessel.flight().surface_altitude

        # Регулировка тяги
        if curr_speed >= 600 and throttle_flag == 0:
            control.throttle = 0.6
            throttle_flag = 1

        # Проверка топлива и смена ступени
        if not enough_fuel(curr_stage):
            curr_stage = change_stage(curr_stage)

        # Изменение угла наклона ракеты
        if altitude < 63000:
            target_pitch = 90 * (1 - altitude / 63000)
        else:
            target_pitch = 0
        ap.target_pitch_and_heading(target_pitch, 90)

        # Выход на требуемую высоту апоапсиса
        if vessel.orbit.apoapsis_altitude > 270000:
            print("Достигнута требуемая высота апоапсиса\n")
            control.throttle = 0.0
            break

        # Запись данных
        nowt = round(time.time() - t0)
        pos = vessel.position(body.reference_frame)
        x, y, z = pos[0] - x0, pos[1] - y0, pos[2] - z0

        add_inf(altitude, vessel.mass, nowt, target_pitch)
        add_point(x, y, z)
        add_spd(*surface_velocity)

    altitude = vessel.flight().surface_altitude
    tta = vessel.orbit.time_to_apoapsis
    print(f'time to apoapsis {tta}')

    
    while tta > 10:
        tta = vessel.orbit.time_to_apoapsis

        surface_velocity = surface_velocity_stream()
        curr_speed = math.sqrt(sum(v**2 for v in surface_velocity))
        altitude = vessel.flight().surface_altitude

        nowt = round(time.time() - t0)
        pos = vessel.position(body.reference_frame)
        x, y, z = pos[0] - x0, pos[1] - y0, pos[2] - z0

        add_inf(altitude, vessel.mass, nowt, target_pitch)
        add_point(x, y, z)
        add_spd(*surface_velocity)
        continue
    # # Построение графиков
    # fig1, axs1 = plt.subplots(2, 1, figsize=(10, 10))

    # # График высоты
    # axs1[0].plot(time_data, altitude_data, label="Высота", color="blue", linewidth=2)
    # axs1[0].set_xlabel("Время (с)")
    # axs1[0].set_ylabel("Высота (м)")
    # axs1[0].set_title("График высоты от времени")
    # axs1[0].legend()
    # axs1[0].grid()

    # # График наклона
    # axs1[1].plot(time_data, pitch_data, label="Наклон", color="green", linewidth=2)
    # axs1[1].set_xlabel("Время (с)")
    # axs1[1].set_ylabel("Градусы")
    # axs1[1].set_title("График наклона от времени")
    # axs1[1].legend()
    # axs1[1].grid()

    # fig2, axs2 = plt.subplots(3, 1, figsize=(10, 15))

    # # Графики скоростей
    # axs2[0].plot(time_data, speed_x_data, label="Скорость X", color="red")
    # axs2[0].set_title("График скорости по X")
    # axs2[0].set_xlabel("Время (с)")
    # axs2[0].set_ylabel("Скорость (м/с)")
    # axs2[0].legend()
    # axs2[0].grid()

    # axs2[1].plot(time_data, speed_y_data, label="Скорость Y", color="blue")
    # axs2[1].set_title("График скорости по Y")
    # axs2[1].set_xlabel("Время (с)")
    # axs2[1].set_ylabel("Скорость (м/с)")
    # axs2[1].legend()
    # axs2[1].grid()

    # axs2[2].plot(time_data, speed_z_data, label="Скорость Z", color="green")
    # axs2[2].set_title("График скорости по Z")
    # axs2[2].set_xlabel("Время (с)")
    # axs2[2].set_ylabel("Скорость (м/с)")
    # axs2[2].legend()
    # axs2[2].grid()

    # fig3, axs3 = plt.subplots(3, 1, figsize=(10, 15))

    # # Графики смещения
    # axs3[0].plot(time_data, x_data, label="X", color="red")
    # axs3[0].set_title("Смещение по X")
    # axs3[0].grid()

    # axs3[1].plot(time_data, y_data, label="Y", color="blue")
    # axs3[1].set_title("Смещение по Y")
    # axs3[1].grid()

    # axs3[2].plot(time_data, z_data, label="Z", color="green")
    # axs3[2].set_title("Смещение по Z")
    # axs3[2].grid()

    # plt.show()

if __name__ == "__main__":
    main()
