class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

####################### pattern #######################

import inspect
from itertools import chain


class MatchError(TypeError):
    pass


Any = lambda obj: obj is not None
Not = lambda func: lambda *args, **kwargs: not func(*args, **kwargs)
OfType = lambda type_: lambda obj: isinstance(obj, type_)


d_funcs = {}
# (frame, func_name): (argspec, [(d_pattern, func), ...])


def destructuring_bind((args, varargs, keywords, defaults), values, kwargs):
    d_arguments = {}
    iter_values = chain(values, defaults or ())
    if keywords:
        used_kwargs = []
    for var in args:
        try:
            value = next(iter_values)
        except StopIteration:
            value = kwargs[var]
            if keywords:
                used_kwargs.append(var)
        if isinstance(var, list):
            d_arguments.update(destructuring_bind(var, None, None, value, None))
        else:
            d_arguments[var] = value
    if varargs:
        d_arguments[varargs] = list(iter_values)
    if keywords:
        d_arguments[keywords] = {k: v for k, v in kwargs.items() if k not in used_kwargs}
    return d_arguments


def match(**pattern):
    frame = inspect.stack()[1][0]
    def decorator(func):
        if not all(key in func.func_code.co_varnames for key in pattern):
            raise SyntaxError("pattern matching rule doesn't agree with the argument list")
        index = (frame, func.func_name)
        if index not in d_funcs:
            d_funcs[index] = (inspect.getargspec(func), [])
        else:
            if inspect.getargspec(func) != d_funcs[index][0]:
                raise SyntaxError("argument list inconsistent")
        argspec, l_pattern_func = d_funcs[index]
        l_pattern_func.append((pattern, func))
        def find_match(*args, **kwargs):
            d_arguments = destructuring_bind(argspec, args, kwargs)
            for pattern, func in l_pattern_func:
                if all(
                        (pattern[name](value) if callable(pattern[name]) else value == pattern[name])
                        for name, value in d_arguments.items() if name in pattern):
                    return func(*args, **kwargs)
            raise MatchError
        return find_match
    return decorator

######################### pipe ########################

class Pipe:
    def __init__(self, funcs=()):
        self.funcs = funcs

    def __or__(self, other):
        return Pipe(self.funcs + (other, ))

    def __call__(self, arg):
        return reduce(lambda result, func: func(result) , self.funcs, arg)

P = Pipe()


######################### let #########################

import copy
from contextlib import contextmanager

@contextmanager
def let(*internals, **bindings):
    target_locals = inspect.stack()[2][0].f_locals
    original = {var: target_locals[var] for var in bindings.keys()}
    for var in internals:
        if var in target_locals:
            original[var] = target_locals[var]
        else:
            target_locals[var] = None
    target_locals.update(bindings)
    yield
    for var in internals:
        del target_locals[var]
    target_locals.update(original)
