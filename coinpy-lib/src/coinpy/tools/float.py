
def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False