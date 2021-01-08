# Dependency Algorithm

Here is my take on an algorithm in Python that resolves dependencies. The best way to illustrate how this works is with an example...

## Example 

Let's say that we have the following dictionary where the keys are items, and the values are the dependencies of those items. Each dependency must itself be an item, and items with no dependencies have an empty list `[]` as they dependency:

```python
my_items = {
    'A': ['B', 'C', 'D'],  # -- A is dependent on B, C, D,
    'B': [],  # -- B is dependent on nothing, etc.
    'C': ['D'],
    'D': ['B', 'E'],
    'E': ['F'],
    'F': [],
    'Z': ['A', 'B', 'C', 'D']
}
```

Note that we've only provided a partial dictionary of items to their dependencies...for example, notice how C is dependent on D, which is dependent on B (no dependencies) and E, which is dependent on F...therefore, C is dependent on D, B, E, and F. 

We can use the `Dependencies` class to get the complete list of dependencies for an item, like so:

```python
from dependency_algorithm import Dependencies

# Creating a Dependencies object
dependencies = Dependencies(my_items)
dependencies.complete_dependencies("C")
```

```
>>> ['D', 'B', 'E', 'F']
```

More importantly, we can return the items in an order such that the dependencies resolve:

```python
dependencies.resolve_dependencies()
```

```
>>> ['B', 'F', 'E', 'D', 'C', 'A', 'Z']
```

In many cases, there are multiple correct ordering of our items such that each item's dependencies resolve. If we're interested in all possible correct orderings, the `Dependencies` class can permutate over all possible orderings, and identify the correct ones (albeit at a high computational cost), like so:

```python
dependencies.all_possible_resolution_orders(verbose=True)
```

```
>>> Number of permutations: 5040
>>> Number of correct orderings: 3
>>> Number of incorrect orderings: 5037
>>> [('B', 'F', 'E', 'D', 'C', 'A', 'Z'),
>>>  ('F', 'B', 'E', 'D', 'C', 'A', 'Z'),
>>>  ('F', 'E', 'B', 'D', 'C', 'A', 'Z')]
```

That's pretty much it! The `Dependencies` class also performs two checks, one for any dependencies that are "missing" (i.e., they are not keys in the input dictionary of items and dependencies), and another for cirular dependencies (i.e., A is dependent on B which is dependent on A which is...and so on...).

## Installation

```
pip install dependency_algorithm
```

## Running the unit tests with `pytest`

```
git clone https://github.com/jakesherman/dependency_algorithm.git
cd dependency_algorithm
pip install -e .
python -m pytest
```

## Future work

* New version of `Dependencies._enhanced_list_dependencies` that uses iteration instead of recursion
* Improved version of `Dependencies.all_possible_resolution_orders` that uses a more efficient algorithm than looping through permutations, ex. a recursive algorithm
