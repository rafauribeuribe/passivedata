from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MICROSOFT_CLIENT_ID: str = ""
    MICROSOFT_CLIENT_SECRET: str = ""
    MICROSOFT_TENANT_ID: str = ""
    REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    SECRET_KEY: str = "dev-secret-key"
    DATABASE_URL: str = "sqlite:///./passivedata.db"
    FRONTEND_URL: str = "http://localhost:3000"

    @property
    def authority(self):
        return f"https://login.microsoftonline.com/{self.MICROSOFT_TENANT_ID}"

    @property
    def scopes(self):
        return ["https://graph.microsoft.com/.default"]

    @property
    def configured(self):
        return bool(self.MICROSOFT_CLIENT_ID and
                    self.MICROSOFT_CLIENT_ID != "TU_CLIENT_ID_AQUI")

    class Config:
        env_file = ".env"


settings = Settings()
