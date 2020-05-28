from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    def _insert_data(apps, schema_editor):
        Subscriber = apps.get_model('exam', 'Subscriber')
        subs1 = Subscriber(
            uuid='26c940a1-7228-4ea2-a3bc-e6460b172040',
            name='Петров Иван Сергеевич', balance=1700, hold=300, status=True,
        )
        subs1.save()

        subs2 = Subscriber(
            uuid='7badc8f8-65bc-449a-8cde-855234ac63e1',
            name='Kazitsky Jason', balance=200, hold=200, status=True,
        )
        subs2.save()

        subs3 = Subscriber(
            uuid='5597cc3d-c948-48a0-b711-393edf20d9c0',
            name='Пархоменко Антон Александрович', balance=10, hold=300, status=True,
        )
        subs3.save()

        subs4 = Subscriber(
            uuid='867f0924-a917-4711-939b-90b179a96392',
            name='Петечкин Петр Измаилович', balance=1000000, hold=1, status=False,
        )
        subs4.save()

    operations = [
        migrations.RunPython(_insert_data),
    ]
