import os


class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    TESSERACT_CMD: str | None = os.getenv("TESSERACT_CMD")


settings = Settings()
