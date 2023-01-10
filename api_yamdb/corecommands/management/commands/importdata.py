import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenre, User)

DATA = {
    User: 'users.csv',
    Genre: 'genre.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    TitleGenre: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = ('Команда предназначена для импорта данных из csv файлов в базу '
            'данных. Во всех путях стоит указывать "/" вместо "\\".')

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default='static/data/',
            help='Указывается путь относительно вашей '
                 'BASE_DIR, по умолчанию static/data/')
        parser.add_argument('--full_path',
                            type=str,
                            help='Указывается полный путь к директории '
                                 'с CSV файлами.')

    def handle(self, *args, **options):
        for model, data_sheet in DATA.items():
            if options['full_path']:
                path = f'{options["full_path"]}/{data_sheet}'
                path.replace('\\', '/')
            else:
                path = settings.BASE_DIR / f'{options["path"]}{data_sheet}'
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    clear_data = {}
                    for i in csv.DictReader(f):
                        for k, v in i.items():
                            if k == 'author':
                                clear_data[k] = User.objects.get(id=int(v))
                            elif k == 'category':
                                clear_data[k] = Category.objects.get(id=int(v))
                            else:
                                clear_data[k] = v
                        model.objects.get_or_create(**clear_data)
                        self.stdout.write(f'{clear_data}=='
                                          f'{self.style.SUCCESS("OK")}')
            except FileNotFoundError:
                raise CommandError('Не найден файл или неверно указан путь.')
        self.stdout.write(self.style.SUCCESS('Импорт выполнен.'))
