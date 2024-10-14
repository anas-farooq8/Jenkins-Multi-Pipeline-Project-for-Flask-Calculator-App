from app import add, subtract, multiply, divide

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(0, 0) == 0
    assert subtract(5, 10) == -5

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(0, 5) == 0
    assert multiply(-1, 3) == -3

def test_divide():
    assert divide(10, 2) == 5
    assert divide(0, 1) == 0
    assert divide(5, 0) == "Division by zero error"
    assert divide(9, 3) == 3
