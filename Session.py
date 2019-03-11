from Card import Card
from Player import Player
from random import shuffle, randint
import time

class Session(object):
    def __init__(self, special_card=False):
        self.card_pile = [Card(i) for i in range(1, 12)]
        shuffle(self.card_pile)
        players = [Player(self, i) for i in range(2)]
        players[0].next = players[1]
        players[1].next = players[0]
        
        AI_index = randint(0, 1)
        # players[AI_index].AI = True
        # print('You are ', players[not AI_index])
        players[0].AI = True
        players[1].AI = True
        self.players = players
        self.init_cards()

    def init_cards(self):
        for p in self.players:
            basecard = self.card_pile.pop()
            p.set_basecard(basecard)
            p.draw(print_cards=False)

    def game_loop(self):
        def wait(t=5):
            time.sleep(t)
        def _ask(p):
            if p.AI:
                wait()
                return p.AI_judge()
            else:
                return p.player_judge()
            return res.upper()
        
        last_stay = False
        p = self.players[0]
        while True:
            print(p, '的回合')
            self.players[0].print_cards(self.players[0].AI)
            self.players[1].print_cards(self.players[1].AI)
            print()

            res = _ask(p)
            while not len(res) or res[0] not in ['D', 'S']:
                res = _ask(p)
            res = res[0]
            if res == 'D':
                print(p, ': Give me another')
                p.draw()
                last_stay = False
            else:
                print(p, ': I\'ll stay' )
                if last_stay: break
                else: last_stay = True
            if p.AI: wait(3)
            p = p.next
            print('-----------------')

        self.show_result()

    def judge(self, sum1, sum2):
        if (sum1 > 21 and sum2 > 21) or (sum1 == sum2):
            return 0
        elif sum2 > 21 or (21 >= sum1 > sum2):
            return 1
        elif sum1 > 21 or (21 >= sum2 > sum1):
           return -1
        else:
            raise Exception()

    def show_result(self):
        p = self.players
        p[0].print_cards(False,True)
        p[1].print_cards(False,True)

        sum1 = p[0].sum()
        sum2 = p[1].sum()
        
        res = self.judge(sum1, sum2)
        if res == 0:
            print('Draw!')
        elif res == 1:
            print(p[0], 'wins!')
        else:
            print(p[1], 'wins!')


sess = Session()
sess.game_loop()
# print(sess.judge(24, 16) or 24 < 21)
