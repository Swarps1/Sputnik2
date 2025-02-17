import matplotlib.pyplot as plt
import numpy as np

# Импорт функций физической модели
from mymodel import solve_ivp, equations, earth_r

# Импорт автопилота
from mypilot import main as run_autopilot, time_data,  x_data, y_data, z_data, speed_data, speed_x_data, speed_y_data, speed_z_data, altitude_data,  pitch_data

# Выполняем автопилот
run_autopilot()

# Данные из физической модели
t_eval = np.linspace(0, 205, 1000)
solution = solve_ivp(equations, (0, 250), [0, earth_r, 0, 0, 90], t_eval=t_eval)
time_phys = solution.t
x, y, vx, vy, _ = solution.y

speed_phys = np.sqrt(vx**2 + vy**2)
height_phys = (y - earth_r) / 1000

# Данные из автопилота
time_auto = time_data
speed_auto = speed_data
height_auto = altitude_data

speed_x_data = np.array(speed_x_data)
speed_y_data = np.array(speed_y_data)
speed = np.sqrt(speed_y_data**2 + speed_x_data**2)

# fig3, (ax4, ax5) = plt.subplots(2, 1, figsize=(10, 12))

# # График высоты
# ax4.plot(time_phys, y - earth_r, label="Физическая модель", color="green")
# ax4.set_xlabel("Время (с)")
# ax4.set_ylabel("Высота (м)")
# ax4.legend()
# ax4.grid()

# # График скорости от времени

# ax5.plot(time_phys, vy, label="Скорость от времени", color="green")
# ax5.set_xlabel("Время (с)")
# ax5.set_ylabel("Скорость (м/с)")
# ax5.set_title("Скорость ракеты от времени")
# ax5.legend()
# ax5.grid()

# # Построение графиков из данных автопилота
# fig1, axs1 = plt.subplots(2, 1, figsize=(10, 10))

# # График высоты
# axs1[0].plot(time_auto, altitude_data, label="Высота", color="blue", linewidth=2)
# axs1[0].set_xlabel("Время (с)")
# axs1[0].set_ylabel("Высота (м)")
# axs1[0].set_title("График высоты от времени")
# axs1[0].legend()
# axs1[0].grid()

# axs1[1].plot(time_data, speed_x_data, label="Скорость X", color="red")
# axs1[1].set_title("График скорости по X")
# axs1[1].set_xlabel("Время (с)")
# axs1[1].set_ylabel("Скорость (м/с)")
# axs1[1].legend()
# axs1[1].grid()




# Сравнение Графиков

fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)  

# --- График физической модели ---
axs[0].plot(time_phys, y - earth_r, label="Физическая модель", color="green")
axs[0].set_ylabel("Высота (м)")
axs[0].set_title("Сравнение высоты: Физическая модель vs Автопилот")
axs[0].legend()
axs[0].grid()

# --- График высоты автопилота ---
axs[1].plot(time_auto, altitude_data, label="Автопилот", color="blue", linewidth=2)
axs[1].set_xlabel("Время (с)")
axs[1].set_ylabel("Высота (м)")
axs[1].legend()
axs[1].grid()

# Создаем фигуру с двумя подграфиками (2 строки, 1 столбец)
fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)  

# --- График скорости от времени (Физическая модель) ---
axs[0].plot(time_phys, vy, label="Скорость (Физ. модель)", color="green")
axs[0].set_ylabel("Скорость (м/с)")
axs[0].set_title("Скорость ракеты от времени")
axs[0].legend()
axs[0].grid()

# --- График скорости по X (Автопилот) ---
axs[1].plot(time_data, speed_x_data, label="Скорость ракеты", color="red")
axs[1].set_xlabel("Время (с)")
axs[1].set_ylabel("Скорость (м/с)")
axs[1].set_title("График скорости ракеты")
axs[1].legend()
axs[1].grid()


fig, ax = plt.subplots(figsize=(10, 6))
# Первый график (Физическая модель)
ax.plot(time_phys, y - earth_r, label="Физическая модель", color="green")
# Второй график (Автопилот)
ax.plot(time_auto, altitude_data, label="Автопилот", color="blue", linewidth=2)
# Настройки осей и заголовка
ax.set_xlabel("Время (с)")
ax.set_ylabel("Высота (м)")
ax.set_title("График высоты от времени")
ax.legend()
ax.grid()


fig, ax = plt.subplots(figsize=(10, 6))
# Первый график (Скорость от времени)
ax.plot(time_phys, vy, label="Скорость ракеты (Физическая модель)", color="green")
# Второй график (Скорость X)
ax.plot(time_data, speed_x_data, label="Скорость ракеты (Автопилот)", color="red")
# Настройки осей и заголовка
ax.set_xlabel("Время (с)")
ax.set_ylabel("Скорость (м/с)")
ax.set_title("График скорости от времени")
ax.legend()
ax.grid()


# axs1[1].plot(time_data, speed, label="Скорость от времени", color="green", linewidth=2)
# axs1[1].set_xlabel("Время (с)")
# axs1[1].set_ylabel("Скорость (м/с)")
# axs1[1].set_title("Скорость ракеты от времени")
# axs1[1].legend()
# axs1[1].grid()


# Создаем графики
# fig2, (ax2, ax3) = plt.subplots(2, 1, figsize=(10, 12))

# # График скорости по X
# ax2.plot(time_phys, vx, label="Физическая модель (Vx)", color="green")
# ax2.set_xlabel("Время (с)")
# ax2.set_ylabel("Скорость по X (м/с)")
# ax2.legend()
# ax2.grid()

# # График скорости по Y
# ax3.plot(time_phys, vy, label="Физическая модель (Vy)", color="green")
# ax3.set_xlabel("Время (с)")
# ax3.set_ylabel("Скорость по Y (м/с)")
# ax3.legend()
# ax3.grid()

# fig2, ax = plt.subplots(figsize=(10, 5))  # Создаем только один график вместо массива осей

# # График скорости по X
# ax.plot(time_auto, speed_x_data, label="Скорость X", color="red")
# ax.set_title("График скорости по X")
# ax.set_xlabel("Время (с)")
# ax.set_ylabel("Скорость (м/с)")
# ax.legend()
# ax.grid()

# axs2[2].plot(time_data, speed_z_data, label="Скорость Z", color="green")
# axs2[2].set_title("График скорости по Z")
# axs2[2].set_xlabel("Время (с)")
# axs2[2].set_ylabel("Скорость (м/с)")
# axs2[2].legend()
# axs2[2].grid()

# fig3, axs3 = plt.subplots(3, 1, figsize=(10, 15))

# # Графики смещения
# axs3[0].plot(time_auto, x_data, label="X", color="red")
# axs3[0].set_title("Смещение по X")
# axs3[0].grid()

# axs3[1].plot(time_auto, y_data, label="Y", color="blue")
# axs3[1].set_title("Смещение по Y")
# axs3[1].grid()

# axs3[2].plot(time_auto, z_data, label="Z", color="green")
# axs3[2].set_title("Смещение по Z")
# axs3[2].grid()
# График смещения по X
# ax5.plot(time_phys, x, label="Физическая модель", color="green")
# ax5.set_xlabel("Время (с)")
# ax5.set_ylabel("Смещение по X (м)")
# ax5.legend()
# ax5.grid()

# # График смещения по X
# ax5.plot(time_phys, x, label="Физическая модель", color="green")
# ax5.set_xlabel("Время (с)")
# ax5.set_ylabel("Смещение по X (м)")
# ax5.legend()
# ax5.grid()

# speed_x_data = np.array(speed_x_data)
# speed_y_data = np.array(speed_y_data)
# time_data = np.array(time_data)

# speed = np.sqrt(speed_y_data**2 + speed_x_data**2)

# plt.figure(figsize=(10, 6))
# plt.plot(time_data, speed, label="Скорость от времени", color="green")
# plt.xlabel("Время (с)")
# plt.ylabel("Скорость (м/с)")
# plt.title("Скорость ракеты от времени")
# plt.legend()
# plt.grid()

# # График наклона
# axs1[1].plot(time_auto, pitch_data, label="Наклон", color="green", linewidth=2)
# axs1[1].set_xlabel("Время (с)")
# axs1[1].set_ylabel("Градусы")
# axs1[1].set_title("График наклона от времени")
# axs1[1].legend()
# axs1[1].grid()

plt.show()
