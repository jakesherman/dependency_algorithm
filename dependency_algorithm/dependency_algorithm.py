"""dependency_algorithm - the algorithm to identify and successfully order/
resolve dependencies
"""

from itertools import permutations 


class MissingDependencyException(Exception):
    """Exception for when a dependency is missing
    """
    pass


class CircularDependencyException(Exception):
    """Exception for when a circular dependency occurs
    """
    pass


class Dependencies(object):
    """Given a dictionary of items mapped to their (partial) dependencies, 
    this class provides methods for computing the complete list of dependencies
    for each item, and ordering the items in a way such that all dependnecies 
    resolve. Also, this class can check that each item's dependencies exist, 
    and that no circular dependencies are present.
    
    Let's illustrate this with a quick example by imagining that we are starting
    with the following dictionary of partial dependencies:

    dependencies = {
        "A": ["B"],  # -- A is dependent on B
        "B": ["C"],  # -- B is dependent on C
        "C": []      # -- C has no dependencies
    }
    
    First, we might be interested in what are all of each item's dependencies...
    for example, A is dependent on B which is dependent on C, so A is therefore
    dependent on both B and C.
    
    Second, we might be interested in what order the dependencies need to be 
    ordered in for them to successfully resolve. In this case, the only possible
    order is C --> B --> A, as any other ordering would result in an item being
    "executed" before one of more of its dependencies.
    """
    
    def __init__(self, dependencies = {}):
        """Initialize the Dependencies object
        """
        assert isinstance(dependencies, dict), '[items] must be a dict'
        self.dependencies = dependencies.copy()
        self.possible_items = list(dependencies.keys())
        self._known_dependencies = {}
        
    
    def dependencies_exist(self, verbose=True):
        """Check if the user inputted partial dependencies (self.items) all 
        exist
        
        Returns
        -------
        whether_dependencies_exist : bool
            True or False, whether all dependencies exist or not
        """
        all_dependencies_exist = True
        for item, dependencies in self.dependencies.items():
            for dependency in dependencies:
                if dependency not in self.possible_items:
                    if verbose:
                        print('Non-existant dependency: ({0}, {1})'.format(
                            item, dependency))
                    all_dependencies_exist = False
        return all_dependencies_exist
    
    
    def _enhanced_list_dependencies(self, my_items, item, known_dependencies={}, 
                                    call_stack_order=set(), debug=False):
        """List the complete set of items that are dependent on a given item 
        (item) in an items dictionary (my_items).

        Parameters
        ----------
        my_items : dict
            A dictionary of {item: list of items that this item depends on}

        item : int or str
            The item in my_items that we want to return a full list of items 
            that this item depends on

        known_dependencies : dict (default of an empty dictionary)
            A dictionary of {item: list of items that this item depends on} that
            is known to be complete. The difference between this and my_items is
            that, for example, if A is dependent on B which is dependent on C 
            which is dependent on nothing, my_items might look like:

            {
                "A": "B",
                "B": "C",
                "C": []
            }

            whereas known_dependencies, when it is complete, will look like:

            {
                "A": ["B", "C"],
                "B": ["C"],
                "C": []
            }

            This function will use known_dependencies as a cache to store known
            complete dependencies. 

        call_stack_order : set
            Whenever we have NOT cached the dependencies for an item, we 
            recursively call this function to find that item's dependencies. 
            When this happens, we add the item that we are recursively calling 
            this function for to the call_stack_order. Each item should only be 
            appearing once in this list because we cache (basically memoize) the
            results of each recursive call. The reason we keep this list is to 
            discover circular dependencies, aka when item 1 is dependent on item
            2 which is dependent on item 1, and so forth. If we don't save 
            call_stack_order and use it to discover circular dependencies, 
            circular dependencies will result in an infinite loop of recursive 
            calls, and will raise an exception when Python's recurssion limit is
            reached.

        debug : bool (default of False)
            In debug mode, this function will print out statements as it 
            recursively travels the tree of dependencies. 

        Returns
        -------
        item_dependencies : list
            The complete list of items that [item] depends on in [my_items]

        known_dependencies : dict
            See above, primarily used as a caching mechanism. If the goal here 
            was just to list the complete set of items that an item depends on, 
            we could probably just add memoization to this function, but the 
            benefit of using known_dependencies is that we can re-use it when 
            looping through an entire items dictionary
            
        call_stack_order : set
            See above

        """

        # List of dependnecies for an item, initially populate with the known 
        # dependencies
        item_dependencies = my_items[item]
        if not isinstance(item_dependencies, list):
            item_dependencies = list(item_dependencies) 

        if debug:
            print("* Current call stack order:", call_stack_order)
            print("Initial item dependencies for {}: ".format(item), 
                item_dependencies)
            print("Current state of known dependencies:", known_dependencies)


        # Traverse the tree of dependencies
        for dependency in item_dependencies:


            # Check to see if we've already cached the dependency or not...
            new_dependencies = known_dependencies.get(dependency)

            if debug:
                print("> Looking into dependency: ", dependency)
                print("** New deps:", new_dependencies)

            if new_dependencies is not None:

                # We HAVE cached the dependencies
                if debug:
                    print(">> Dependency for {} known: ".format(dependency), 
                        new_dependencies)

            else:

                # We have NOT cached the dependencies
                if debug:
                    print(">> Dependency for {} unknown, initiating recursive "
                        "call ..... ".format(dependency))

                if dependency in call_stack_order:
                    raise CircularDependencyException("Circular dependency with"
                        " item: {}".format(dependency))
                else:
                    call_stack_order.add(dependency)

                # Rececursively call this function until we known all of the 
                # possible dependencies
                new_dependencies, known_dependencies, call_stack_order = \
                    self._enhanced_list_dependencies(
                        my_items=my_items, 
                        item=dependency, 
                        known_dependencies=known_dependencies,
                        call_stack_order=call_stack_order,
                        debug=debug
                    ) 

            if new_dependencies:

                # Merge the existing and newly discovered dependencies
                item_dependencies = list(set(
                    item_dependencies + new_dependencies))

        # When we have all of an item's dependencies, add them to the cache, and
        # return the list of the item's dependencies
        if debug:
            print("& All dependencies for {} are known :) they are: ".\
                    format(item), item_dependencies)
        known_dependencies[item] = item_dependencies
        return item_dependencies, known_dependencies, call_stack_order
    
    
    def _complete_dependencies(self, debug=False):
        """Take the input of partial dependencies, and complete it so that all 
        dependencies are flushed out. Here's an example:
        
        dependencies = {
            "A": ["B"],  # -- A is dependent on B
            "B": ["C"],  # -- B is dependent on C
            "C": []      # -- C has no dependencies
        }
        
        C isn't listed as a dependency of A, but it is, because A is dependent
        on B which is dependent on C, therefore (B, C) are dependencies for A.
        
        Parameters
        ----------
        debug : bool (default of False)
            Whether or not to print out statements helping for debugging as the 
            _enhanced_list_dependencies method is called.
            
        Returns
        -------
        known_dependencies : dict
            A dictionary of the same form as the input when initializing this 
            class, but one that is complete, i.e., all dependencies for each 
            item are listed out.
            
        """
        if not self.dependencies_exist(verbose=True):
            raise MissingDependencyException()
            
        for item in self.possible_items:
            _, self._known_dependencies, _ = \
                self._enhanced_list_dependencies(
                    my_items=self.dependencies, 
                    item=item, 
                    known_dependencies=self._known_dependencies, 
                    call_stack_order=set(), 
                    debug=debug
                )
            
    
    def complete_dependencies(self, item):
        """Return the complete list of dependencies for item [item]
        
        Parameters
        ----------
        item : str or int
            The item to return the complete list of dependencies for
            
        Returns
        -------
        dependencies : list
            The complete list of dependencies for item [item]
            
        """
        if self._known_dependencies == {}:
            self._complete_dependencies()
        return self._known_dependencies[item]
    
    
    def complete_dependencies_dict(self):
        """Return the dictionary of items mapped to their complete list of 
        dependencies
       
        Returns
        -------
        complete_dependencies_dict : dict
            Dict of items mapped to their complete list of dependencies
            
        """
        if self._known_dependencies == {}:
            self._complete_dependencies()
        return self._known_dependencies
        
    
    def no_circular_dependencies(self):
        """Check for no circular dependencies (automatically happens during 
        self._enhanced_list_dependencies, so no real need to call this on
        its own).
        
        Returns
        -------
        no_circular_dependencies : bool
            True if no circular dependencies, otherwise False
        
        """
        try:
            self._complete_dependencies()
            return True
        except CircularDependencyException:
            return False
        
    
    def resolve_dependencies(self):
        """Return a list of the dependencies in an order such that they resolve
        successfully. Note that this is only ONE possible ordering, when there 
        are potentially many possible orderings. Use this method if you only 
        care about dependency resolution but don't necessarily care about the 
        order in which dependencies resolve.
        
        Returns
        -------
        ordered_dependencies : list
            A list of the dependencies in an order such that they resolve 
            successfully 
        
        """
        if self._known_dependencies == {}:
            self._complete_dependencies()
        return list(self._known_dependencies.keys())
    
    
    def _check_if_ordering_is_correct(self, ordering):
        """Given an [ordering] of items and a complete dictionary of items to 
        their dependencies [known_dependencies], check to see if the ordering 
        is correct from a dependency management perspective or not.
        """
        if self._known_dependencies == {}:
            self._complete_dependencies()
        items_already_looped_through = set()
        for item in ordering:
            items_already_looped_through.add(item)
            # Loop through each item's complete set of dependencies, if any of 
            # those dependencies haven't already been looped through, then the 
            # ordering is incorrect!
            for item_dependency in self._known_dependencies[item]:
                if item_dependency not in items_already_looped_through:
                    return False
        return True
    
    
    def all_possible_resolution_orders(self, verbose=False):
        """Instead of returning one correct ordering of the input items that 
        successfully resolves their depedencies, return ALL possible orderings. 
        This is a "naive" approach with horrible runtime complexity because it 
        loops through every possible ordering and checks to see whether or not 
        that ordering is correct. I'm working on the "non-naive" approach...
        
        Parameters
        ----------
        verbose : bool (default of False)
            Prints out the # of permutations and # of correct vs. incorrect 
            orderings ("correct" means the dependencies are successfully 
            resolved)
        
        Returns
        -------
        all_possible_orderings : list of lists
            List of lists, each sublist is a possible ordering of the items that
            successfully resolves all dependencies
        
        """
        incorrect_orderings = []
        correct_orderings = []
        
        for my_items_perm in list(permutations(self.possible_items)):
            if self._check_if_ordering_is_correct(my_items_perm):
                correct_orderings.append(my_items_perm)
            else:
                incorrect_orderings.append(my_items_perm)
                
        if verbose:
            num_correct_orderings, num_incorrect_orderings = \
                len(correct_orderings), len(incorrect_orderings)
            print("Number of permutations:", 
                num_correct_orderings + num_incorrect_orderings)
            print("Number of correct orderings:", num_correct_orderings)
            print("Number of incorrect orderings:", num_incorrect_orderings)
            
        return correct_orderings
