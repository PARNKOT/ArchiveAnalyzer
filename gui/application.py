import os
import logging
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from typing import List
from threading import Event
from gui.image_container import ImageContainer


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Logger
        self.logger = logging.getLogger("Gui")

        # Events
        self.dir_changed_event = Event()
        self.next_button_pressed_event = Event()

        self.title("Vidar archive analyzer")
        self.geometry("850x850")
        self.minsize(850, 850)

        # Frames
        self.frame_file_chooser = tk.Frame(self, bg="white")
        self.frame_next = tk.Frame(self, bg="white")
        self.frame_images = tk.Frame(self, bg="white")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=7)

        self.frame_file_chooser.grid(column=0, row=0, sticky="nswe")
        self.frame_next.grid(column=0, row=1, sticky="nswe")
        self.frame_images.grid(column=0, row=2, sticky="nswe")

        # Variables
        self.directory_to_analyze = tk.StringVar()

        # Frame file chooser
        self.button_ask_file = tk.Button(self.frame_file_chooser,
                                         text="Choose directory",
                                         command=self.choose_directory, bg="#cccecf", font=12)
        self.label_directory = tk.Label(self.frame_file_chooser, textvariable=self.directory_to_analyze,
                                        width=55, wraplength=550.0, bg="#cccecf")

        self.button_ask_file.pack(side="left", padx=20, pady=5)
        self.label_directory.pack(side="left", pady=5, expand=True)

        # Frame next
        self.button_next = tk.Button(self.frame_next, text="Next", bg="#007FFF", fg="white",
                                     font=12, command=self.next_button_clicked)
        self.button_next.pack(fill=tk.X)

        # Frame images
        for i in range(3):
            self.frame_images.columnconfigure(i, weight=1)
            self.frame_images.rowconfigure(i, weight=1)

        self.image_containers = [ImageContainer(self.frame_images) for _ in range(9)]

    def load_images(self, dirs: List[str]):
        for i, dir_ in enumerate(dirs):
            optical_classes_dir = os.path.join(self.directory_to_analyze.get(), dir_, "optical-classes")
            img_file = f"{os.path.join(optical_classes_dir, os.listdir(optical_classes_dir)[0])}/01.jpg"

            if not os.path.exists(img_file):
                img_file = img_file.replace("01.jpg", "01_primary.jpg")

            self.logger.debug("Load image: {0}", img_file)

            self.image_containers[i].img_path = img_file

            img = Image.open(img_file).resize((280, 180), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image=img)
            self.image_containers[i].set_background_image(img)
            self.image_containers[i].grid(row=i//3, column=i%3)

    def set_atomic_class_labels(self, labels: List[str]):
        for i, label in enumerate(labels):
            self.image_containers[i].atomic_class.set(label)
            self.image_containers[i].true_atomic_class.set(label)

    def choose_directory(self):
        self.directory_to_analyze.set(fd.askdirectory(title="Choose a directory",
                                                      initialdir=os.curdir))
        self.dir_changed_event.set()
        self.logger.info("Directory changed: {0}", self.directory_to_analyze.get())

    def next_button_clicked(self):
        self.next_button_pressed_event.set()
        self.logger.debug("Next button pressed")


def run_app():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    run_app()
