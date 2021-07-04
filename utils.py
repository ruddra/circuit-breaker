import logging
import time
from functools import wraps

logger = logging.getLogger('circuitbreaker')


class TimeIt():
    def __init__(self):
        self.start_time = time.time()

    def __call__(self, my_func):
        @wraps(my_func)
        def timed(*args, **kw):
            t_start = time.time()
            output = my_func(*args, **kw)
            t_end = time.time()
            logger.info(
                f'{my_func.__name__} took {t_end-t_start} seconds to execute\n'
            )
            logger.info(f'Total time took {t_end - self.start_time}')
            return output
        return timed


timeit = TimeIt()
