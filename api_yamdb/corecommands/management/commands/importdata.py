from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import csv
from yamdb.models import (User, Title, Genre, Category, TitleGenre,
                          Review, Comment)

DATA = {
    User: 'users.csv',
    Category: 'category.csv',
    Comment: 'comments.csv',
    Review: 'review.csv',
    Genre: 'genre.csv',
    TitleGenre: 'genre_title.csv',
    Title: 'titles.csv'
}


class Command(BaseCommand):
    help = (f'Команда предназначена для импорта данных из csv файлов в базу '
            f'данных. Во всех путях стоит указывать "/" вместо "\\".')

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default=f'static/data/',
            help='Указывается путь относительно вашей '
                 'BASE_DIR, по умолчанию static/data/')
        parser.add_argument('--full_path',
                            type=str,
                            help='Указывается полный путь к директории '
                                 'с CSV файлами.')
        pass

    def handle(self, *args, **options):
        for model, data_sheet in DATA.items():
            if options['full_path']:
                path = f'{options["full_path"]}/{data_sheet}'
                path.replace('\\', '/')
                print(path)
            else:
                path = settings.BASE_DIR / f'{options["path"]}{data_sheet}'
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    clear_data = []
                    for i in reader:
                        del i['id']
                        clear_data.append(i)
                    model.objects.bulk_create(model(**data) for data in
                                              clear_data)
                    print(clear_data)
                    self.stdout.write(self.style.SUCCESS('Импорт выполнен.'))
            except FileNotFoundError:
                raise CommandError('Не найден файл или неверно указан путь.')
