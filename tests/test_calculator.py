import pytest
from app.tools.calculator import calculate
def test_calculator(): assert calculate('2 + 3 * 4')=='14.0'
def test_rejects_python():
 with pytest.raises(ValueError): calculate("__import__('os').system('whoami')")
