def conjugate_points(points_count):
    """
    Conjugates number of points (in a range 0 to 10) in Polish language.

    :param points_count: number of points
    :return: conjugated word
    """
    if points_count == 0:
        result = "punktów"
    elif points_count == 1:
        result = "punkt"
    elif 2 <= points_count <= 4:
        result = "punkty"
    elif 5 <= points_count <= 10:
        result = "punktów"
    else:
        raise ValueError("Number of points must be between 0 and 10.")
    return result


def string_is_integer(value):
    return value.isdigit()
