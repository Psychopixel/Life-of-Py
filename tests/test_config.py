import os
import pytest
from src.config import EnvConfig
from dotenv import set_key

@pytest.fixture
def setup_test_env(tmp_path):
    """
    Creates a temporary .env file for testing in a
    temporary directory, then returns the file path.
    """
    env_content = """\
GRID_WIDTH=250
GRID_HEIGHT=300
PREY_INITIAL=10
"""
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)
    return str(env_file)

def test_load_success(setup_test_env):
    cfg = EnvConfig(env_file=setup_test_env)
    loaded = cfg.load()
    assert loaded, "Should successfully load the .env file"

def test_get_values(setup_test_env):
    cfg = EnvConfig(env_file=setup_test_env)
    cfg.load()

    grid_w = cfg.get_int("GRID_WIDTH")
    grid_h = cfg.get_int("GRID_HEIGHT")
    prey_init = cfg.get_int("PREY_INITIAL")
    
    assert grid_w == 250
    assert grid_h == 300
    assert prey_init == 10

def test_missing_key(setup_test_env):
    cfg = EnvConfig(env_file=setup_test_env)
    cfg.load()

    # With a fallback
    missing_value = cfg.get_int("NON_EXISTING_KEY", fallback=-1)
    assert missing_value == -1
    
    # Without fallback, should raise ValueError
    with pytest.raises(ValueError):
        cfg.get_int("NON_EXISTING_KEY_2")

def test_incorrect_type(setup_test_env):
    """
    If we try to convert a non-numeric string to int or float,
    it should raise ValueError.
    """
    # Modify .env content to break a value
    set_key(setup_test_env, "GRID_WIDTH", "not_a_number")

    cfg = EnvConfig(env_file=setup_test_env)
    cfg.load()

    with pytest.raises(ValueError):
        cfg.get_int("GRID_WIDTH")
