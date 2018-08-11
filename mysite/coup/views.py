# from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Player, Card, Deck, Action, Game, CardInstance, ActionHistory
# from django.contrib.auth.mixins import LoginRequiredMixin
from .action import get_initial_action_data
import random


def index(request):
    players = Player.objects.all()
    # try:
    names = [player.playerName for player in players]
    # except:
    #     names = []
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


def startgame(request):
    game = Game(id=1)
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
    cards = []
    current_player_coins = players.get(playerNumber=game.whoseTurn).coins
    for player in players:
        for card in player.hand.all():
            cards.append(card)
    if not game.ck_winner():
        return render(
            request,
            'table.html',
            context={'players': players, 'actions': actions, 'game': game,
                     'current_player_name': game.currentPlayerName(), 'actionhistory': actionhistory, 'cards': cards,
                     'current_player_coins': current_player_coins}
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

    get_initial_action_data(request)

    game = Game.objects.all()[0]
    if not game.pending_action:
        game.nextTurn()
        game.clearCurrent()
        game.save()
        return redirect(showtable)
    else:
        get_initial_action_data(request)

        if game.discardRequired():
            player = game.getPlayerFromPlayerName(game.current_player1)
            return render(request, 'discard.html', {'player': player, 'cards': player.hand.all()})

        if game.playerRequired():
            players = Player.objects.all()
            return render(request, 'player.html', {'players': players})

        if game.lose_influence_required:
            player = game.getPlayerFromPlayerName(game.current_player2)
            return render(request, 'lose_influence.html', {'player': player, 'cards': player.hand.all()})
