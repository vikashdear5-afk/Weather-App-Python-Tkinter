"""
Professional Weather App - Single file (no external images)
Style A — Purple Modern (Gradient + Glass card + Rounded button)

Replace API_KEY with your OpenWeatherMap API key.
Dependencies: requests, Pillow
"""

import io
import math
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageFont

BG_COLOR = "#3F1D7A"   # purple background
FG_COLOR = "white"
CARD_COLOR = "#5A2EA6"
BUTTON_COLOR = "#7A42F4"
FONT_FAMILY = "Segoe UI"


# ---------- CONFIG ----------
API_KEY = "API-KEY HERE PASTE"  # <<< Replace with your OpenWeatherMap API key
WIDTH, HEIGHT = 430, 650
FONT_FAMILY = "Segoe UI"  # will fall back if not present

# Color palette for Style A (Purple Modern)
COLORS = {
    "bg1": (62, 30, 104),   # deep purple
    "bg2": (90, 44, 141),   # softer purple
    "card": (255, 255, 255, 45),  # semi-transparent white for glass
    "card_solid": (95, 62, 160),  # card accent
    "btn": (122, 90, 245),
    "white": (255, 255, 255),
    "muted": (220, 215, 235)
}

# ---------- Utility: Create gradient background image ----------
def create_gradient_bg(w=WIDTH, h=HEIGHT, c1=COLORS["bg1"], c2=COLORS["bg2"]):
    """Create a vertical gradient PIL image (RGB)."""
    img = Image.new("RGB", (w, h), c1)
    top = Image.new("RGB", (w, 1), c1)
    bottom = Image.new("RGB", (w, 1), c2)
    for y in range(h):
        ratio = y / (h - 1)
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        Image.new("RGB", (w, 1), (r, g, b)).paste(img, (0, y))
        img.putpixel((0, y), (r, g, b))
    # faster correct approach:
    pixels = img.load()
    for y in range(h):
        ratio = y / (h - 1)
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        for x in range(w):
            pixels[x, y] = (r, g, b)
    return img

# ---------- Utility: Draw rounded rectangle on a PIL image ----------
def rounded_rectangle(draw, xy, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

# ---------- Utility: Create glass card (semi-transparent) ----------
def create_glass_card(w=340, h=320, radius=24):
    # Create RGBA card image with blur and semi-transparent white
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    fill = (255, 255, 255, 40)  # low alpha to give glass effect
    rounded_rectangle(d, (0, 0, w - 1, h - 1), radius, fill=fill)
    # subtle inner highlight
    overlay = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle((6, 6, w - 6, h - 6), radius - 6, fill=(255, 255, 255, 12))
    card = Image.alpha_composite(card, overlay)
    card = card.filter(ImageFilter.GaussianBlur(0.6))
    return card

# ---------- Utility: Create a small app icon programmatically ----------
def create_app_icon(size=64):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Outer rounded circle
    outer = (0, 0, size, size)
    d.ellipse(outer, fill=(120, 85, 245, 255))
    # inner stylized sun/cloud glyph
    # sun circle
    s = int(size * 0.38)
    cx, cy = size // 2 - 6, size // 2 - 4
    d.ellipse((cx - s//2, cy - s//2, cx + s//2, cy + s//2), fill=(255, 205, 0, 255))
    # cloud
    cw = int(size * 0.9)
    ch = int(size * 0.45)
    cloud = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cloud)
    cd.ellipse((size*0.18, size*0.48, size*0.48, size*0.72), fill=(255,255,255,255))
    cd.ellipse((size*0.35, size*0.36, size*0.65, size*0.66), fill=(255,255,255,255))
    cd.ellipse((size*0.52, size*0.48, size*0.82, size*0.72), fill=(255,255,255,255))
    cd.rectangle((size*0.18, size*0.58, size*0.82, size*0.74), fill=(255,255,255,255))
    cloud = cloud.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.alpha_composite(img, cloud)
    # soft highlight
    highlight = Image.new("RGBA", (size, size), (255,255,255,0))
    hd = ImageDraw.Draw(highlight)
    hd.ellipse((size*0.05, size*0.05, size*0.45, size*0.45), fill=(255,255,255,50))
    img = Image.alpha_composite(img, highlight)
    return img

# ---------- Main App ----------
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather — Purple Modern")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)

        # Create background image dynamically
        self.bg_image_pil = create_gradient_bg(WIDTH, HEIGHT)
        # add soft abstract shapes for texture
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
        od = ImageDraw.Draw(overlay)
        # big soft orb
        od.ellipse((-120, -80, 420, 540), fill=(255,255,255,12))
        od.ellipse((120, -120, 620, 420), fill=(255,255,255,6))
        overlay = overlay.filter(ImageFilter.GaussianBlur(24))
        self.bg_image_pil = Image.alpha_composite(self.bg_image_pil.convert("RGBA"), overlay)

        self.bg_image = ImageTk.PhotoImage(self.bg_image_pil)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Create and set app icon
        self.app_icon_pil = create_app_icon(64)
        self.app_icon = ImageTk.PhotoImage(self.app_icon_pil)
        try:
            root.iconphoto(False, self.app_icon)
        except Exception:
            pass

        # Build UI elements on canvas for flexible positioning
        self.build_ui()

    def build_ui(self):
        # Title text
        self.canvas.create_text(WIDTH//2, 40, text="🌤 Weather", font=(FONT_FAMILY, 24, "bold"),
                                fill="white")

        # Search box background (rounded)
        entry_w = 320
        entry_h = 54
        ex = (WIDTH - entry_w) // 2
        ey = 90
        # create rounded rectangle using PIL and put as image so it looks smooth
        r = 12
        entry_img = Image.new("RGBA", (entry_w, entry_h), (0,0,0,0))
        ed = ImageDraw.Draw(entry_img)
        ed.rounded_rectangle((0, 0, entry_w, entry_h), radius=r, fill=(255,255,255,255))
        entry_img = entry_img.filter(ImageFilter.GaussianBlur(0.3))
        entry_tk = ImageTk.PhotoImage(entry_img)
        self.canvas.create_image(ex, ey, anchor="nw", image=entry_tk)
        self._entry_bg = entry_tk  # hold reference

        # Actual Entry (placed over the image)
        self.city_entry = tk.Entry(self.root, justify="center", bd=0, font=(FONT_FAMILY, 14))
        self.city_entry.place(x=ex+10, y=ey+10, width=entry_w-110, height=entry_h-20)
        self.city_entry.insert(0, "Enter city (e.g. Delhi)")

        # Button (rounded) - we create image for it for a rounded pill effect
        btn_w, btn_h = 120, 44
        btn_x = ex + entry_w - btn_w - 12
        btn_y = ey + 5
        btn_img = Image.new("RGBA", (btn_w, btn_h), (0,0,0,0))
        bd = ImageDraw.Draw(btn_img)
        bd.rounded_rectangle((0,0,btn_w,btn_h), radius=22, fill=COLORS["btn"])
        btn_img = btn_img.filter(ImageFilter.GaussianBlur(0.2))
        btn_tk = ImageTk.PhotoImage(btn_img)
        self.canvas.create_image(btn_x, btn_y, anchor="nw", image=btn_tk)
        self._btn_img = btn_tk

        # Button text (clickable)
        btn_label = tk.Label(self.root, text="Get Weather", bg="#7A5AF5", fg="white",
                     font=(FONT_FAMILY, 11, "bold"))

        btn_label.place(x=btn_x, y=btn_y+8, width=btn_w, height=btn_h-8)
        btn_label.bind("<Button-1>", lambda e: self.get_weather())

        # Glass card (center)
        card_w, card_h = 360, 380
        card_x = (WIDTH - card_w) // 2
        card_y = 170
        card_pil = create_glass_card(card_w, card_h, radius=26)
        card_tk = ImageTk.PhotoImage(card_pil)
        self.canvas.create_image(card_x, card_y, anchor="nw", image=card_tk)
        self._card_img = card_tk

        # Place weather icon placeholder
        self.icon_label = tk.Label(self.root, bg=BG_COLOR, bd=0, highlightthickness=0)


  # transparent-like color

        self.icon_label.place(x=card_x + 20, y=card_y + 20, width=120, height=120)

        # Info text area inside card
        self.info_text = tk.Text(self.root, bg=BG_COLOR, bd=0, highlightthickness=0,
                         font=(FONT_FAMILY, 13), fg="white")

        self.info_text.place(x=card_x + 160, y=card_y + 30, width=card_w - 180, height=220)
        self.info_text.insert("1.0", "Enter a city and click 'Get Weather' to fetch the forecast.")
        self.info_text.configure(state="disabled")

        # Footer small hints
        self.canvas.create_text(WIDTH//2, card_y + card_h + 22,
                                text="Powered by OpenWeatherMap • Job-ready Tkinter UI",
                                font=(FONT_FAMILY, 9), fill="#EDEBFF")

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city or city.lower().startswith("enter city"):
            messagebox.showwarning("Input required", "Please type a city name.")
            return

        # Build API call
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            resp = requests.get(url, timeout=10)
            data = resp.json()
            if resp.status_code != 200:
                msg = data.get("message", "Could not get weather.")
                messagebox.showerror("API Error", msg.title())
                return

            # parse
            name = data.get("name", city.title())
            country = data.get("sys", {}).get("country", "")
            temp = data["main"]["temp"]
            feels = data["main"].get("feels_like", temp)
            humidity = data["main"]["humidity"]
            wind = data.get("wind", {}).get("speed", 0)
            desc = data["weather"][0]["description"].title()
            icon_code = data["weather"][0]["icon"]

            # Update text info
            info_lines = [
                f"{name}, {country}",
                "",
                f"🌡 Temperature: {temp:.1f} °C",
                f"🤍 Feels like: {feels:.1f} °C",
                f"🌥 Condition: {desc}",
                f"💧 Humidity: {humidity}%",
                f"💨 Wind: {wind} m/s",
            ]
            self.info_text.configure(state="normal")
            self.info_text.delete("1.0", "end")
            self.info_text.insert("1.0", "\n".join(info_lines))
            self.info_text.configure(state="disabled")

            # Fetch weather icon from OpenWeather (small png)
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_resp = requests.get(icon_url, timeout=8)
            icon_img = Image.open(io.BytesIO(icon_resp.content)).convert("RGBA")
            icon_img = icon_img.resize((120, 120), Image.LANCZOS)

            # subtle circle background behind icon
            bg = Image.new("RGBA", (120, 120), (0,0,0,0))
            d = ImageDraw.Draw(bg)
            d.ellipse((0,0,120,120), fill=(255,255,255,20))
            bg = Image.alpha_composite(bg, icon_img)
            tk_icon = ImageTk.PhotoImage(bg)
            self.icon_label.configure(image=tk_icon)
            self.icon_label.image = tk_icon

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Network problem: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load weather: {e}")

# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
