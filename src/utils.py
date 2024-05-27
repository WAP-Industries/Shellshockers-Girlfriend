import tkinter as tk
import os
from PIL import Image, ImageTk
import chromadb


class Utils:
    Root = os.path.dirname(os.path.abspath(__file__))
    Client = chromadb.Client(
        settings=chromadb.Settings(
            is_persistent=True, 
            persist_directory=f"{Root}\\memory",
        )
    )

    @staticmethod
    def RemoveVoice():
        from girlfriend import Girlfriend
        
        if os.path.exists(Girlfriend.VoiceFile):
            try:
                os.remove(Girlfriend.VoiceFile)
            except Exception as e:
                Girlfriend.Error("remove voice file", e)
    
    @staticmethod
    def LoadSprite(src: str, x: int, y: int, width: int, height: int) -> None:
        from girlfriend import Girlfriend

        image = ImageTk.PhotoImage(Image.open(f"assets\\{src}").resize((width, height)))
        Girlfriend.Sprites.append(image)
        Girlfriend.Window.Canvas.create_image(x, y, image=image, anchor=tk.NW)

    @staticmethod
    def RemoveSprite() -> None:
        from girlfriend import Girlfriend
        Girlfriend.Sprites[-1].__del__()
        Girlfriend.Sprites.pop()

    class CustomWindow(tk.Tk):
        def __init__(self, width, height):
            super().__init__()
            
            transcolor = "grey"
            self.overrideredirect(1)
            self.attributes("-transparentcolor", transcolor)
            self.attributes("-topmost", True)
            self.geometry(f"{width}x{height}")

            self.Canvas = tk.Canvas(self, bg=transcolor, borderwidth=0, highlightthickness=0)
            self.Canvas.pack(fill=tk.BOTH, expand=True)
            self.Canvas.bind('<ButtonPress-1>', self.StartMove)
            self.Canvas.bind('<B1-Motion>', self.MoveWindow)
            
        def StartMove(self, event) -> None:
            self.startx = event.x_root
            self.starty = event.y_root

        def MoveWindow(self, event) -> None:
            deltax = event.x_root - self.startx
            deltay = event.y_root - self.starty
            x = self.winfo_x() + deltax
            y = self.winfo_y() + deltay
            self.geometry(f'+{x}+{y}')
            self.startx = event.x_root
            self.starty = event.y_root