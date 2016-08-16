# Dependency Algorithm

Here is my take on an algorithm in Python that resolves dependencies. I walk through the process of creating the algorithm in `dependency_algo.ipynb`, and implement it in a `Dependencies` class in `Dependencies.py`. The `Dependencies` class accepts as an input a dictionary of items as keys and lists of dependencies as values (see below). Alternatively, you may use the `add_item` method to add items to a `Dependencies` object.

I did not look at other dependency algorithms when creating this, but afterwards I found some [great work by Ferry Boender](http://www.electricmonk.nl/log/2008/08/07/dependency-resolving-algorithm/) that used recursion to resolve dependencies. My solutions do not use recursion.

## Example 

Dictionary of items we want to resolve dependencies for:

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

We can use the `Dependencies` class to take these items and order them.

```python
import collections
from Dependencies import Dependencies

# Creating a Dependencies object
dependencies = Dependencies(my_items)

# The order method returns an OrderedDict
print Dependencies(my_items).order()
```

```
>>> OrderedDict([('B', []),
>>>              ('F', []),
>>>              ('E', ['F']),
>>>              ('D', ['B', 'E']),
>>>              ('C', ['D']),
>>>              ('A', ['B', 'C', 'D']),
>>>              ('Z', ['A', 'B', 'C', 'D'])])
```

We can also output a list of the item names in order

```python
print Dependencies(my_items).order_list()
```

```
>>> ['B', 'F', 'E', 'D', 'C', 'A', 'Z']
```


## Files

- `dependency_algo.ipynb` Jupyter Notebook where I walk through the steps I used in creating the algorithm
- `Dependencies.py` contains the `Dependencies` class used to order a dictionary of items and their dependencies
- `tests.py` has a few quick tests to check to make sure that the `Dependencies` class is functioning correctly
