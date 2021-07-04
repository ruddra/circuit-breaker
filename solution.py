
from random import randint
from time import sleep
from webhook import WebhookService, RuntimeException
from utils import timeit
from circuit_breaker import CircuitBreakerExpection, CircuitBreaker as circuit


class Solution():
    def __init__(self):
        self.webhook = WebhookService()

    def main(self):
        for i in range(10000):
            marchent_id = randint(1, 5)
            try:
                self.process_marchent(marchent_id)
            except CircuitBreakerExpection as e:
                print(f'Circuit is broken. Status: {str(e)}')
                print(f'Will sleep 10 seconds')
                sleep(10)

    @timeit
    @circuit(recovery_timeout=5)
    def process_marchent(self, marchent):
        return self.webhook.send(marchent)


if __name__ == '__main__':
    Solution().main()
