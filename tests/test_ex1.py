import pytest

'''
This is to skip a test
@pytest.mark.skip
def test_example():
    assert 1==1
'''

@pytest.mark.skip
def test_example():
    assert 1==1

def test_example2():
    assert 1==1