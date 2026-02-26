from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "WeChat QR Order"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./wechat_order.db"
    
    # WeChat Pay
    WECHAT_MCHID: str = ""  # 商户号
    WECHAT_SERIAL_NO: str = ""  # 证书序列号
    WECHAT_PRIVATE_KEY: str = ""  # 商户私钥
    WECHAT_APIV3_KEY: str = ""  # APIv3密钥
    WECHAT_APPID: str = ""  # 公众号或小程序appid
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    class Config:
        env_file = ".env"


settings = Settings()
