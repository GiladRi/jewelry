from functools import wraps
import typing


def _true(*args, **kwargs):
    return True


def _empty(*args, **kwargs):
    pass


class ValidationException(Exception):
    pass


def jewelry(
        validators: typing.Union[tuple[callable], list[callable]] = None,
        before_function: typing.Union[callable, tuple[callable], list[callable]] = _empty,
        after_function: typing.Union[callable, tuple[callable], list[callable]]= _empty,
        formatter: callable = None) -> callable:
    def wrapper(function: callable) -> callable:
        @wraps(function)
        def inner(*args, **kwargs) -> callable:
            # Validates the input(s)
            if validators and not all(bool_values := [validator(*args, **kwargs) for validator in validators]):
                raise ValidationException(
                    f"The next validators returned 'False' values: {[validator.__name__ for (index, validator) in enumerate(validators) if not bool_values[index]]} "
                )

            # Before the wrapped function
            if isinstance(before_function, (tuple, list)):
                before_output = before_function[0](*args, **kwargs)
                for func in before_function[1:]:
                    before_output = func(before_output) if before_output else func(*args, **kwargs)
            else:
                before_function(*args, **kwargs)
            # The wrapped function
            output = function(*args, **kwargs)

            # After the wrapped function
            if isinstance(after_function, (tuple, list)):
                after_output = after_function[0](*args, **kwargs)
                for func in after_function[1:]:
                    after_output = func(after_output) if after_output else func(*args, **kwargs)
            else:
                after_output = after_function(*args, **kwargs)

            output = after_output if after_output else output
            return formatter(output) if formatter else output

        return inner

    return wrapper
