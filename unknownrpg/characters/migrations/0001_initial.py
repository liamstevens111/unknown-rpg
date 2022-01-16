# Generated by Django 4.0.1 on 2022-01-16 03:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('level', models.IntegerField()),
                ('gold', models.IntegerField()),
                ('current_hp', models.IntegerField()),
                ('current_xp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CharacterInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.character')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.item')),
            ],
            options={
                'verbose_name_plural': 'Character Inventory',
            },
        ),
        migrations.CreateModel(
            name='CharacterEquipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(choices=[('weapon', 'Weapon'), ('armour', 'Armour'), ('helmet', 'Helmet'), ('necklace', 'Necklace'), ('bracelet', 'Bracelet'), ('ring', 'Ring')], max_length=20, verbose_name='slot')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.character')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.item')),
            ],
            options={
                'verbose_name_plural': 'Character Equipment',
                'unique_together': {('character', 'slot')},
            },
        ),
        migrations.AddField(
            model_name='character',
            name='equipment',
            field=models.ManyToManyField(related_name='equipment_character', through='characters.CharacterEquipment', to='items.Item'),
        ),
        migrations.AddField(
            model_name='character',
            name='inventory',
            field=models.ManyToManyField(related_name='inventory_character', through='characters.CharacterInventory', to='items.Item'),
        ),
        migrations.AddField(
            model_name='character',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
