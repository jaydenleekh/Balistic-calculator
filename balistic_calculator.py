import tkinter as tk
from tkinter import messagebox
import math


# =========================
# 기본 물리 상수
# =========================

g = 9.81
R = 287.05
Rv = 461.5

V0 = 225       # 초기속도 고정
DIAMETER = 0.081
CD = 0.3


# =========================
# 공기 계산
# =========================

def vapor_pressure(temp):

    return 610.78 * math.exp(
        (17.27 * temp) /
        (temp + 237.3)
    )


def air_density(temp, pressure_hpa, humidity):

    pressure = pressure_hpa * 100

    T = temp + 273.15

    es = vapor_pressure(temp)

    e = humidity / 100 * es


    rho = (
        (pressure - e) / (R*T)
        +
        e / (Rv*T)
    )

    return rho



def drag_force(rho, velocity):

    area = math.pi * (DIAMETER/2)**2

    return (
        0.5 *
        rho *
        CD *
        area *
        velocity**2
    )



# =========================
# 거리 계산
# =========================

def calculate_range(angle, mass, temp, pressure, humidity):

    dt = 0.01


    theta = math.radians(angle)


    vx = V0 * math.cos(theta)
    vy = V0 * math.sin(theta)


    x = 0
    y = 0


    rho = air_density(
        temp,
        pressure,
        humidity
    )


    while y >= 0:


        v = math.sqrt(
            vx**2 + vy**2
        )


        if v == 0:
            break


        F = drag_force(
            rho,
            v
        )


        ax = -(F/mass)*(vx/v)

        ay = (
            -g
            -(F/mass)*(vy/v)
        )


        vx += ax*dt
        vy += ay*dt


        x += vx*dt
        y += vy*dt


    return x



# =========================
# 목표거리 → 각도
# =========================

def find_angle(target, mass, temp, pressure, humidity):


    best_angle = 0
    best_error = float("inf")


    angle = 0


    while angle <= 90:


        distance = calculate_range(
            angle,
            mass,
            temp,
            pressure,
            humidity
        )


        error = abs(
            distance - target
        )


        if error < best_error:

            best_error = error
            best_angle = angle


        angle += 0.1


    return best_angle



# =========================
# GUI 동작
# =========================


def run_calculation():

    try:

        mass = float(mass_entry.get())
        temp = float(temp_entry.get())
        pressure = float(pressure_entry.get())
        humidity = float(humidity_entry.get())
        value = float(value_entry.get())


        if mode.get() == "angle":


            result = calculate_range(
                value,
                mass,
                temp,
                pressure,
                humidity
            )


            result_text.config(
                text=
                f"수평 도달거리\n{result:.2f} m"
            )


        else:


            result = find_angle(
                value,
                mass,
                temp,
                pressure,
                humidity
            )


            result_text.config(
                text=
                f"필요한 각도\n{result:.1f}°"
            )


    except:

        messagebox.showerror(
            "입력 오류",
            "모든 칸에 숫자를 입력하세요."
        )



def change_label():

    if mode.get() == "angle":

        value_label.config(
            text="초기 각도(도)"
        )

    else:

        value_label.config(
            text="목표 거리(m)"
        )



# =========================
# 창 생성
# =========================

window = tk.Tk()

window.title(
    "공기저항 투사체 시뮬레이터"
)

window.geometry(
    "420x520"
)


title = tk.Label(
    window,
    text="공기저항 투사체 계산기",
    font=("Arial",16)
)

title.pack(pady=10)



mode = tk.StringVar()

mode.set("angle")



tk.Radiobutton(
    window,
    text="각도 → 거리",
    variable=mode,
    value="angle",
    command=change_label
).pack()


tk.Radiobutton(
    window,
    text="거리 → 각도",
    variable=mode,
    value="distance",
    command=change_label
).pack()



def make_entry(text):

    tk.Label(
        window,
        text=text
    ).pack()

    entry = tk.Entry(window)

    entry.pack()

    return entry



mass_entry = make_entry(
    "질량(kg)"
)

temp_entry = make_entry(
    "기온(℃)"
)

pressure_entry = make_entry(
    "기압(hPa)"
)

humidity_entry = make_entry(
    "습도(%)"
)



value_label = tk.Label(
    window,
    text="초기 각도(도)"
)

value_label.pack()


value_entry = tk.Entry(window)

value_entry.pack()



tk.Button(
    window,
    text="계산하기",
    command=run_calculation,
    width=15
).pack(pady=20)



result_text = tk.Label(
    window,
    text="결과 대기중",
    font=("Arial",14)
)

result_text.pack()



window.mainloop()
