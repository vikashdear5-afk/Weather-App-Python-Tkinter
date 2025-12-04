# 🌦️ Weather App (Python + Tkinter)

A modern **GUI Weather Application** built using **Python**, **Tkinter**, and the **OpenWeather API**.
Designed with a **purple modern UI**, **smooth layout**, **custom icons**, and **error handling**.
This project is perfect for showcasing Python GUI development skills in your **portfolio** or **job applications**.

---

## 🚀 Features

* ✔ **Beautiful Purple UI Theme**
* ✔ **Search weather by city**
* ✔ **Live temperature, humidity, wind speed**
* ✔ **Weather condition icons** (sun, rain, clouds, etc.)
* ✔ **API integration (OpenWeather)**
* ✔ **Error handling** (invalid city, no internet)
* ✔ **Responsive layout**
* ✔ **EXE support using PyInstaller**
* ✔ **Clean, readable, job-ready code**

---

## 🖼️ Screenshots

(Add your screenshot here)

```
assets/
└── screenshot.png
```

---

## 📦 Project Structure

```
WeatherApp/
│
├── weather_app.py
├── assets/
│   ├── app_icon.ico
│   ├── clear.png
│   ├── rain.png
│   ├── cloudy.png
│   ├── search.png
│   └── ...more icons
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔧 Requirements

Install dependencies:

```
pip install -r requirements.txt
```

**requirements.txt**

```
requests
Pillow
```

---

## 🔑 Setup OpenWeather API Key

1. Create a free account at:
   [https://openweathermap.org/api](https://openweathermap.org/api)
2. Generate an API key
3. Add your API key inside `weather_app.py`:

```python
API_KEY = "YOUR_API_KEY"
```

---

## ▶️ Run the Application

```
python weather_app.py
```

---

## 🖥️ Build EXE (Windows)

Use:

```
pyinstaller --onefile --windowed --icon=assets/app_icon.ico weather_app.py
```

Your EXE will be in:

```
dist/weather_app.exe
```

---

## 🧩 Technologies Used

* **Python 3.x**
* **Tkinter**
* **Requests**
* **Pillow (PIL)**
* **OpenWeather API**

---

## 📚 What You Will Learn

* GUI programming with Tkinter
* API data fetching
* Error handling
* Using custom icons in Tkinter
* Creating professional desktop apps
* Building EXE using PyInstaller
* Project structuring for GitHub

---

## 🤝 Contributing

Feel free to fork this repository and submit pull requests!

---

## 📜 License

This project is open-source and free to use.

---

## ⭐ Support

If you like this project, please **⭐ star the repository**.
Your support motivates me to build more awesome projects!
