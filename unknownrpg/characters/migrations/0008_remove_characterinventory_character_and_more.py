# Generated by Django 4.0.2 on 2022-02-26 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0007_characterinventory_unique_character_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='characterinventory',
            name='character',
        ),
        migrations.RemoveField(
            model_name='characterinventory',
            name='item',
        ),
        migrations.RemoveField(
            model_name='character',
            name='equipment',
        ),
        migrations.RemoveField(
            model_name='character',
            name='inventory',
        ),
        migrations.DeleteModel(
            name='CharacterEquipment',
        ),
        migrations.DeleteModel(
            name='CharacterInventory',
        ),
    ]
