from src.variable import Variable as Var


def disable_assertions(func):
    def wrapper(*args, **kwargs):
        if Var.disable_assertions_condition:
            try:
                func(*args, **kwargs)
            except AssertionError:
                pass
        else:
            func(*args, **kwargs)

    return wrapper
