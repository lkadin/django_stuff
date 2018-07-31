from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Player, Card, Deck, Action, Game, CardInstance, ActionHistory
from django.contrib.auth.mixins import LoginRequiredMixin
from .action import get_initial_action_data, checkTurn, playerRequired, discardRequired
import random


def index(request):
    players = Player.objects.all()
    try:
        names = [player.playerName for player in players]
    except:
        names = []
    if len(players) <= 4:
        if request.user.username not in names and request.user.username:
            player = Player(playerName=request.user.username)
            player.save()
        return render(
            request,
            'login_screen.html',
            context={'players': players})
    else:
        return render(
            request,
            'no_more.html')


def startgame():
    game = Game.objects.get(id=80)
    game.initialize()
    game.clearCurrent()
    game.whoseTurn = random.randint(0, 3)
    game.save()
    Deck.objects.all().delete()
    deck = Deck(id=1)
    deck.save()
    deck.build()
    # players = Player.objects.all()
    # game = Game.objects.all()
    # actions = Action.objects.all()
    return redirect(showtable)
    # request,
    # 'table.html',
    # context={'players': players,'actions':actions,'game':game}
    # )


def showtable(request):
    players = Player.objects.all()
    actions = Action.objects.all()
    actionhistory = ActionHistory.objects.all().order_by('-id')[:4]
    game = Game.objects.all()[0]
    if not game.ck_winner():
        return render(
            request,
            'table.html',
            context={'players': players, 'actions': actions, 'game': game,
                     'current_player_name': game.currentPlayerName(), 'actionhistory': actionhistory}
        )
    else:
        return render(
            request,
            'game_over.html',
            context={'players': players, 'actions': actions, 'game': game, 'winner': game.ck_winner()}
        )


def showdeck(request):
    deck = Deck.objects.all()[0]
    cardsremaining = deck.cardsremaining()
    return render(
        request,
        'show_deck.html',
        context={'deck': deck, 'cardsremaining': cardsremaining}
    )


def initialdeal(request):
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


def actions(request):

    # checkTurn(request)
    game = Game.objects.all()[0]
    if not checkTurn(request):
        return render(request, 'redo.html', {'redo': "Not your turn"})

    get_initial_action_data(request)

    if playerRequired():
        players = Player.objects.all()
        return render(request, 'player.html', {'players': players})
    elif discardRequired():
        game = Game.objects.all()[0]
        player = game.getPlayerFromPlayerName(game.current_player1)
        return render(request, 'discard.html', {'player': player, 'cards': player.hand.all()})
    if game.redoMessage is None:
            game.nextTurn()
            game.clearCurrent()
            game.save()
            return redirect(showtable)
