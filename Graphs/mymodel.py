import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Константы Кербина
Temp = 300  # Температура (не используется в коде)
R = 8.310  # Универсальная газовая постоянная (не используется)
earth_r = 600_000  # Радиус Кербина (м)
earth_mass = 5.2915158e22  # Масса Кербина (кг)
G = 6.67430e-11  # Гравитационная постоянная (м³/кг/с²)
g0 = 9.81  # Ускорение свободного падения (м/с²)
H = 5000  # Высота масштаба атмосферы (м)
p0 = 1.225  # Плотность воздуха на уровне моря (кг/м³)

# Ракетные параметры
T_stage1 = 1_545_575  # Тяга первой ступени (Н)
T_stage2 = 326_351  # Тяга второй ступени (Н)
Isp1 = 280  # Удельный импульс первой ступени (с)
Isp2 = 280  # Удельный импульс второй ступени (с)
m0 = 50_782  # Начальная масса ракеты (кг)
m_stage1 = 33_760  # Масса первой ступени (кг)
m_stage2 = 17_022  # Масса второй ступени (кг)=
Cd = 0.2  # Коэффициент лобового сопротивления
A = 1.4  # Площадь поперечного сечения ракеты (м²)

# Времена событий (разделение ступеней)
stage_1_sep = 120  # Отделение первой ступени (с)
stage_2_sep = 180  # Отделение второй ступени (с)

# Целевая высота апоапсиса
apoapsis_target = 270_000  # м

# Функции для вычислений
def rho(h):
    """Возвращает плотность атмосферы на высоте h."""
    return p0 * np.exp(-h / H) if h > 0 else p0

def g(h):
    """Возвращает гравитационное ускорение на высоте h."""
    return G * earth_mass / ((earth_r + h) ** 2)

def thrust(t):
    """Возвращает текущую тягу ракеты."""
    if t < stage_1_sep:
        return T_stage1
    elif t < stage_2_sep:
        return T_stage2
    return 0

def mass(t):
    """Возвращает текущую массу ракеты."""
    if t < stage_1_sep:
        return m0 - (T_stage1 / (Isp1 * g0)) * t
    elif t < stage_2_sep:
        return m0 - m_stage1 - (T_stage2 / (Isp2 * g0)) * (t - stage_1_sep)
    return max(m0 - m_stage1 - m_stage2, 1)  # Не даем массе стать нулевой

def equations(t, state):
    """Система дифференциальных уравнений для движения ракеты."""
    x, y, vx, vy, theta = state
    h = max(0, y - earth_r)

    # Обновление угла поворота
    if h < 63_000:
        theta = np.radians(90 * (1 - h / 63_000))
    else:
        theta = 0

    v = np.sqrt(vx**2 + vy**2)
    m = mass(t)
    T = thrust(t)

    # Силы и ускорения
    drag = 0.5 * Cd * rho(h) * A * v**2
    ax = (T * np.cos(theta) - drag * (vx / v)) / m if v > 0 else 0
    ay = (T * np.sin(theta) - drag * (vy / v)) / m - g(h) if v > 0 else -g(h)

    return [vx, vy, ax, ay, theta]

# Начальные условия
x0, y0 = 0, earth_r
vx0, vy0 = 0, 0
theta0 = np.radians(90)  # Начальный угол в радианах
state0 = [x0, y0, vx0, vy0, theta0]

# Временной диапазон
t_span = (0, 200)
t_eval = np.linspace(t_span[0], t_span[1], 1000)

# Условие остановки (достижение целевого апоапсиса)
def terminate_event(t, state):
    return state[1] - earth_r - apoapsis_target

terminate_event.terminal = True
terminate_event.direction = 1

# Решение уравнений
solution = solve_ivp(equations, t_span, state0, t_eval=t_eval, events=terminate_event)

# Извлечение данных
t = solution.t
x, y, vx, vy, theta = solution.y

# Перевод в километры
x_km = x / 1000
y_km = (y - earth_r) / 1000

# # Построение графиков
# plt.figure(figsize=(10, 6))
# plt.plot(x_km, y_km, label="Траектория ракеты", color="red")
# plt.xlabel("Горизонтальное расстояние (км)")
# plt.ylabel("Высота (км)")
# plt.title("Траектория полета ракеты")
# plt.legend()
# plt.grid()
# plt.show()

# # График высоты от времени
# plt.figure(figsize=(10, 6))
# plt.plot(t, y_km, label="Высота от времени", color="blue")
# plt.xlabel("Время (с)")
# plt.ylabel("Высота (км)")
# plt.title("Высота ракеты от времени")
# plt.legend()
# plt.grid()
# plt.show()

# # График скорости от времени
# speed = np.sqrt(vx**2 + vy**2)
# plt.figure(figsize=(10, 6))
# plt.plot(t, speed, label="Скорость от времени", color="green")
# plt.xlabel("Время (с)")
# plt.ylabel("Скорость (м/с)")
# plt.title("Скорость ракеты от времени")
# plt.legend()
# plt.grid()
# plt.show()
