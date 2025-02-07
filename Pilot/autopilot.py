import krpc
import math
import time


conn = krpc.connect(name = 'AutoPilot')
vessel = conn.space_center.active_vessel


#контрольные параметры
vessel.control.sas = False
vessel.control.rcs = False
vessel.auto_pilot.engage()
vessel.control.throttle = 1.0



print(vessel.name)
time.sleep(3)
print('3 seconds before the start...')
time.sleep(1)
print('2 seconds before the start...')
time.sleep(1)
print('1 second before the start...')
time.sleep(1)
print('Poehali!')


all_fuel_for_curr_stage = {
    # 0: 457,
    0: 341,
    1: 0,

}


# проверяем, достаточно ли топлива в ступени
def enough_fuel(stage):
    curr_fuel = vessel.resources.amount('LiquidFuel')
    if curr_fuel < all_fuel_for_curr_stage[stage]:
        return False
    return True

# меняем ступень
def change_stage(stage):
    vessel.control.throttle = 0.0
    time.sleep(1)
    vessel.control.activate_next_stage()
    vessel.control.throttle = 1.0
    time.sleep(1)
    print(f'{stage} stage out')
    return stage + 1

#выход на орбиту
vessel.control.activate_next_stage()
vessel.auto_pilot.target_pitch_and_heading(90, 0)
apoasis_flag = False
fl = 0


curr_stage = 0
while True:
    surface_velocity_stream = conn.add_stream(
        getattr, vessel.flight(vessel.orbit.body.reference_frame), "velocity"
    )
    surface_velocity = surface_velocity_stream()
    curr_speed = (surface_velocity[0] ** 2 + surface_velocity[1] ** 2 + surface_velocity[2] ** 2) ** 0.5


    # print(curr_speed)
    # print(vessel.resources_in_decouple_stage(0).amount('LiquidFuel'))
    # print(vessel.resources.amount('LiquidFuel'))

    altitude = vessel.flight().surface_altitude

        

    if curr_speed >= 600 and fl == 0:
        vessel.control.throttle = 0.6
        fl = 1
    
    # проверяем, достаточно ли топлива в ступени
    if not enough_fuel(curr_stage):
        curr_stage = change_stage(curr_stage)
    
    # меняем угол наклона ракеты
    if altitude < 63000:
        target_pitch = 90 * (1 - altitude / 63000)  # Чем выше высота, тем меньше наклон
        vessel.auto_pilot.target_pitch_and_heading(target_pitch, 90)
    else:
        vessel.auto_pilot.target_pitch_and_heading(0, 90)

    # вышли на требуемый апоцентр
    if (vessel.orbit.apoapsis_altitude > 270000):
        print("Needed apoasis OKed\n")
        vessel.control.throttle = 0.0
        break


altitude = vessel.flight().surface_altitude
tta = vessel.orbit.time_to_apoapsis
print(f'time to apoapsis {tta}')

while altitude < 70000:
    altitude = vessel.flight().surface_altitude
    continue
conn.space_center.warp_to(conn.space_center.ut + tta - 30)

while tta > 10:
    tta = vessel.orbit.time_to_apoapsis
    continue

vessel.control.throttle = 1.0
while abs(vessel.orbit.periapsis_altitude - vessel.orbit.apoapsis_altitude) > 190000:
    # print(vessel.resources.amount('LiquidFuel'))
    if not enough_fuel(curr_stage):
        curr_stage = change_stage(curr_stage)
    continue
vessel.control.throttle = 0.0
print('Orbit Oked')
time.sleep(3)
vessel.control.activate_next_stage()
time.sleep(10)
print(f'orbit {vessel.flight().surface_altitude} diff {vessel.orbit.periapsis_altitude - vessel.orbit.apoapsis_altitude}')




# Построение графиков
# fig1, ax1 = plt.subplots(figsize=(10, 6))
# ax1.plot(time_phys, speed_phys, label="Физическая модель", color="red")
# ax1.plot(time_auto, speed_auto, label="Автопилот", color="blue", linewidth=2)
# ax1.set_title("График скорости")
# ax1.set_xlabel("Время (с)")
# ax1.set_ylabel("Скорость (м/с)")
# ax1.legend()
# ax1.grid()