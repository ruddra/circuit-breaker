# Circuit Breaker

A naive circuit breaker implementation in Python.

## Usage
Import the decorator from `circuit_breaker` folder and use it in a function like this:

```python
from circuit_breaker import circuit_breaker


@circuit_breaker
def some_function():
    # rest of the code
```

Please see the `solution.py` file for more understanding on how this decorator can be used.

## Test

To see the decorator work, please run `python solution.py` and you will see logs like this:

![screenshot](https://raw.githubusercontent.com/ruddra/circuit_breaker/master/circuitbreaker.jpg)

## License

MIT
