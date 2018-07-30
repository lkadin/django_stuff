from .models import Player, Card, Deck, Action, Game, CardInstance, ActionHistory

def get_initial_action_data(request):

    if request.method == 'GET':
        playerName = request.GET.get('playerName', None)
        player = Player.objects.get(playerName=playerName)
        action = request.GET.get('action', None)
        game = Game.objects.all()[0]
        if action=='Draw':
            game.discardRequired=True
        game.current_player1 = player.playerName
        game.current_action=action
        game.redo=False
        game.redoMessage=None
        game.save()

    if request.method == 'POST':
        # redoMessage=None
        # if checkTurn(request):
        #     return
        game = Game.objects.all()[0]
        action = Action.objects.get(name=game.current_action)
        actionName=action.name
        if action.player2_required:
        # get second player name
            playerName2 = request.POST.get('name')
            playerName1 = game.current_player1
            player = Player.objects.get(playerName=playerName1)
            player2 = Player.objects.get(playerName=playerName2)
            game.current_player2 = player2.playerName
            game.save()
            return

        elif actionName == 'Draw': #get discard
            player = game.getPlayerFromPlayerName(game.current_player1)
            discards=(request.POST.getlist('cardnames'))
            for discard in discards:
                player.discard(discard)
                player.save()
                # game.clearCurrent()
                game.redo=False
                game.redoMessage=None
                game.save()
            # return redirect(showTable)
            return

    actionName = game.current_action
    action = Action.objects.get(name=actionName)
    game.redoMessage = action.action(player)

    # if game.redoMessage:
    #     game.redo=True
    #     game.save()
    # else:
    #     game.nextTurn()
    #     game.save()

    return

def checkTurn(request):
    game=Game.objects.all()[0]

    playerName=Player.objects.get(playerNumber=game.whoseTurn).playerName
    if request.user.username == playerName:
        # game.redoMessage=None
        # game.redo=False
        # game.save()
        return True
    else:
        # game.redoMessage = "Not your turn"
        # game.redo=True
        # game.save()
        return False

def playerRequired():
    game=Game.objects.all()[0]
    action=game.current_action
    nextAction = Action.objects.get(name=action)
    return  nextAction.player2_required

def discardRequired():
    game = Game.objects.all()[0]
    player=game.getPlayerFromPlayerName(game.current_player1)
    if player.cardcount()>2:
        return game.discardRequired



