from django.contrib import admin

# Register your models here.
from .models import Player, Card, Action, Deck, Game, CardInstance

admin.site.register(Player)
admin.site.register(Card)
admin.site.register(Action)
admin.site.register(Deck)
admin.site.register(Game)
admin.site.register(CardInstance)
