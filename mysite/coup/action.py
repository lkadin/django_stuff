from .models import Player, Card, Deck, Action, Game, CardInstance, ActionHistory


def take_action(request):
    game = Game.objects.all()[0]
    action = Action.objects.get(name=game.current_action)
    player1 = Player.objects.get(playerName=game.current_player1)

    if action.pending_required:
        game.pending_action = True
        game.save()

    game = Game.objects.all()[0]

    if game.current_action == "Income":
        player1.addCoins(1)
    elif game.current_action == "Foreign Aid":
        player1.addCoins(2)
    elif game.current_action == "Take 3 coins":
        player1.addCoins(3)
    elif game.current_action == "Block":
        game.clearCurrent()
        game.save()
        return
    elif game.current_action == 'Challenge':
        if not game.challenge_in_progress:
            game.challenge()
        else:
            return


    elif game.current_action == 'Allow Steal':
        player2 = Player.objects.get(playerName=game.current_player2)
        player1.addCoins(2)
        player1.save()
        player2.loseCoins(2)
        player2.save()
        game.clearCurrent()
        game.save()
        return

    # elif game.current_action in ('Assassinate', 'Coup', 'Steal'):
    elif action.player2_required:

        if request.method == 'GET':
            return

        playerName2 = game.current_player2
        if not playerName2:
            playerName2 = request.POST.get('name', None)
            game.player2_turn = True
            game.current_player2 = playerName2
            game.save()


    elif game.current_action == "Draw":
        if not game.discardRequired():
            player1 = Player.objects.get(playerName=game.current_player1)
            player1.draw()
            player1.save()
            game.pending_action = True
            game.save()
            return
        else:
            discards = request.POST.getlist('cardnames', None)
            if discards:
                game.discard_cards(discards)
                game.pending_action = False
                game.save()
                return
    player1.save()
    actionhistory = ActionHistory(name=action.name, player1=player1.playerName, player2=game.current_player2)
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
    if actionName == 'Challenge' and request.user.username:
        playerName1 = request.user.username

    game = Game.objects.all()[0]
    game.current_player1 = playerName1
    game.current_action = actionName
    game.save()
    return


def finish_lose_influence(request):
    game = Game.objects.all()[0]
    action = Action.objects.get(name=game.current_action)
    prior_action_name, prior_player_name = game.get_prior_action_info()
    if prior_action_name != 'Challenge':
        player1 = game.getPlayerFromPlayerName(game.current_player1)
        player1.loseCoins(action.coins_required)
        player1.save()
    cardName = request.POST.get('cardnames', None)
    player2 = game.getPlayerFromPlayerName(game.current_player2)
    player2.lose_influence(cardName)
    player2.save()
    game.clearCurrent()
    game.nextTurn()
    game.save()
    return
