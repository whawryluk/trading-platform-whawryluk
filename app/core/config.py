from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	environment: str = "production"

	class Config:
		env_file = ".env"
		fields = {
			"environment": {"env": "ENVIRONMENT"}
		}
