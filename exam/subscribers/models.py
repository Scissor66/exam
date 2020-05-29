from django.db import models, transaction


class SubscriberException(Exception):
    pass


class Subscriber(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=1000, help_text='ФИО абонента')
    balance = models.IntegerField(help_text='Текущий баланс на счете')
    hold = models.IntegerField(help_text='Холды на счете')
    status = models.BooleanField(help_text='Счет открыт')

    @classmethod
    def check_amount(cls, amount):
        if amount <= 0:
            raise SubscriberException('Amount must be positive')

    def check_status(self):
        if not self.status:
            raise SubscriberException('Account is closed')

    def check_substraction_is_possible(self, amount):
        if self.balance < (amount + self.hold):
            raise SubscriberException('Balance is insufficient')

    @classmethod
    def find(cls, uuid, updlock=False):
        queryset = Subscriber.objects.filter(uuid=uuid)
        if updlock:
            queryset = queryset.select_for_update()
        subscriber = queryset.first()
        if not subscriber:
            raise SubscriberException('Subscriber is not found')
        return subscriber

    @classmethod
    @transaction.atomic
    def add(cls, uuid, amount):
        subscriber = cls.find(uuid=uuid, updlock=True)
        subscriber.check_amount(amount)
        subscriber.check_status()

        subscriber.balance += amount
        subscriber.save()
        return subscriber

    @classmethod
    @transaction.atomic
    def substract(cls, uuid, amount):
        subscriber = cls.find(uuid=uuid, updlock=True)
        subscriber.check_amount(amount)
        subscriber.check_status()
        subscriber.check_substraction_is_possible(amount)

        subscriber.balance -= amount + subscriber.hold
        subscriber.hold = 0
        subscriber.save()
        return subscriber

    def unhold(self):
        self.check_status()
        self.check_substraction_is_possible(0)

        self.balance -= self.hold
        self.hold = 0
        self.save()
