from abc import ABC, abstractmethod

class AbstractAcceptanceFunction(ABC):
    """docstring for AbstractAcceptanceFunction"""
    def __init__(self):
        super().__init__()

    @abstractmethod
    def accept(self):
        pass
