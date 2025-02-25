# Generated by Django 5.0.6 on 2024-05-17 09:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='ФИО')),
                ('dob', models.DateField(verbose_name='Дата рождения')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('code', models.CharField(max_length=31, primary_key=True, serialize=False, unique=True, verbose_name='Код')),
                ('name', models.CharField(verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Источник',
                'verbose_name_plural': 'Источники',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('code', models.CharField(max_length=31, primary_key=True, serialize=False, unique=True, verbose_name='Код')),
                ('name', models.CharField(verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='AuthorInfo',
            fields=[
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='info', serialize=False, to='articles.author', verbose_name='Автор')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=31, null=True, verbose_name='Phone')),
            ],
            options={
                'verbose_name': 'Инфо об авторе',
                'verbose_name_plural': 'Инфо об авторе',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.TextField(verbose_name='Название статьи')),
                ('text', models.TextField(verbose_name='Содержание стати')),
                ('publish_date', models.DateField(blank=True, null=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='articles.author', verbose_name='Автор')),
                ('tags', models.ManyToManyField(related_name='articles', to='articles.tag')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField(verbose_name='Оценка')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='articles.article', verbose_name='Статья')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ratings', to='articles.source', verbose_name='Источник')),
            ],
            options={
                'verbose_name': 'Оценка к статьям',
                'verbose_name_plural': 'Оценки к статьям',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='articles.article', verbose_name='Статья')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='comments', to='articles.source', verbose_name='Источник')),
            ],
            options={
                'verbose_name': 'Комментарий к статьям',
                'verbose_name_plural': 'Комментарии к статьям',
            },
        ),
    ]
