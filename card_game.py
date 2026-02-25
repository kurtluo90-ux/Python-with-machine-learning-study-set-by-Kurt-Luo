import random

class CardGame:
    def __init__(self):
        self.suits = ['♠', '♥', '♦', '♣']
        self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.jokers = ['小王', '大王']
        self.deck = []
        self.players = []
        self.dealer = None
        self.base_bet = 1
        
    def create_deck(self):
        deck = []
        for suit in self.suits:
            for rank in self.ranks:
                deck.append([suit, rank])
        deck.append(['', '小王'])
        deck.append(['', '大王'])
        random.shuffle(deck)
        return deck
    
    def get_card_value(self, card):
        if card[1] in ['10', 'J', 'Q', 'K']:
            return 0
        elif card[1] == 'A':
            return 1
        elif card[1] in self.ranks[1:9]:
            return int(card[1])
        elif card[1] in self.jokers:
            return 0
        return 0
    
    def calculate_points(self, cards):
        total = 0
        joker_count = 0
        
        for card in cards:
            if card[1] in self.jokers:
                joker_count += 1
            else:
                total += self.get_card_value(card)
        
        if joker_count > 0:
            return self.calculate_with_joker(cards, total, joker_count)
        
        return total % 10
    
    def calculate_with_joker(self, cards, total, joker_count):
        best_points = total % 10
        
        for i in range(10):
            test_total = total + i * joker_count
            test_points = test_total % 10
            if test_points > best_points:
                best_points = test_points
        
        return best_points
    
    def get_card_type_2(self, cards):
        if len(cards) != 2:
            return None, 1
        
        card1, card2 = cards
        is_double_joker = (card1[1] in self.jokers and card2[1] in self.jokers)
        has_joker = (card1[1] in self.jokers or card2[1] in self.jokers)
        
        if is_double_joker:
            return '无敌', 10
        
        points = self.calculate_points(cards)
        
        is_same_suit = (card1[0] == card2[0] and card1[0] != '')
        is_same_rank = (card1[1] == card2[1])
        
        if is_same_suit or is_same_rank:
            if points == 9:
                return '双倍天公9', 2
            elif points == 8:
                return '双倍天公8', 2
            else:
                return '二倍对子', 2
        
        if points == 9:
            return '天公9', 1
        elif points == 8:
            return '天公8', 1
        
        if points == 0:
            return '木虱', 1
        
        return f'{points}点', 1
    
    def get_card_type_3(self, cards):
        if len(cards) != 3:
            return None, 1
        
        points = self.calculate_points(cards)
        
        is_flush = self.is_flush(cards)
        is_straight = self.is_straight(cards)
        is_three_of_kind = self.is_three_of_kind(cards)
        
        if is_flush and is_straight:
            return '八倍同花顺', 8
        elif is_three_of_kind:
            return '五倍三同张', 5
        elif is_straight:
            return '四倍顺子', 4
        elif is_flush:
            return '三倍同花', 3
        
        if points == 0:
            return '木虱', 1
        
        return f'{points}点', 1
    
    def is_straight(self, cards):
        joker_count = sum(1 for card in cards if card[1] in self.jokers)
        
        if joker_count == 2:
            return True
        
        if joker_count == 1:
            non_joker_ranks = []
            for card in cards:
                if card[1] not in self.jokers:
                    if card[1] == 'A':
                        non_joker_ranks.append(1)
                    elif card[1] == 'K':
                        non_joker_ranks.append(13)
                    elif card[1] == 'Q':
                        non_joker_ranks.append(12)
                    elif card[1] == 'J':
                        non_joker_ranks.append(11)
                    elif card[1] == '10':
                        non_joker_ranks.append(10)
                    else:
                        non_joker_ranks.append(int(card[1]))
            
            if len(non_joker_ranks) == 2:
                diff = abs(non_joker_ranks[1] - non_joker_ranks[0])
                if diff == 1 or diff == 2:
                    return True
                if non_joker_ranks == [1, 13] or non_joker_ranks == [1, 12]:
                    return True
            return False
        
        ranks = []
        for card in cards:
            if card[1] == 'A':
                ranks.append(1)
            elif card[1] == 'K':
                ranks.append(13)
            elif card[1] == 'Q':
                ranks.append(12)
            elif card[1] == 'J':
                ranks.append(11)
            elif card[1] == '10':
                ranks.append(10)
            else:
                ranks.append(int(card[1]))
        
        ranks.sort()
        
        if ranks[2] - ranks[0] == 2 and ranks[1] - ranks[0] == 1:
            return True
        
        if ranks == [1, 12, 13] or ranks == [1, 2, 3] or ranks == [1, 2, 13]:
            return True
        
        return False
    
    def is_three_of_kind(self, cards):
        joker_count = sum(1 for card in cards if card[1] in self.jokers)
        
        if joker_count == 0:
            return cards[0][1] == cards[1][1] == cards[2][1]
        
        if joker_count == 1:
            non_joker_ranks = [card[1] for card in cards if card[1] not in self.jokers]
            if len(non_joker_ranks) == 2 and non_joker_ranks[0] == non_joker_ranks[1]:
                return True
        
        if joker_count >= 2:
            return True
        
        return False
    
    def is_pair(self, cards):
        return (cards[0][1] == cards[1][1] or 
                cards[0][1] == cards[2][1] or 
                cards[1][1] == cards[2][1])
    
    def is_flush(self, cards):
        non_joker_suits = [card[0] for card in cards if card[0] != '']
        
        if len(non_joker_suits) == 0:
            return True
        
        if len(non_joker_suits) == 1:
            return True
        
        if len(non_joker_suits) == 2:
            return non_joker_suits[0] == non_joker_suits[1]
        
        if len(non_joker_suits) == 3:
            return non_joker_suits[0] == non_joker_suits[1] == non_joker_suits[2]
        
        return False
    
    def must_draw_third(self, cards):
        if len(cards) != 2:
            return False
        
        joker_count = sum(1 for card in cards if card[1] in self.jokers)
        return joker_count == 1
    
    def compare_hands(self, hand1, hand2):
        type1, mult1 = self.get_hand_type(hand1)
        type2, mult2 = self.get_hand_type(hand2)
        
        priority_order = [
            '无敌', '双倍天公9', '双倍天公8', '天公9', '天公8', 
            '八倍同花顺', '五倍三同张', '四倍顺子', '三倍同花', '二倍对子', 
            '9点', '8点', '7点', '6点', '5点', '4点', '3点', '2点', '1点', '木虱'
        ]
        
        try:
            priority1 = priority_order.index(type1)
            priority2 = priority_order.index(type2)
        except ValueError:
            priority1 = 99
            priority2 = 99
        
        if type1 == '二倍对子' and type2 == '二倍对子':
            points1 = self.calculate_points(hand1)
            points2 = self.calculate_points(hand2)
            if points1 > points2:
                return 1, mult1
            elif points1 < points2:
                return -1, mult2
            else:
                return 0, mult1
        elif type1 == '二倍对子' or type2 == '二倍对子':
            points1 = self.calculate_points(hand1)
            points2 = self.calculate_points(hand2)
            if points1 > points2:
                return 1, mult1
            elif points1 < points2:
                return -1, mult2
            elif type1 == '二倍对子':
                return 1, mult1
            else:
                return -1, mult2
        
        if priority1 < priority2:
            return 1, mult1
        elif priority1 > priority2:
            return -1, mult2
        else:
            return 0, mult1
    
    def get_hand_type(self, hand):
        if len(hand) == 2:
            return self.get_card_type_2(hand)
        elif len(hand) == 3:
            return self.get_card_type_3(hand)
        else:
            return None, 1
    
    def deal_cards(self, num_players):
        self.deck = self.create_deck()
        self.players = []
        
        for i in range(num_players):
            hand = [self.deck.pop(), self.deck.pop()]
            self.players.append({
                'id': i,
                'hand': hand,
                'bet': self.base_bet
            })
        
        self.dealer = {
            'id': 'dealer',
            'hand': [self.deck.pop(), self.deck.pop()],
            'bet': self.base_bet
        }
        
        return self.players, self.dealer
    
    def draw_card(self, player):
        if len(player['hand']) >= 3:
            return False
        
        if len(self.deck) == 0:
            return False
        
        new_card = self.deck.pop()
        player['hand'].append(new_card)
        return True
    
    def play_round(self, num_players=2):
        print(f"\n=== 新游戏开始 ===")
        print(f"玩家数量: {num_players}")
        print(f"底注: {self.base_bet}")
        
        self.deal_cards(num_players)
        
        print(f"\n=== 发牌阶段 ===")
        for i, player in enumerate(self.players):
            print(f"玩家{i+1}的牌: {player['hand']}")
        print(f"庄家的牌: {self.dealer['hand']}")
        
        print(f"\n=== 补牌阶段 ===")
        for i, player in enumerate(self.players):
            if self.must_draw_third(player['hand']):
                print(f"玩家{i+1}有1张鬼牌，必须补牌")
                self.draw_card(player)
                print(f"玩家{i+1}补牌后: {player['hand']}")
            else:
                choice = input(f"玩家{i+1}是否补牌？(y/n): ").strip().lower()
                if choice == 'y':
                    self.draw_card(player)
                    print(f"玩家{i+1}补牌后: {player['hand']}")
                else:
                    print(f"玩家{i+1}选择不补牌: {player['hand']}")
        
        if self.must_draw_third(self.dealer['hand']):
            print(f"庄家有1张鬼牌，必须补牌")
            self.draw_card(self.dealer)
            print(f"庄家补牌后: {self.dealer['hand']}")
        else:
            choice = input(f"庄家是否补牌？(y/n): ").strip().lower()
            if choice == 'y':
                self.draw_card(self.dealer)
                print(f"庄家补牌后: {self.dealer['hand']}")
            else:
                print(f"庄家选择不补牌: {self.dealer['hand']}")
        
        print(f"\n=== 比牌阶段 ===")
        for i, player in enumerate(self.players):
            result, multiplier = self.compare_hands(player['hand'], self.dealer['hand'])
            player_type, player_mult = self.get_hand_type(player['hand'])
            dealer_type, dealer_mult = self.get_hand_type(self.dealer['hand'])
            
            print(f"\n玩家{i+1} vs 庄家:")
            print(f"玩家{i+1}: {player['hand']} - {player_type} (×{player_mult})")
            print(f"庄家: {self.dealer['hand']} - {dealer_type} (×{dealer_mult})")
            
            if result == 1:
                win_amount = self.base_bet * multiplier
                print(f"玩家{i+1}赢了! 赢得 {win_amount}")
            elif result == -1:
                lose_amount = self.base_bet * multiplier
                print(f"玩家{i+1}输了! 输掉 {lose_amount}")
            else:
                print(f"平局!")
        
        return True

if __name__ == "__main__":
    game = CardGame()
    num_players = int(input("请输入玩家数量 (2-7): "))
    if num_players < 2:
        num_players = 2
    elif num_players > 7:
        num_players = 7
    
    while True:
        game.play_round(num_players)
        play_again = input("\n是否继续游戏？(y/n): ").strip().lower()
        if play_again != 'y':
            print("游戏结束，谢谢参与！")
            break
