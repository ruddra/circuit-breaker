import logging
from functools import wraps
from datetime import datetime, timedelta

# Circuit status
STATE_CLOSED = 'closed'
STATE_OPEN = 'open'
STATE_HALF_OPEN = 'half_open'

logger = logging.getLogger('circuitbreaker')


class CircuitBreaker(object):
    """
    Decorator class for Circuit breaker implementation
    """
    FAILURE_THRESHOLD = 5  # 5 retries
    RECOVERY_TIMEOUT = 30  # will wait 30 seconds before closing the circuit
    EXPECTED_EXCEPTION = Exception  # the exception it expects from the function
    FALLBACK_FUNCTION = None  # fallback function will be called if circuit is open

    def __init__(self, failure_threshold=None, recovery_timeout=None, expected_exception=None, fallback_func=None):
        """
        Initiating the object with parameters for configuring the breaker
        """
        self.failure_threshold = failure_threshold or self.FAILURE_THRESHOLD
        self.recovery_timeout = recovery_timeout or self.RECOVERY_TIMEOUT
        self.expected_exception = expected_exception or self.EXPECTED_EXCEPTION
        self.fallback_func = fallback_func or self.FALLBACK_FUNCTION
        self.opts = dict(circuit_opened=None, will_recover=None,
                         state=STATE_CLOSED, total_failed=0)  # holding circuit state information

    @property
    def _state(self):
        if self.opts['state'] == STATE_OPEN and datetime.now() > self._will_recover:
            # if current time is bigger then recovery time then
            # we half open the circuit
            self.opts['state'] = STATE_HALF_OPEN
            self.opts['total_failed'] = 0
        return self.opts['state']

    @property
    def _total_failed(self):
        return self.opts['total_failed']

    @property
    def _circuit_opened(self):
        return self.opts['circuit_opened']

    @property
    def _will_recover(self):
        return self.opts['will_recover']

    def __call__(self, func):
        @ wraps(func)
        def decorated(*args, **kwargs):
            if self._state == STATE_OPEN:
                # circuit is open, we either call fallback function
                # or just raise exception
                if self.fallback_func:
                    return self.fallback_func(*args, **kwargs)
                raise CircuitBreakerExpection(
                    func, **self.opts)
            self.process_func(func, *args, **kwargs)
        return decorated

    def update_state(self):
        # update the opts values after each iteration of the decorator
        will_recover = None
        circuit_opened = None
        total_failed = self._total_failed
        if total_failed > self.failure_threshold or \
                self._state == STATE_HALF_OPEN and self._total_failed > 0:
            # if total failed count exceeds threshold value, then we open the circuit
            # also if the circuit is in half open state, we will open it if there is any new error
            state = STATE_OPEN
            circuit_opened = datetime.now()
            will_recover = datetime.now() + \
                timedelta(seconds=self.recovery_timeout)
        else:
            # otherwise we close the circuit
            state = STATE_CLOSED
            total_failed = 0

        self.opts.update({
            'state': state,
            'circuit_opened': circuit_opened,
            'will_recover': will_recover,
            'total_failed': total_failed
        })

    def process_func(self, func, *args, **kwargs):
        """
        run the function passing through the decorator
        """
        results = None
        try:
            results = func(*args, **kwargs)
        except self.expected_exception:
            self.opts['total_failed'] = self.opts['total_failed'] + 1

        self.update_state()
        logger.info(f'Circuit status: {str(self.opts)}')
        return results


class CircuitBreakerExpection(Exception):
    """
    Raise custom error if Circuit is open
    """

    def __init__(self, func, state=None, total_failed=None, circuit_opened=None, will_recover=None):
        self.func = func
        self.circuit_opened = circuit_opened
        self.will_recover = will_recover

    def __str__(self):
        return f"Circuit opened for {self.func.__name__} at {self.circuit_opened} \n" \
            f"Will recover at {self.will_recover}"


circuit_breaker = CircuitBreaker()
