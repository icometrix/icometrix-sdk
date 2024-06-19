from abc import abstractmethod, ABC


class ApiClient(ABC):
    """
    Interface for API clients, used to make HTTP calls to the icometrix API
    """

    @abstractmethod
    def get(self, uri: str, **kwargs) -> dict:
        pass

    @abstractmethod
    def post(self, uri: str, data: dict, **kwargs) -> dict:
        pass

    @abstractmethod
    def put(self, uri: str, data: dict, **kwargs) -> dict:
        pass

    @abstractmethod
    def delete(self, uri: str, **kwargs):
        pass

    @abstractmethod
    def put_file(self, uri: str, fields, **kwargs):
        pass

    @abstractmethod
    def stream_file(self, uri: str, out_path: str, **kwargs):
        pass
