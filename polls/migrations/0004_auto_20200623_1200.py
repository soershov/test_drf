# Generated by Django 3.0.6 on 2020-06-23 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('polls', '0003_auto_20200623_0042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ques',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('question_type', models.IntegerField()),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Poll')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_polls.ques_set+', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
        migrations.CreateModel(
            name='ChoicesQuestion',
            fields=[
                ('ques_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polls.Ques')),
            ],
            options={
                'verbose_name': 'ChoicesQuestion',
            },
            bases=('polls.ques',),
        ),
        migrations.CreateModel(
            name='TextQuestion',
            fields=[
                ('ques_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polls.Ques')),
                ('question_text', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('polls.ques',),
        ),
        migrations.CreateModel(
            name='YesNoQuestion',
            fields=[
                ('ques_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polls.Ques')),
                ('yes_no', models.BooleanField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('polls.ques',),
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.ChoicesQuestion'),
        ),
    ]
