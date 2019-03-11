class Player(object):
    def __init__(self, session, order):
        self.session = session
        self.basecard = None
        self.card_list = []
        self.next = self
        self.name = 'Player %d'%order
        self.AI = False

    def __repr__(self):
        return self.name + '[%s]'%('AI' if self.AI else 'P')

    def set_basecard(self, basecard):
        assert(self.basecard is None)
        self.basecard = basecard
    
    def print_cards(self, hide_basecard=True, print_sum=True):
        assert(self.basecard is not None)
        print(self, '的手牌：', end=' ')
        # hide_basecard = False
        if hide_basecard: 
            print('X', end=' ')
        else:
            print(self.basecard, end=' ')
        for card in self.card_list:
            print(card, end=' ')
        if print_sum:
            _sum = self.sum(hide_basecard)
            print('sum=%d%s'%(_sum, '+X' if hide_basecard else ''), end='')

        print()

    def draw(self, print_cards=True):
        card = self.session.card_pile.pop()
        self.card_list.append(card)
        if print_cards: 
            print(self, '摸了一张', card)
            self.print_cards(self.AI)

    def sum(self, hide_basecard=False):
        '''
        return a integer.
        '''
        ret = 0
        for card in self.card_list:
            ret += card.number
        if not hide_basecard:
            ret += self.basecard.number
        return ret

    def player_judge(self):
        print('Stay[S] or draw[D]?', end=' ')
        res = input()
        return res

    def AI_judge(self):
        sess = self.session
        visit = {} # still unused.
        for i in range(1, 12):
            visit[i] = True
        visit[self.basecard.number] = False
        for card in self.card_list:
            visit[card.number] = False
        for card in self.next.card_list:
            visit[card.number] = False
        
        oppo_sum = self.next.sum(hide_basecard=True)
        self_sum = self.sum(hide_basecard=False)
        if oppo_sum >= 21 or self_sum > 21:
            # print('someone busts...')
            return 'S'

        possibilities = [i for i in visit if visit[i]]
        chance = 0
        win_count = 0
        for i in possibilities:
            _oppo_sum = oppo_sum + i
            _remain = possibilities.copy()
            _remain.remove(i)
            for j in _remain:
                if self_sum+j <= 21: win_count += 1
                
        chance = win_count / (len(possibilities)*(len(possibilities)-1))
        # print(chance)
        if chance > 0.5: return 'D'
        else: return 'S'