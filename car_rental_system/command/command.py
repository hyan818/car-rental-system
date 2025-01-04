from abc import abstractmethod


class Command:
    @abstractmethod
    def handle(self, command):
        pass
