import secrets
from abc import ABC, abstractmethod


class TokensHelper(ABC):
    @abstractmethod
    def token_exists(self, token: str) -> bool:
        pass

    @abstractmethod
    def add_token(self, token: str) -> None:
        pass

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token

    @abstractmethod
    def get_tokens(self) -> list[str]:
        """
        Get all tokens
        """

    @abstractmethod
    def delete_token(self, token: str) -> None:
        """
        Delete token from storage
        :param token:
        :return:
        """
