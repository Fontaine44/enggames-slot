from abc import ABC, abstractmethod

class Animation(ABC):
    def __init__(self):
        self.current_animation_time = 0
        self.playing = False
    
    def start(self):
        self.playing = True
    
    def stop(self):
        self.playing = False

    @abstractmethod
    def play(self):
        pass

    # @abstractmethod
    # def reset(self):
    #     pass