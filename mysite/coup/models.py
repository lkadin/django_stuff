from django.db import models
from django.db.models import Max
import random

class ActionHistory(models.Model):
    name = models.CharField(max_length=20, default="Assassinate")
    tran_date=models.DateTimeField(auto_now_add=True, blank=True)
    player1 = models.CharField(max_length=20, default="Lee")
    player2 = models.CharField(max_length=20, default="Lee")

class Action(models.Model):
    name = models.CharField(max_length=20, default="Assassinate")
    player2_required=models.BooleanField(default=False)


    def __str__(self):
        return self.name

    def action(self,player,player2=None):
        game=Game.objects.all()[0]
        self.player=player
        self.player2=player2
        game.current_action = self.name
        game.current_player1=self.player.playerName
        game.save()
        self.redo=False
        if self.name == "Income":
            player.addCoins(1)
        elif self.name == "Foreign Aid":
            player.addCoins(2)
        elif self.name == "Take 3 coins":
            player.addCoins(3)
        elif self.name == "Steal":
            self.steal(self.player)
        elif self.name == 'Assassinate':
            if player.coins<3:
                self.redo = "You don't have enough coins"
            else:
                player.loseCoins(3)
        elif self.name == "Draw":
            self.draw(player)
        elif self.name == 'Coup':
            if player.coins<7:
                self.redo = "You don't have enough coins"
            else:
                pass
                # player.loseCoins(7)
        elif self.name == 'Challenge':  # assassinate and steal??
            pass
        player.save()
        if not self.redo:
            actionhistory=ActionHistory(name=self.name,player1=player.playerName)
            actionhistory.save()
        return self.redo



class Card(models.Model):
    cardName = models.CharField(max_length=20, default="Assassin")

    # status = models.BooleanField(default=True)

    def __str__(self):
        return self.cardName

class CardInstance(models.Model):
    import uuid
    """
    Model representing a specific card 
    """

    card = models.ForeignKey('Card', on_delete=models.SET_NULL, null=True)
    shuffle_order = models.IntegerField(null=True)

    def __str__(self):
        return (self.card.cardName)

    CARD_STATUS = (
        ('U', 'Up'),
        ('D', 'Down'),
    )
    status = models.CharField(max_length=1, choices=CARD_STATUS, blank=True, default='D', help_text='Card status')


class Player(models.Model):
    playerName = models.CharField(max_length=20, default="Lee")
    playerNumber = models.IntegerField(default=0)
    coins = models.IntegerField(default=2)
    hand = models.ManyToManyField(CardInstance)

    def __str__(self):
        return self.playerName

    def addCoins(self, numCoins):
        self.coins += numCoins

    def loseCoins(self, numCoins):
        self.coins -= numCoins

    def influence(self):
        cnt = 0
        for card in self.hand.all():
            if card.status == "D":
                cnt += 1
        return cnt

class Deck(models.Model):
    cards = models.ManyToManyField(CardInstance)

    def __str__(self):
        return ("Deck")

    def build(self):
        cis = CardInstance.objects.all()
        for ci in cis:
            ci.save()
            self.cards.add(ci)
    def shuffle(self):
        for i in range(self.cards.count() - 1, -1, -1):
            r = random.randint(0, i)
            self.card1=self.cards.filter(shuffle_order=i)[0]
            self.card2=self.cards.filter(shuffle_order=r)[0]
            self.card1.shuffle_order,self.card2.shuffle_order=self.card2.shuffle_order,self.card1.shuffle_order
            self.card1.save()
            self.card2.save()

    def drawCard(self):
        self.maxcard=CardInstance.objects.all().aggregate(Max('shuffle_order'))
        self.max=self.maxcard['shuffle_order__max']
        self.draw=CardInstance.objects.get(shuffle_order=self.max)
        self.draw.shuffle_order=None
        self.cards.remove(self.draw)
        self.draw.save()
        return self.draw
class Game(models.Model):
    NUM_OF_CARDS = models.IntegerField(default=2)
    whoseTurn = models.IntegerField(default=0)
    current_action = models.CharField(max_length=20,null=True,blank=True)
    current_player1 = models.CharField(max_length=20,null=True,blank=True)
    current_player2 = models.CharField(max_length=20,null=True,blank=True)

    def del_card_instances(self):
        CardInstance.objects.all().delete()

    def build_cards(self):
        self.order = 0
        for card in Card.objects.all():
            for _ in range(3):

                card.cardinstance_set.create(shuffle_order=self.order)
                self.order += 1
                card.save()

    def initialize(self):
        ActionHistory.objects.all().delete()
        self.del_card_instances()
        self.build_cards()
        deck = Deck(id=1)
        deck.save()
        deck.build()
        deck.shuffle()
        deck.save()
        Player.objects.all().delete()
        self.add_all_players() #########################This will be replaced by login
        self.initialDeal()


    def initialDeal(self):
        self.deck = Deck.objects.all()[0]
        self.deck.shuffle()
        self.deck.save()
        players=Player.objects.all()
        for i in range(self.NUM_OF_CARDS):
            for player in players:
                player.hand.add(self.deck.drawCard())
                self.deck.save()

    def add_all_players(self):
        player=Player(playerName="Lee",playerNumber=0)
        player.save()
        player=Player(playerName="Adina",playerNumber=1)
        player.save()
        player=Player(playerName="Sam",playerNumber=2)
        player.save()
        player=Player(playerName="Jamie",playerNumber=3)
        player.save()

    def nextTurn(self):
        self.whoseTurn=(self.whoseTurn+1) % 4

    def currentPlayerName(self):
        self.players=[self.player for self.player in Player.objects.all()]
        return self.players[self.whoseTurn].playerName

    def ck_winner(self):
        self.players = Player.objects.all()
        count = 0
        for self.player in self.players:
            if self.player.influence() > 0:
                count += 1
                self.winner = self.player.playerName
        if count == 1:
            # self.message("Game over - {} wins".format(winner))
            return self.winner
    def getPlayerFromPlayerName(self,playerName):
        return Player.objects.get(playerName=playerName)

    def clearCurrent(self):
        self.current_action=None
        self.current_player1=None
        self.current_player2=None
