from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv('.env')


class _Settings(BaseSettings):
    uybor_hostname: str
    uybor_api_version: str

    olx_hostname: str
    olx_api_version: str


settings = _Settings()
