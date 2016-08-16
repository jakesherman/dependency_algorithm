"""tests.py - quick tests to check that Dependencies.py is working correctly.
"""

import collections
from Dependencies import Dependencies


def ipynb_check():
    """Check that the my_items dictionary from the .ipynb file is successfully
    ordered by Dependencies.py
    """
    my_items = {
        'A': ['B', 'C', 'D'],  # -- A is dependent on B, C, D,
        'B': [],  # -- B is dependent on nothing, etc.
        'C': ['D'],
        'D': ['B', 'E'],
        'E': ['F'],
        'F': [],
        'Z': ['A', 'B', 'C', 'D']
    }
    correct_order_list = ['B', 'F', 'E', 'D', 'C', 'A', 'Z']
    correct_order = collections.OrderedDict([
        ('B', []),
        ('F', []),
        ('E', ['F']),
        ('D', ['B', 'E']),
        ('C', ['D']),
        ('A', ['B', 'C', 'D']),
        ('Z', ['A', 'B', 'C', 'D'])
    ])
    dependencies = Dependencies(my_items)
    return all([dependencies.order() == correct_order, 
        dependencies.order_list() == correct_order_list])


def other_check():
    """Second check.
    """
    my_items = {
        'A': ['E'],
        'B': ['A', 'C', 'Z'],
        'C': ['Z'],
        'Z': ['E'],
        'E': []
    }
    correct_order_list = ['E', 'Z', 'A', 'C', 'B']
    correct_order = collections.OrderedDict([
        ('E', []),
        ('Z', ['E']),
        ('A', ['E']),
        ('C', ['Z']),
        ('B', ['A', 'C', 'Z'])
    ])
    dependencies = Dependencies(my_items)
    return all([dependencies.order() == correct_order, 
        dependencies.order_list() == correct_order_list])


def test_dependencies_exist():
    my_items = {
        'A': ['B', 'C', 'D'],
        'B': [],  
        'C': ['D'],
        'D': ['B', 'E'],
        'E': ['A'],
        'F': [],
        'Z': ['A', 'B', 'C', 'D', 'Y']
    }
    try:
        Dependencies(my_items).order()
        return False
    except AssertionError:
        return True


def test_circular_dependencies():
    my_items = {
        'A': ['B', 'C', 'D'],
        'B': [],  
        'C': ['D'],
        'D': ['B', 'E'],
        'E': ['A'],
        'F': [],
        'Z': ['A', 'B', 'C', 'D']
    }
    try:
        Dependencies(my_items).order()
        return False
    except AssertionError:
        return True


def main():
    assert ipynb_check(), 'ipynb_check failed!'
    assert other_check(), 'other_check failed!'
    assert test_dependencies_exist(), 'dependencies_exist failed!'
    assert test_circular_dependencies(), 'circular_dependencies failed!'
    print '\nAll tests passed!'
    

if __name__ == '__main__':
    main()
