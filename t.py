from flask_utils import validate_params


@validate_params()
def my_func(age: int):
    return age


if __name__ == "__main__":
    my_func(26)
