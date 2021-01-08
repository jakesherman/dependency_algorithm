"""test_dependency_algorithm.py - tests :)
"""

from dependency_algorithm import Dependencies
import pytest


################################################################################
# Data structures to use in these tests
################################################################################

# Two mistakes: (1) Y doesn't exist, and (2) circular dependency between E and A
items_2_mistakes = {
    'A': ['B', 'C', 'D'],  # -- A is dependent on B, C, D,
    'B': [],  # -- B is dependent on nothing, etc.
    'C': ['D'],
    'D': ['B', 'E'],
    'E': ['A'],
    'F': [],
    'Z': ['A', 'B', 'C', 'D', 'Y']
}

# One mistakes: circular dependency between E and A
items_1_mistakes = {
    'A': ['B', 'C', 'D'],  # -- A is dependent on B, C, D,
    'B': [],  # -- B is dependent on nothing, etc.
    'C': ['D'],
    'D': ['B', 'E'],
    'E': ['A'],
    'F': [],
    'Z': ['A', 'B', 'C', 'D']
}

# No mistakes
items_0_mistakes = {
    'A': ['B', 'C', 'D'],  # -- A is dependent on B, C, D,
    'B': [],  # -- B is dependent on nothing, etc.
    'C': ['D'],
    'D': ['B', 'E'],
    'E': ['F'],
    'F': [],
    'Z': ['A', 'B', 'C', 'D']
}

# Correct version of items_0_mistakes where all dependencies are complete
items_0_mistakes_complete = {
    'B': [],
    'F': [],
    'E': ['F'],
    'D': ['E', 'F', 'B'],
    'C': ['E', 'F', 'B', 'D'],
    'A': ['C', 'B', 'D', 'F', 'E'],
    'Z': ['A', 'C', 'D', 'B', 'F', 'E']
}

# All possible correct orderings of the items in items_0_mistakes such that all
# dependencies resolve correctly
items_0_mistakes_all_possible_correct = [
    ['F', 'E', 'B', 'D', 'C', 'A', 'Z'],
    ['F', 'B', 'E', 'D', 'C', 'A', 'Z'],
    ['B', 'F', 'E', 'D', 'C', 'A', 'Z']
]

################################################################################
# Test the items_ data structures above
################################################################################


def test_existing_dependencies():
    """Does the existing dependency check work?
    """
    deps = Dependencies(items_2_mistakes)
    assert not deps.dependencies_exist(verbose=False)
    deps = Dependencies(items_1_mistakes)
    assert deps.dependencies_exist(verbose=False)
    deps = Dependencies(items_0_mistakes)
    assert deps.dependencies_exist(verbose=False)


def test_circular_dependencies():
    """Ensure that the circular dependency checker works
    """
    deps = Dependencies(items_1_mistakes)
    assert not deps.no_circular_dependencies()
    deps = Dependencies(items_0_mistakes)
    assert deps.no_circular_dependencies()


def test_complete_dependencies_check():
    """Check that the complete_dependencies and complete_dependencies_dict 
    methods are working successfully
    """
    deps = Dependencies(items_0_mistakes)
    test_passed = True

    # Does deps.complete_dependencies work?
    for item, in items_0_mistakes_complete.keys():
        if deps.complete_dependencies(item) != items_0_mistakes_complete[item]:
            test_passed = False
            
    # Does deps.complete_dependencies_dict work?
    if deps.complete_dependencies_dict() != items_0_mistakes_complete:
        test_passed = False

    assert test_passed


def test_dependency_resolution():
    """Dependencies are ordered correctly such that they successfully resolve?
    """
    deps = Dependencies(items_0_mistakes)
    dependency_order = deps.resolve_dependencies()
    assert dependency_order in items_0_mistakes_all_possible_correct


def test_all_possible_correct_orderings():
    """Check to see if we can successfully produce all possbile orderings of the
    dependencies that resolve them
    """
    deps = Dependencies(items_0_mistakes)
    all_possible_correct_orderings = deps.all_possible_resolution_orders()
    assert set(all_possible_correct_orderings) == \
        set([tuple(x) for x in items_0_mistakes_all_possible_correct])
