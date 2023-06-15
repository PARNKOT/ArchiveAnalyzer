import os
import logging
from typing import List
from threading import Thread, Event

from statistics import Statistics, Detection, localize
from gui.application import Application

logger = logging.getLogger("Main")

statistics = Statistics()
application = Application()
app_running_event = Event()


def parse_description_file(path: str):
    global statistics

    optical_classes_dir = os.path.join(path, "optical-classes")
    description_file = f"{os.path.join(optical_classes_dir, os.listdir(optical_classes_dir)[0])}/description.txt"

    with open(description_file, "r") as f:
        detection = Detection()
        for line in f.readlines():
            if "Udrm:" in line:
                detection.udrm = line.split(":")[1].strip(" \n")
            elif "Class:" in line:
                detection.atomic_class = localize(line.split(":")[1].strip(" \n").split(",")[0])
            elif "Confidence:" in line:
                detection.confidence = line.split(":")[1].strip(" \n")
            elif "Neural network:" in line:
                detection.nn = line.split(":")[1].strip(" \n")

    return detection


def update_statistics(detections: List[Detection]):
    for i, detection in enumerate(detections):
        if detection.atomic_class.lower() != application.image_containers[i].true_atomic_class.get().lower():
            detection.is_right = False
        detection.atomic_class = application.image_containers[i].true_atomic_class.get()
        statistics.update(detection)


def worker():
    while app_running_event.is_set():
        application.dir_changed_event.wait()
        root = application.directory_to_analyze.get()
        logger.info(f"Directory changed to: {root}")
        dirs = os.listdir(root)

        for i in range(0, len(dirs), 9):
            logger.info("Loading images")
            dirs_package = dirs[i:i+9]
            application.load_images(dirs_package)

            detections = [parse_description_file(os.path.join(root, dir_)) for dir_ in dirs_package]
            labels = [detection.atomic_class for detection in detections]

            application.set_atomic_class_labels(labels)

            application.next_button_pressed_event.clear()
            logger.info("Waiting next button to click")
            application.next_button_pressed_event.wait()

            logger.info("Updating statistics")
            update_statistics(detections)

        logger.info("Saving statistics to file {0}", root)
        statistics.save(root)

        application.dir_changed_event.clear()


if __name__ == '__main__':
    app_running_event.set()

    worker_thread = Thread(target=worker, name="WorkerThread", daemon=True)
    worker_thread.start()

    application.mainloop()
    app_running_event.clear()

