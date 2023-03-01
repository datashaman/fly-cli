import pytest
import sys
from fly_cli import FlyCLI

class NoMethods:
    pass

class NoArguments:
    def method(self):
        return ()

class PositionalArgument:
    def method(self, arg1):
        return (arg1,)

class TwoPositionalArguments:
    def method(self, arg1, arg2):
        return (arg1, arg2)

def test_no_methods(fly):
    sys.argv = ['script']
    with pytest.raises(Exception):
        fly(NoMethods())

def test_no_arguments(fly, capsys):
    sys.argv = ['script', 'method']
    fly(NoArguments())
