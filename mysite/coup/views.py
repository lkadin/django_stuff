from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Player, Card, Deck, Action, Game, CardInstance, ActionHistory
from django.contrib.auth.mixins import LoginRequiredMixin
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


def startGame(request):
    game = Game.objects.get(id=80)
    game.initialize()
    game.clearCurrent()
    game.whoseTurn = random.randint(0, 3)
    game.save()
    Deck.objects.all().delete()
    deck = Deck(id=1)
    deck.save()
    deck.build()
    players = Player.objects.all()
    game = Game.objects.all()
    actions = Action.objects.all()
    return redirect(showTable)
    # request,
    # 'table.html',
    # context={'players': players,'actions':actions,'game':game}
    # )


def showTable(request):
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


def showDeck(request):
    deck = Deck.objects.all()[0]
    cardsremaining=deck.cardsremaining()
    return render(
        request,
        'show_deck.html',
        context={'deck': deck,'cardsremaining':cardsremaining}
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


def actions(request):
    players = Player.objects.all()
    game = Game.objects.all()[0]
    action=game.current_action
    if request.method == 'GET':
        playerName = request.GET.get('playerName', None)
        player = Player.objects.get(playerName=playerName)
        action = request.GET.get('action', None)
        player2=None
        game.current_player1 = player.playerName
        game.save()

    if request.method == 'POST':
        try:
            playerName2 = request.POST.get('name')
            playerName1 = game.current_player1
            player = Player.objects.get(playerName=playerName1)
            player2 = Player.objects.get(playerName=playerName2)
            player_required = False
            game.current_player2 = player2.playerName
            game.save()
        except:
            pass
        try:
            discards=(request.POST.getlist('cardnames'))
            for discard in discards:
                player.discard(discard)
                player.save()
                game.nextTurn()
                game.clearCurrent()
                game.save()
            return redirect(showTable)
            # return render(request, 'discard_result.html', {'action': action,'discard':discard,'player':player})
        except:
            pass
        player = game.getPlayerFromPlayerName(game.current_player1)
        playerName = player.playerName

    if request.user.username != playerName:
        return render(request, 'not_your_turn.html', {'action': action})

    nextAction = Action.objects.get(name=action)
    player_required = nextAction.player2_required

    if player_required and player2==None:
        return render(request, 'player.html', {'players': players, 'action': action})
    else:
        player2=None

    redo = nextAction.action(player, player2)
    if player.cardcount()>2:
        return  render(request, 'discard.html',{'player': player, 'action': action,'cards':player.hand.all()})
        player.save()
    if not redo :
        game.nextTurn()
        game.clearCurrent()
        game.save()
        return redirect(showTable)
    else:
        return render(request, 'redo.html', {'redo': redo})
