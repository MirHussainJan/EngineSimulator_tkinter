import tkinter as tk
import math

root = tk.Tk()
root.title("Engine Simulator")
root.configure(bg="#2C3E50")

digital_speed = tk.Label(root, font=("Arial", 20), bg="#2C3E50", fg="#ECF0F1")
digital_speed.grid(row=0, column=0, pady=10)

my_throttle = tk.Scale(root, from_=100, to=0, orient="vertical", length=300, command=lambda val: on_press(int(val)), bg="#34495E", fg="#ECF0F1", highlightthickness=0)
my_throttle.grid(row=1, column=1, padx=20, pady=10, rowspan=2)

state_frame = tk.Frame(root, bg="#2C3E50")
state_frame.grid(row=2, column=0, columnspan=4, pady=10)

state_Starting = tk.Label(state_frame, font=("Arial", 14), text="STARTING", bg="#2C3E50", fg="#ECF0F1")
state_Starting.grid(row=0, column=0, padx=10)

state_ON = tk.Label(state_frame, font=("Arial", 14), text="ON", bg="#2C3E50", fg="#ECF0F1")
state_ON.grid(row=0, column=1, padx=10)

state_Running = tk.Label(state_frame, font=("Arial", 14), text="RUNNING", bg="#2C3E50", fg="#ECF0F1")
state_Running.grid(row=0, column=2, padx=10)

state_OFF = tk.Label(state_frame, font=("Arial", 14), text="OFF", bg="#2C3E50", fg="#ECF0F1")
state_OFF.grid(row=0, column=4, padx=10)

state_Cooling = tk.Label(state_frame, font=("Arial", 14), text="COOLING", bg="#2C3E50", fg="#ECF0F1")
state_Cooling.grid(row=0, column=3, padx=10)

digital_temp = tk.Label(root, font=("Arial", 20), bg="#2C3E50", fg="#ECF0F1")
digital_temp.grid(row=0, column=2, columnspan=3, pady=10)

speedometer = tk.Canvas(root, width=400, height=400, bg="#34495E", highlightthickness=0)
speedometer.grid(row=1, column=0, padx=20, pady=10)

tempmeter = tk.Canvas(root, width=400, height=400, bg="#34495E", highlightthickness=0)
tempmeter.grid(row=1, column=2, padx=20, pady=10)

speed_value = 0
temperature_value = 0
system_state = "OFF"

def draw_speedometer():
    speedometer.create_arc(50, 50, 350, 350, start=0, extent=180, style=tk.ARC, width=2, outline="#BDC3C7")
    for i in range(0, 101, 4):
        angle = 180 + (i * 1.8)
        x = 200 + 160 * math.cos(math.radians(angle))
        y = 200 + 160 * math.sin(math.radians(angle))
        if i % 10 == 0:
            speedometer.create_text(x, y, text=str(i), font=("Arial", 12), fill="#ECF0F1")
        else:
            x1 = 200 + 155 * math.cos(math.radians(angle))
            y1 = 200 + 155 * math.sin(math.radians(angle))
            speedometer.create_line(x1, y1, x, y, fill="#95A5A6", width=0.5)

def draw_tempmeter():
    tempmeter.create_arc(50, 50, 350, 350, start=0, extent=180, style=tk.ARC, width=2, outline="#BDC3C7")
    
    for i in range(0, 1001, 50):
        angle = 180 + (i * 0.18)  # Adjusted for range up to 1000
        x = 200 + 160 * math.cos(math.radians(angle))
        y = 200 + 160 * math.sin(math.radians(angle))
        
        if i <= 250:
            color = "lightblue"
        elif i <= 350:
            color = "#FFA07A"
        elif i <= 500:
            color = "#FF8C00"
        elif i <= 750:
            color = "#FF4500"
        else:
            color = "#FF0000"
        
        if i % 100 == 0:
            tempmeter.create_text(x, y, text=str(i), font=("Arial", 12), fill=color)
        else:
            x1 = 200 + 155 * math.cos(math.radians(angle))
            y1 = 200 + 155 * math.sin(math.radians(angle))
            tempmeter.create_line(x1, y1, x, y, fill="#95A5A6", width=0.5)

def speed_needle(value):
    angle = 180 + (value * 1.8)
    x = 200 + 120 * math.cos(math.radians(angle))
    y = 200 + 120 * math.sin(math.radians(angle))
    speedometer.delete("needle")
    speedometer.create_line(200, 180, x, y, fill="green", width=2, tag="needle")
    digital_speed.config(text=f'Speed: {value} km/h')
    global speed_value
    speed_value = value

def temp_needle(value):
    angle = 180 + (value * 1.8)
    x = 200 + 120 * math.cos(math.radians(angle))
    y = 200 + 120 * math.sin(math.radians(angle))
    tempmeter.delete("needle")
    
    global temp_value
    temp_value = value * 10

    if temp_value <= 250:
        color = "lightblue"
    elif temp_value <= 450:
        color = "#FFA07A"  # Light Salmon
    elif temp_value <= 600:
        color = "#FF8C00"  # Dark Orange
    elif temp_value <= 850:
        color = "#FF4500"  # Orange Red
    else:
        color = "#FF0000"  # Red

    digital_temp.config(text=f'🔥: {temp_value} °C', fg=color)
    tempmeter.create_line(200, 200, x, y, fill=color, width=2, tag="needle")

def set_state(state):
    global system_state
    system_state = state
    state_Starting.config(bg="#2C3E50")
    state_ON.config(bg="#2C3E50")
    state_Running.config(bg="#2C3E50")
    state_OFF.config(bg="#2C3E50")
    state_Cooling.config(bg="#2C3E50")
    if state == "Starting":
        state_Starting.config(bg="#3498DB")
    elif state == "ON":
        state_ON.config(bg="#3498DB")
        my_throttle.config(state=tk.NORMAL)
        my_throttle.set(0)
    elif state == "Running":
        state_Running.config(bg="#3498DB")
    elif state == "Cooling":
        state_Cooling.config(bg="#3498DB")
    elif state == "OFF":
        state_OFF.config(bg="#3498DB")
        
count = 0

def on_press(value):
    global count
    if(value == 100):
        count=count+1
    if(value == 0):
        count=count+1
    if(count==3):
        set_state("Starting")
        my_throttle.config(state="disabled")
        root.after(1000, lambda: set_state("ON"))
    elif(count>3):
        speed_needle(value)

def off_press():
    global count
    set_state("OFF")
    my_throttle.set(0)
    count = 0
    speed_needle(0)

off_button = tk.Button(root, text="OFF", command=off_press, bg="#E74C3C", fg="#ECF0F1", font=("Arial", 14))
off_button.grid(row=3, column=2, pady=10)

def update_temperature():
    global temperature_value
    if speed_value > 0:
            temperature_value += (speed_value / 100) * 0.2
            if temperature_value > 100:
                temperature_value = 100
    else:
            temperature_value -= 0.2
            if temperature_value < 0:
                temperature_value = 0
    temp_needle(int(temperature_value))
    if speed_value > 0:
            set_state("Running")
    elif system_state == "Running" and speed_value == 0 and temp_value==0:
        set_state("ON")
    elif system_state == "Cooling" and speed_value == 0 and temp_value==0:
        set_state("ON")
    elif system_state == "Running" and speed_value == 0 and temp_value!=0:
        set_state("Cooling")
    root.after(100, update_temperature)

draw_speedometer()
draw_tempmeter()
speed_needle(0)
temp_needle(0)
set_state("OFF")

update_temperature()

root.mainloop()