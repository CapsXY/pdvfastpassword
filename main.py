import datetime
import os
import sys
import threading
import tkinter as tk

import pyperclip
import pystray
from PIL import Image, ImageDraw, ImageFont


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def convert_number(num_str: str) -> str:
    table = "@ABCDEFGHI"
    return "".join([table[int(ch)] for ch in num_str])


def generate_syncplus(dt: datetime.datetime) -> str:
    ano = dt.strftime("%y")
    mes = dt.strftime("%m")
    dia = dt.strftime("%d")
    hora = dt.strftime("%I")
    return convert_number(ano) + convert_number(mes) + convert_number(dia) + convert_number(hora)


def generate_etiqueta(dt: datetime.datetime) -> str:
    mes = dt.strftime("%m")
    dia = dt.strftime("%d")
    hora = dt.strftime("%H")
    return convert_number(mes) + convert_number(dia) + convert_number(hora)


class App:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()

        threading.Thread(target=self.start_tray, daemon=True).start()

    def start_tray(self):
        # Carrega logo
        icon_path = resource_path(os.path.join("img", "logo.png"))

        try:
            image = Image.open(icon_path)
        except Exception:
            image = Image.new("RGB", (64, 64), "black")
            d = ImageDraw.Draw(image)

            try:
                font = ImageFont.truetype("arial.ttf", 18)
            except:
                font = ImageFont.load_default()

            text = "PDV"
            bbox = d.textbbox((0, 0), text, font=font)
            text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            pos = ((64 - text_w) // 2, (64 - text_h) // 2)
            d.text(pos, text, font=font, fill="white")

        def copy_syncplus(icon, item):
            password = generate_syncplus(datetime.datetime.now())
            pyperclip.copy(password)

        def copy_etiqueta(icon, item):
            password = generate_etiqueta(datetime.datetime.now())
            pyperclip.copy(password)

        def quit_app(icon, item):
            icon.stop()
            self.root.quit()

        menu = (
            pystray.MenuItem("Sync Plus", copy_syncplus),
            pystray.MenuItem("Etiqueta", copy_etiqueta),
            pystray.MenuItem("Sair", quit_app),
        )

        icon = pystray.Icon("senha_app", image, "Gerador de Senha", menu)
        icon.run()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
