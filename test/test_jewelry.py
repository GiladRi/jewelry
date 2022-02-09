from jewelry import jewelry

def before(*args, **kwargs):
    print("before")
    return 324


def after1(*args, **kwargs):
    print("after1")
    return 1

def after2(*args, **kwargs):
    print("after2")
    return 2

def validate(x):
    return isinstance(x, int)


def my_formatter(output):
    print(output)
    return str(output)


@jewelry(
    validators=[validate, validate],
    before_function=before,
    after_function=(after1, after2),
    formatter=my_formatter
)
def dummy(x: int):
    print("hi", x)
    return 55


# dummy = jewelry(function=dummy, before_function=before, after_function=after)

print(dummy(12))