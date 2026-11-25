
from app import greet

def test_greet():
    assert greet() == "Hello, DevOps Deployment!"

def test_greet_is_string():
    assert isinstance(greet(), str)

def test_greet_not_empty():
    assert len(greet()) > 0
