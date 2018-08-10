from django.db import models
from django.db.models import Max
import random

class Function(models.Model):
    methodName = models.CharField(max_length=20,blank=True,null=True)
    arguments = models.TextField()
    action = models.ForeignKey("Action",on_delete=models.CASCADE,default=0)

class ActionHistory(models.Model):
    name = models.CharField(max_length=20, default="Assassinate")
    tran_date=models.DateTimeField(auto_now_add=True, blank=True)
    player1 = models.CharField(max_length=20, default="Lee")
    player2 = models.CharField(max_length=20, default="Lee")

class Action(models.Model):
    name = models.CharField(max_length=20, default="Assassinate")
    player2_required=models.BooleanField(default=False)
    coins_required = models.IntegerField(default=0)
    def __str__(self):
        return self.name




class Card(models.Model):
    cardName = models.CharField(max_length=20, default="Assassin")

    # status = models.BooleanField(default=True)

    def __str__(self):
        return self.cardName

class CardInstance(models.Model):
    # import uuid
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
    def draw(self):
        if len(self.hand.all())<4:
            self.deck = Deck.objects.all()[0]
            self.hand.add(self.deck.drawCard())
            self.hand.add(self.deck.drawCard())
            self.save()

    def discard(self,cardname):
        self.cardname=cardname
        self.card_id=Card.objects.filter(cardName=cardname)[0].id
        self.card=self.hand.filter(card_id=self.card_id)[0]
        self.deck = Deck.objects.all()[0]
        self.deck.returnCard(self.card)
        self.hand.remove(self.card)
        self.deck.save()
        self.save()

    def cardcount(self):
        return len(self.hand.all())

    def lose_influence(self, cardname):
        self.cardname = cardname
        self.card_id = Card.objects.filter(cardName=cardname)[0].id
        self.card = self.hand.filter(card_id=self.card_id)[0]
        self.card.status = 'U'
        self.card.save()
        self.save()

class Deck(models.Model):
    cards = models.ManyToManyField(CardInstance)

    def __str__(self):
        return ("Deck")

    def cardsremaining(self):
        self.cnt=0
        for self.card in self.cards.all():
            if self.card.shuffle_order != None:
                self.cnt+=1
        return self.cnt

    def cardsavailable(self):
        self.cardsavail=[]
        for self.card in self.cards.all():
            if self.card.shuffle_order != None:
                self.cardsavail.append(self.card)
        return self.cardsavail

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
        self.card=CardInstance.objects.get(shuffle_order=self.max)
        self.card.shuffle_order=None
        self.card.save()
        return self.card

    def returnCard(self,card):
        self.card=card
        self.maxcard = CardInstance.objects.all().aggregate(Max('shuffle_order'))
        self.max=self.maxcard['shuffle_order__max']+1
        self.card.shuffle_order=self.max
        self.card.save()


class Game(models.Model):
    NUM_OF_CARDS = models.IntegerField(default=2)
    whoseTurn = models.IntegerField(default=0)
    current_action = models.CharField(max_length=20,null=True,blank=True)
    current_player1 = models.CharField(max_length=20,null=True,blank=True)
    current_player2 = models.CharField(max_length=20,null=True,blank=True)
    redoMessage = models.CharField(max_length=30,blank=True,null=True)
    pending_action = models.BooleanField(default=False)

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
            return self.winner

    def clearCurrent(self):
        self.current_action=None
        self.current_player1=None
        self.current_player2=None
        self.pending_action = False
        # self.save()

    def getPlayerFromPlayerName(self,playerName):
        return Player.objects.get(playerName=playerName)

    def discard_cards(self,cards):
        player=Player.objects.get(playerName=self.current_player1)
        for card in cards:
            player.discard(card)
            player.save()
        # self.save()

    def discardRequired(self):
        player = self.getPlayerFromPlayerName(self.current_player1)
        if player.cardcount() > 2:
            return True
        else:
            return False

    def playerRequired(self):
        if self.current_player2:
            return
        actionName = self.current_action
        action = Action.objects.get(name=actionName)
        return action.player2_required
