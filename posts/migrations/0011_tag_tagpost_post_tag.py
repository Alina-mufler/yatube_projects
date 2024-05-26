# Generated by Django 4.2.5 on 2024-02-06 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_remove_post_pub_date_post_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('name', models.TextField(verbose_name='Наименование хэштега')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TagPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(through='posts.TagPost', to='posts.tag'),
        ),
    ]