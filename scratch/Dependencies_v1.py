import collections


class Dependencies(object):
    """Orders a dictionary of items to their dependencies such that all 
    dependencies resolve. Initialize the class with the [items] object:

    {
        'item1': ['dependency1', 'dependency2', ...],
        'item2': ['dependency1', 'dependency2', ...],
        ...
    }

    Alternatively, the class can be intiailized with no items, and items can 
    be added with the add_item method.

    The order method returns an OrderedDict of self.items in an order that 
    resolves all dependencies, and the order_list method does the same but 
    simply returns a list of item names in order.

    This class also ensures that all dependencies exist, and no circular
    dependencies exist. These checks happen when calling the order or order_list
    methods.
    """
    
    def __init__(self, items = {}):
        """Perform dependency existance and no circular dependencies checks
        when initializing a Dependencies object.
        """
        assert isinstance(items, dict), '[items] must be a dict'
        assert self.dependencies_exist(items), \
            'One or more dependencies do not exist in [items]'
        assert self.no_circular_dependencies(items), \
            'One or more circular dependencies exist in [dependencies]'
        self.items = items.copy()
        
        
    @staticmethod
    def dependencies_exist(my_items):
        """Check if the initial dependencies for the items in [my_items] exist 
        in [my_items].
        """
        all_dependencies_exist = True
        for item, dependencies in my_items.items():
            for dependency in dependencies:
                if dependency not in my_items.keys():
                    print 'Non-existant dependency: ({0}, {1})'.format(
                        item, dependency)
                    all_dependencies_exist = False
        return all_dependencies_exist
    
    
    @staticmethod
    def list_dependencies(my_items, item):
        """Find all dependencies for [item] within [my_items].
        """
        dependencies, new_dependencies_count = list(my_items[item]), -1
        while new_dependencies_count != 0:
            new_dependencies_count = 0
            for item in dependencies:
                new_dependencies = [new_item for new_item in my_items[item] 
                                    if new_item not in dependencies]
                dependencies += new_dependencies
                new_dependencies_count += len(new_dependencies)
        return dependencies

    
    def no_circular_dependencies(self, my_items):
        """Check for any circular dependencies in [my_items].
        """
        not_circular = True
        for item in my_items.keys():
            dependencies = self.list_dependencies(my_items, item)
            if item in dependencies:
                not_circular = False
                print 'Circular dependency for', item
        return not_circular
        
        
    def add_item(self, item, dependencies = []):
        """Add a new item to self.dependencies, along with optional dependencies
        for that item.
        """
        if self.items.has_key(item):
            raise Exception('{0} already an item!'.format(str(item)))
        else:
            self.items[item] = dependencies
            
            
    def remove_item(self, item):
        """Add a new item to self.dependencies, along with optional dependencies
        for that item.
        """
        if not self.items.has_key(item):
            raise Exception('{0} does not exist!'.format(str(item)))
        else:
            del self.items[item]
            
            
    def modify_item(self, item, dependencies = []):
        """Modify the dependencies for an item.
        """
        if not self.items.has_key(item):
            raise Exception('{0} does not exist!'.format(str(item)))
        else:
            self.items[item] = dependencies
            
            
    def order_dependencies(self, my_items):
        """Order the dependencies in [my_items], returning a list of keys from
        [my_items] in order such that all dependencies resolve.
        """
        items, index = my_items.keys(), 0
        while (len(items) - 1) != index:
            item = items[index]
            current_dependencies = self.list_dependencies(my_items, item)
            no_order_change = True
            for dependency in current_dependencies:
                if items.index(dependency) - items.index(item) > 0:
                    items += [items.pop(index)]
                    no_order_change = False
                    break
            if no_order_change:
                index += 1
        return items
    
    
    def order(self):
        """Return self.items as an OrderedDict in an order that resolves
        all dependencies.
        """
        self.__init__(self.items)
        if self.items:
            ordered_items = self.order_dependencies(self.items)
            return collections.OrderedDict(
                [(item, self.items[item]) for item in ordered_items])
        else:
            return {}
        
    
    def order_list(self):
        """Returns the keys of self.items (the item names) in an order 
        that resolves all dependencies.
        """
        self.__init__(self.items)
        if self.items:
            return self.order_dependencies(self.items)
        else:
            return []
    
    
    def __str__(self):
        return str(self.items)
    
    
    __repr__ = __str__
