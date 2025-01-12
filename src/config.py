import os
from dotenv import load_dotenv

class EnvConfig:
    """
    Loads key-value pairs from a .env file and provides
    convenient getters for various types.
    """

    def __init__(self, env_file: str = "config/.env"):
        """
        :param env_file: Path to the .env file
        """
        self.env_file = env_file
        self._loaded = False

    def load(self) -> bool:
        """
        Loads environment variables from the .env file.
        Returns True if the file is found and loaded, False otherwise.
        """
        # load_dotenv returns True if the file was found, False if not
        result = load_dotenv(dotenv_path=self.env_file, override=True)
        # For older versions of python-dotenv, load_dotenv might not return bool
        self._loaded = bool(result)  # Convert to bool just in case
        if not self._loaded:
            print(f"[WARNING] Could not load .env file: {self.env_file}")
        return self._loaded

    def get(self, key: str, fallback=None) -> str:
        """
        Gets an environment variable as a string.
        :param key: The environment variable name
        :param fallback: Value to return if the key is missing
        :return: The string value or fallback
        """
        if not self._loaded:
            raise ValueError("EnvConfig not loaded. Call load() first.")
        return os.getenv(key, fallback)

    def get_int(self, key: str, fallback=None) -> int:
        """
        Gets an environment variable as an integer.
        """
        val = self.get(key, fallback)
        if val is None:
            # No fallback provided
            raise ValueError(f"Missing environment variable: {key}")
        try:
            return int(val)
        except ValueError:
            raise ValueError(f"Cannot convert environment variable '{key}' to int.")

    def get_float(self, key: str, fallback=None) -> float:
        """
        Gets an environment variable as a float.
        """
        val = self.get(key, fallback)
        if val is None:
            raise ValueError(f"Missing environment variable: {key}")
        try:
            return float(val)
        except ValueError:
            raise ValueError(f"Cannot convert environment variable '{key}' to float.")
