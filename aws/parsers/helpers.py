"""
Function wrappers to help parse data.
"""

def parse_bool(f):
    """
    Parse a boolean from the text returned from a function.
    
    :param f: 
    :return: 
    """
    def inner(*args, **kwargs):
        r = f(*args, **kwargs)
        if not r:
            return False
        return r.lower() == 'true'
    return inner


def first_element(f):
    """
    Return the first element in a list if it exists, otherwise return None.
    
    :param f: 
    :return: 
    """
    def inner(*args, **kwargs):
        r = f(*args, **kwargs)
        if r:
            return r[0]
        return
    return inner


def load_into(element_wrapper, *args, **kwargs):
    """
    Decorator function to take the returned xpath element and return a new BaseElementWrapper subclass instance
    from it.

    :param element_wrapper: Subclass of BaseElementWrapper
    :param args: Positional args provided to the __init__ method of the subclass.
    :param kwargs: Keyword args provided to the __init__ method of the subclass.
    :return: 
    """

    def wrapper(f):
        def inner(*fargs, **fkwargs):
            r = f(*fargs, **fkwargs)
            if isinstance(r, list):
                return [element_wrapper(x, *args, **kwargs) for x in r]
            return element_wrapper(r, *args, **kwargs)

        return inner
    return wrapper