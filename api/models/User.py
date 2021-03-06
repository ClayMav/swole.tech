"""All registered users are input into this model"""

from models import BaseModel
from playhouse.postgres_ext import CharField


class User(BaseModel):
    name = CharField(unique=True, primary_key=True)
    photo = CharField(null=True)
