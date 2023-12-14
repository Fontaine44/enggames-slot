from abc import ABC, abstractmethod

class Animation(ABC):
    def __init__(self):
        self.current_animation_time = 0
        self.playing = False
    
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def play(self):
        pass