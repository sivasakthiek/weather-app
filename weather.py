from tkinter import *
import requests
import tkinter.messagebox
import emoji
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from geopy.geocoders import Nominatim
import json


base = Tk()
base.title("Group 6 Weather App")
base.geometry("400x600")
base.configure(bg="#2F4F4F")


weather_emojis = {
    'clear sky': '☀️',
    'few clouds': '🌤️',
    'scattered clouds': '🌥️',
    'broken clouds': '☁️',
    'shower rain': '🌧️',
    'rain': '🌦️',
    'thunderstorm': '⛈️',
    'snow': '❄️',
    'mist': '🌫️',
}

def update_background(weather_condition):
    if 'clear' in weather_condition:
        base.configure(bg="#FFD700")
    elif 'cloud' in weather_condition:
        base.configure(bg="#A9A9A9")
    elif 'rain' in weather_condition:
        base.configure(bg="#4682B4")
    elif 'thunderstorm' in weather_condition:
        base.configure(bg="#2F4F4F")
    elif 'snow' in weather_condition:
        base.configure(bg="#FFFFFF")
    else:
        base.configure(bg="#87CEFA")

def weather_response_format(weather):
    try:
        name = weather['name']
        desc = weather['weather'][0]['description']
        temp = int(weather['main']['temp'] - 273)
        humidity = weather['main']['humidity']
        rain_possibility = weather['rain']['1h'] if 'rain' in weather else 0
        emoji_icon = weather_emojis.get(desc, '')

        display_str = f'''
City: {name}
Conditions: {desc} {emoji_icon}
Temperature (°C): {temp}
Humidity: {humidity}%
Rain Possibility (1hr): {rain_possibility}mm
'''
        update_background(desc)
    except:
        display_str = '''Sorry! The city could not be found, Please try again!'''
    return display_str

def get_weather(city):
    weather_key = '14ed2a78adcbcbfe1ac9d1ffb8c5eea6'  
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': weather_key, 'q': city}
    weather_response = requests.get(url, params=params)
    weather = weather_response.json()

    label['text'] = weather_response_format(weather)

def get_default_city_weather():
    try:
        ip_request = requests.get('https://ipinfo.io/')
        location_data = json.loads(ip_request.text)
        city = location_data['city']
        get_weather(city)
    except:
        tkinter.messagebox.showerror("Error", "Could not fetch the default city")

def close_app():
    closeapp = tkinter.messagebox.askyesno("Group 6 Weather App", "Do you want to exit App?")
    if closeapp > 0:
        base.destroy()

def credits_func():
    tkinter.messagebox.showinfo(
        title="Credits",
        message='''Made with love by Group 6 CIT TIV
***Mohammed
***Alvin
***Hassan
***Moses
***Francis
GPL V4 License 2021'''
    )

title_label = Label(base, text="Weather App", font=("Arial", 18, "bold"), bg="#2F4F4F", fg="white")
title_label.pack(pady=10)

frame = Frame(base, bg="#1E1E1E", bd=5)
frame.pack(fill="both", padx=10, pady=5)

entry = Entry(frame, font=('Courier', 12), justify="center")
entry.pack(fill="x", padx=5, pady=5)

button = Button(frame, text="Get Weather", command=lambda: get_weather(entry.get()), font=("Arial", 12), bg="#4682B4", fg="white")
button.pack(pady=5)

default_button = Button(base, text="Show My City's Weather", font=("Arial", 12), command=get_default_city_weather, bg="#4682B4", fg="white")
default_button.pack(pady=10)

label_frame = Frame(base, bg="white", bd=5)
label_frame.pack(fill="both", expand=True, padx=10, pady=5)

label = Label(label_frame, font=('Courier', 14), bg="white", anchor="nw", justify="left")
label.pack(fill="both", expand=True)

menubar = Menu(base)
base.configure(menu=menubar)
submenu1 = Menu(menubar, tearoff=0)
submenu2 = Menu(menubar, tearoff=0)

menubar.add_cascade(label="File", menu=submenu1)
menubar.add_cascade(label="Help", menu=submenu2)

submenu1.add_command(label="Exit", command=close_app)
submenu2.add_command(label="About", command=credits_func)

base.mainloop()
