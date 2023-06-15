import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

from variables import ATOMIC_CLASSES


class ImageContainer(tk.Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, padx=5, pady=5, bg="white", **kwargs)

        self.atomic_class = tk.StringVar(value="Коптер")
        self.true_atomic_class = tk.StringVar(value="Коптер")
        self.img_path = ""

        self.label_image = tk.Label(self, textvariable=self.atomic_class,
                                    compound="bottom",
                                    font=("Helvetica", 12),
                                    pady=5, bg="white") # #f2f2f2
        self.button_yes = tk.Button(self, text="Да")
        self.button_no = tk.Button(self, text="Нет")

        self.combobox = ttk.Combobox(self, textvariable=self.true_atomic_class,
                                     values=ATOMIC_CLASSES)

        self.label_image.pack(fill=tk.X)
        self.combobox.pack(fill=tk.X)

        self.label_image.bind("<Button-1>", self.show_image)

    def set_background_image(self, img: tk.PhotoImage):
        self.label_image.configure(image=img)
        self.label_image.image = img

    def show_image(self, event):
        if self.img_path != "":
            Image.open(self.img_path).show()


if __name__ == "__main__":
    app = tk.Tk()

    frame = ImageContainer(app)
    img = Image.open("../images/01_primary.jpg")
    img = ImageTk.PhotoImage(image=img)
    frame.set_background_image(img)
    frame.pack()

    app.mainloop()
