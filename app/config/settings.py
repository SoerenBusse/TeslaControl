from pydantic import BaseSettings


class Settings(BaseSettings):
    tesla_account_email: str
    vehicle_vin: str
    api_username: str
    api_password: str
    token_file_path: str


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
