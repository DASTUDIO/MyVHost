# Generated by Django 3.1.5 on 2021-01-11 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pub', '0002_auto_20190806_2219'),
    ]

    operations = [
        migrations.CreateModel(
            name='notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='template_info',
            fields=[
                ('key', models.TextField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('brief', models.TextField()),
                ('headimg', models.TextField()),
                ('default', models.TextField()),
                ('created', models.IntegerField()),
                ('modified', models.IntegerField()),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='user_comments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('userid', models.IntegerField()),
                ('publisherid', models.IntegerField()),
                ('content', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('created', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='user_comments_likes_map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_id', models.IntegerField()),
                ('publisher', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(unique=True)),
                ('position', models.TextField()),
                ('active', models.IntegerField()),
                ('friend_url', models.TextField()),
                ('brief', models.TextField()),
                ('real_name', models.TextField()),
                ('id_code', models.TextField()),
                ('phone', models.TextField()),
                ('email', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='resource_info',
            options={'ordering': ('-created',)},
        ),
        migrations.RemoveField(
            model_name='resource_permission',
            name='permitteduser',
        ),
        migrations.RemoveField(
            model_name='resource_restful',
            name='modifiable',
        ),
        migrations.RemoveField(
            model_name='resource_restful',
            name='readable',
        ),
        migrations.RemoveField(
            model_name='resource_restful',
            name='writeable',
        ),
    ]
