from pydantic_settings import BaseSettings

class SettingsFrontendApp(BaseSettings):

    class Config:
        env_file = '.env'

FrontendSettings = SettingsFrontendApp()