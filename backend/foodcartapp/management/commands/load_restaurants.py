import sys
import time

import requests
from django.core.exceptions import MultipleObjectsReturned
from django.core.management.base import BaseCommand

from foodcartapp.models import Restaurant


class Command(BaseCommand):
    help = 'Скачивание ресторанов по url'

    def add_arguments(self, parser):
        parser.add_argument(
            'url',
            nargs='+',
            type=str,
            help='Список url адресов для загрузки данных'
        )

    def handle(self, *args, **options):
        urls = options['url']
        time_out = 5
        for url in urls:
            try:
                response = requests.get(url, timeout=time_out)
                response.raise_for_status()
                raw_place = response.json()
                for obj in raw_place:
                    restaurant, created = Restaurant.objects.get_or_create(
                        name=obj['title'],
                        address=obj['address'],
                        contact_phone=obj['contact_phone'],
                    )

                    if not created:
                        print('Место уже имеется')
                        continue
                    self.stdout.write(self.style.SUCCESS(f"Добавлен: {restaurant}"))

            except MultipleObjectsReturned:
                print('Найдено несколько мест')
            except requests.exceptions.ConnectionError:
                print(
                    'Соединение прервано. Скрипт продолжает работу',
                    file=sys.stderr
                )
                time.sleep(20)
            except requests.exceptions.HTTPError as error:
                print(
                    f'Не корректно введен url: {error}',
                    file=sys.stderr
                )
                continue
            except requests.exceptions.ReadTimeout:
                continue
