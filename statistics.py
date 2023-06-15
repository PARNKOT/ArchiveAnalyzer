from threading import Lock
from dataclasses import dataclass


def localize(atomic_class: str):
    if atomic_class.lower() == "uavcopter":
        return "Коптер"
    elif atomic_class.lower() == "bird":
        return "Птица"
    elif atomic_class.lower() in ["uavplane", "civilplane", "militaryplane"]:
        return "Самолет"
    elif atomic_class.lower() == "unknown":
        return "Неизвестно"

    raise ValueError(f"Cannot translate {atomic_class}")


@dataclass
class Detection:
    udrm = ""
    atomic_class = ""
    confidence = ""
    nn = ""
    is_right = True


class Statistics:
    def __init__(self):
        self.__statistics = {}
        self.__false_positive_count = 0
        self.__mutex = Lock()

    @property
    def statistics(self):
        return self.__statistics

    @property
    def localized_statistics(self):
        ret = {}
        for atomic_class in self.__statistics:
            ret[localize(atomic_class)] = self.__statistics[atomic_class]
        return ret

    def update(self, detection: Detection):
        with self.__mutex:
            if detection.atomic_class in self.__statistics:
                self.__statistics[detection.atomic_class] += 1
            else:
                self.__statistics[detection.atomic_class] = 1

            if not detection.is_right:
                self.__false_positive_count += 1

    def save(self, path):
        with open(f"{path}_statistics.txt", "w") as f:
            f.write(str(self.__statistics))
            f.write(f"\nКоличество ЛП: {self.__false_positive_count}")


