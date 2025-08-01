
# my_module/utils.py

def useful_function():
    """This function is actively used by main.py."""
    print("Executing the useful function.")
    return "This is a result."

def old_calculation(a, b):
    """
    This function is a relic from a past version and is no longer called anywhere.
    Vulture should identify it as 100% unused code.
    """
    # This complex logic is no longer needed.
    result = (a * a) + (b * b)
    return result

def another_useful_function():
    """Another function that does something useful."""
    return "Something else."