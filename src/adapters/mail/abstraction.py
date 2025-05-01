from abc import ABC, abstractmethod


class AbstractMailAdapter(ABC):
    @abstractmethod
    def send_mail(self, to: list[str], subject: str, body: str):
        raise NotImplementedError
