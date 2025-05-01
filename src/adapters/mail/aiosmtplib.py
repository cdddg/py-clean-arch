from .abstraction import AbstractMailAdapter


class AiosmtplibMailAdapter(AbstractMailAdapter):
    def send_mail(self, to: list[str], subject: str, body: str):
        # TODO: To be implemented
        ...
