import os
from typing import Optional, List
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
        # Try loading the file immediately
        if not self.load():
            print(f"[WARNING] Default .env file not found: {self.env_file}")

    def load(self) -> bool:
        """
        Loads environment variables from the .env file.
        Returns True if the file is found and loaded, False otherwise.
        """
        result = load_dotenv(dotenv_path=self.env_file, override=True)
        self._loaded = bool(result)
        if not self._loaded:
            print(f"[WARNING] Could not load .env file: {self.env_file}")
        return self._loaded

    def reload(self) -> bool:
        """
        Reloads the environment variables from the .env file.
        """
        return self.load()

    def get(self, key: str, fallback: Optional[str] = None) -> str:
        """
        Gets an environment variable as a string.
        :param key: The environment variable name
        :param fallback: Value to return if the key is missing
        :return: The string value or fallback
        """
        if not self._loaded:
            raise ValueError(
                f"EnvConfig not loaded. Call load() first. File: {self.env_file}"
            )
        val = os.getenv(key, fallback)
        if val is None:
            raise ValueError(
                f"Environment variable '{key}' not found in file: {self.env_file}"
            )
        return val

    def get_int(self, key: str, fallback: Optional[int] = None) -> int:
        """
        Gets an environment variable as an integer.
        """
        val = self.get(key, fallback)
        if val is None:
            raise ValueError(f"Missing environment variable: {key}")
        try:
            return int(val)
        except ValueError:
            raise ValueError(f"Cannot convert environment variable '{key}' to int.")

    def get_float(self, key: str, fallback: Optional[float] = None) -> float:
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

    def get_bool(self, key: str, fallback: Optional[bool] = None) -> bool:
        """
        Gets an environment variable as a boolean.
        - True values: 'true', '1', 'yes', 'y', 't' (case-insensitive)
        - False values: 'false', '0', 'no', 'n', 'f' (case-insensitive)
        """
        val = self.get(key, fallback)
        if val is None:
            raise ValueError(f"Missing environment variable: {key}")
        if isinstance(val, str):
            val = val.lower()
            if val in ('true', '1', 'yes', 'y', 't'):
                return True
            elif val in ('false', '0', 'no', 'n', 'f'):
                return False
        raise ValueError(f"Cannot convert environment variable '{key}' to bool.")

    def get_list(self, key: str, fallback: Optional[List[str]] = None, delimiter: str = ",") -> List[str]:
        """
        Gets an environment variable as a list.
        :param key: The environment variable name
        :param fallback: Value to return if the key is missing
        :param delimiter: The delimiter used to split the string into a list
        :return: A list of strings
        """
        val = self.get(key, fallback)
        if val is None:
            raise ValueError(f"Missing environment variable: {key}")
        return [item.strip() for item in val.split(delimiter)]
    
    def get_color(self, key: str, fallback=None) -> tuple:
        """
        Gets an environment variable as a color tuple.
        """
        val = self.get(key, fallback)
        if val is None:
            raise ValueError(f"Missing environment variable: {key}")
        try:
            return tuple(map(int, val.split(',')))
        except ValueError:
            raise ValueError(f"Cannot convert environment variable '{key}' to color tuple.")

    def __repr__(self) -> str:
        return f"<EnvConfig env_file='{self.env_file}' loaded={self._loaded}>"