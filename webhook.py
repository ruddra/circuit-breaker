import time
import random


class RuntimeException(Exception):
    pass


class WebhookService(object):

    def send(self, merchant):
        print(f"TRY: webhook to merchant {merchant}")

        if merchant % 2 == 0:
            self.fail(merchant)

        print(f"SUCCESS: webhook to merchant {merchant}")

    def fail(self, merchant):
        raise RuntimeException(f"Marchent {merchant} failed to process")
