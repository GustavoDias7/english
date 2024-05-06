from peewee import *

db = SqliteDatabase('database.db')

class Card(Model):
    text = CharField(unique=True)
    translation = CharField()
    path_audio = CharField()
    is_anki = BooleanField(default=False)

    class Meta:
        database = db

db.create_tables([Card])