# scenes/baseScene.py
import abc

class BaseScene(abc.ABC):
    @abc.abstractmethod
    def handle_event(self, event):
        pass

    @abc.abstractmethod
    def update(self, hand_position):
        pass

    @abc.abstractmethod
    def draw(self, screen):
        pass
