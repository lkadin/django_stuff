from .models import Player, Card, Deck, Action, Game, CardInstance, ActionHistory


def take_action(request):

    game = Game.objects.all()[0]
    action = Action.objects.get(name=game.current_action)
    player1 = Player.objects.get(playerName=game.current_player1)

    if game.current_action in ("Draw", "Assassinate", "Coup"):
        game.pending_action = True
        game.save()

    game = Game.objects.all()[0]

    if game.current_action == "Income":
        player1.addCoins(1)
    elif game.current_action == "Foreign Aid":
        player1.addCoins(2)
    elif game.current_action == "Take 3 coins":
        player1.addCoins(3)
    elif game.current_action == "Steal":
        pass
    elif game.current_action == 'Assassinate':

        if request.method == 'GET':
            return
        playerName2 = game.current_player2
        if not playerName2:
            playerName2 = request.POST.get('name', None)
            game.player2_turn = True
            game.current_player2 = playerName2
            game.save()
            return



    elif game.current_action == "Draw":

        if not game.discardRequired():

            player1 = Player.objects.get(playerName=game.current_player1)
            print("preparing to draw")
            player1.draw()
            player1.save()
            game.pending_action = True
            game.save()
            return
        else:
            discards = request.POST.getlist('cardnames', None)
            print("dicsrads = {}".format(discards))
            if discards:
                try:
                    print("prepaaring to discard")
                    game.discard_cards(discards)
                    game.pending_action = False
                    game.save()
                    return
                except:
                    game.redoMessage = "Could not discard"
                    game.pending_action = True
                    game.save()
                    return
    player1.save()
    actionhistory = ActionHistory(name=action.name, player1=player1.playerName)
    actionhistory.save()
    game.save()
    return

def get_initial_action_data(request):
    if request.method == 'GET':
        getrequest(request)
    take_action(request)
    return

def getrequest(request):
    playerName1 = request.GET.get('playerName', None)
    actionName = request.GET.get('action', None)
    game = Game.objects.all()[0]
    game.current_player1 = playerName1
    game.current_action = actionName
    game.save()
    return


def finish_lose_influence(request):
    game = Game.objects.all()[0]
    player1 = game.getPlayerFromPlayerName(game.current_player1)
    player1.loseCoins(3)
    player1.save()
    cardName = request.POST.get('cardnames', None)
    player2 = game.getPlayerFromPlayerName(game.current_player2)
    print("Player {} is losing card {}".format(player2, cardName))
    player2.lose_influence(cardName)
    player2.save()
    game.clearCurrent()
    game.pending_action = False
    game.save()
    return
