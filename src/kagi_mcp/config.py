import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class to manage environment variables.
    """

    def __init__(self):
        self.KAGI_API_KEY = self.get_env_var("KAGI_API_KEY", required=True)
        self.LOG_LEVEL = self.get_env_var("LOG_LEVEL", default="INFO")
        self.KAGI_URL = self.get_env_var("LOG_LEVEL", default="https://kagi.com/api/v0/")

    @staticmethod
    def get_env_var(var_name, default=None, required=False):
        """
        Fetches an environment variable.

        :param var_name: Name of the environment variable
        :param default: Default value if the variable is not set (optional)
        :param required: Whether the variable is required. Raises an error if not found (default: False)
        :return: The value of the environment variable
        """
        value = os.getenv(var_name, default)
        if required and not value:
            raise ValueError(
                f"{var_name} environment variable is required but not set."
            )
        return value
