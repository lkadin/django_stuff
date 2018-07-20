from django.db import models
from django.db.models import Max
import random


class Action(models.Model):
    name = models.CharField(max_length=20, default="Assassinate")

    def __str__(self):
        return self.name


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
        for card in self.hand:
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
            self.card1.shuffle_order,self.card1.shuffle_order=self.card2.shuffle_order,self.card1.shuffle_order

    def drawCard(self):
        self.maxcard=CardInstance.objects.all().aggregate(Max('shuffle_order'))
        self.max=self.maxcard['shuffle_order__max']
        self.draw=CardInstance.objects.get(shuffle_order=self.max)
        self.draw.shuffle_order=None
        self.cards.remove(self.draw)
        self.draw.save()
        # self.cards.save()
        return self.draw
class Game(models.Model):
    NUM_OF_CARDS = models.IntegerField(default=2)
    whoseTurn = models.IntegerField(default=0)

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
        self.del_card_instances()
        self.build_cards()

        # deck = Deck.objects.get(id=1)
        deck = Deck(id=1)
        deck.save()
        deck.build()
        deck.shuffle()
        deck.save()
        Player.objects.all().delete()
        self.add_all_players() #########################This will be replaced by login
        self.initialDeal()


    def initialDeal(self):
        self.deck = Deck.objects.get(id=1)
        # self.deck = Deck(id=1)
        self.deck.shuffle()
        self.deck.save()
        players=Player.objects.all()
        for i in range(self.NUM_OF_CARDS):
            for player in players:
                player.hand.add(self.deck.drawCard())

    def add_all_players(self):
        player=Player(playerName="Lee",playerNumber=0)
        player.save()
        player=Player(playerName="Adina",playerNumber=1)
        player.save()
        player=Player(playerName="Sam",playerNumber=2)
        player.save()
        player=Player(playerName="Jamie",playerNumber=3)
        player.save()