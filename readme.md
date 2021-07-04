# circuit_breaker

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
