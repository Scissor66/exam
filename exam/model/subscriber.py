from django.db import models


class SubscriberException(Exception):
    pass


class Subscriber(models.Model):
    uuid = models.UUIDField(db_index=True)
    name = models.CharField(max_length=1000, help_text='ФИО абонента')
    balance = models.IntegerField(help_text='Текущий баланс на счете')
    hold = models.IntegerField(help_text='Холды на счете')
    status = models.BooleanField(help_text='Счет открыт')

    @classmethod
    def _check_amount(cls, amount):
        if amount <= 0:
            raise SubscriberException('Amount must be positive')

    def _check_status(self):
        if not self.status:
            raise SubscriberException('Account is closed')

    def _check_substraction_is_possible(self, amount):
        if self.balance < (amount + self.hold):
            raise SubscriberException('Balance is insufficient')

    @classmethod
    def find_by_uuid(cls, uuid):
        subscriber = Subscriber.objects.filter(uuid=uuid).first()
        if not subscriber:
            raise SubscriberException('Subscriber is not found')
        return subscriber

    def add(self, amount):
        self._check_amount(amount)
        self._check_status()

        self.balance += amount
        self.save()

    def substract(self, amount):
        self._check_amount(amount)
        self._check_status()
        self._check_substraction_is_possible(amount)

        self.balance -= amount + self.hold
        self.hold = 0
        self.save()

    def unhold(self):
        self._check_status()
        self._check_substraction_is_possible(0)

        self.balance -= self.hold
        self.hold = 0
        self.save()
