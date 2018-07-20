from django.http import HttpResponse
from django.shortcuts import render
from .models import Player, Card, Deck, Action, Game, CardInstance
from django.contrib.auth.mixins import LoginRequiredMixin
import random


def index(request):
    players = Player.objects.all()
    try:
        names = [player.playerName for player in players]
    except:
        names=[]
    if len(players) <=4 :
        if request.user.username not in names and request.user.username:
            player=Player(playerName=request.user.username)
            player.save()
        return render(
            request,
            'login_screen.html',
            context={'players': players})
    else:
        return render(
            request,
            'no_more.html')


def startGame(request):
    game = Game.objects.get(id=80)
    game.initialize()
    game.whoseTurn = random.randint(0, 4)
    game.save()
    Deck.objects.all().delete()
    deck=Deck(id=1)
    deck.save()
    deck.build()
    players = Player.objects.all()
    game = Game.objects.all()
    return render(
        request,
        'table.html',
        context={'players': players,'game':game}
    )

def showTable(request):
    players = Player.objects.all()
    actions = Action.objects.all()
    game=Game.objects.all()[0]
    return render(
        request,
        'table.html',
        context={'players': players,'actions':actions,'game':game}
    )

def showDeck(request):
    decks = Deck.objects.all()[0]
    return render(
        request,
        'show_deck.html',
        context={'decks': decks}
    )

def initialDeal(request):
    game = Game.objects.get(id=80)
    players = Player.objects.all()
    game.initialDeal()
    return render(
        request,
        'table.html',
        context={'players': players}
    )

def shuffle(request):
    deck = Deck.objects.get(id=210)
    # deck=decks[0]
    deck.shuffle()
    deck.save()
    return render(
        request,
        'show_deck.html',
        context={'deck': deck}
    )