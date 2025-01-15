import random
from machine import Pin
import time

button_hit = Pin(2, Pin.IN, Pin.PULL_UP)
button_pass = Pin(3, Pin.IN, Pin.PULL_UP)
button_double = Pin(4, Pin.IN, Pin.PULL_UP)
button_split = Pin(5, Pin.IN, Pin.PULL_UP)


# Constants
BLACKJACK = 21
DEALER_MIN = 16
BLACKJACK_PAYOUT = 2.5

hand_bust1 = 0
hand_bust2 = 0
end_split = 0


while True:
    try:
        balance = int(input("Input starting money: "))
        if balance <= 0:
            print("Starting money must be greater than zero. Please try again.")
        else:
            break
    except ValueError:
        print("Invalid input! Please enter a numeric value.")

last_pressed_time = 0  # Timestamp of the last button press


# Utility Functions
def card_value(card):
    rank = card[:-1]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    return int(rank)

def hand_value(hand):
    value = sum(card_value(card) for card in hand)
    num_aces = sum(1 for card in hand if card[:-1] == 'A')
    while value > BLACKJACK and num_aces > 0: #ace truns into 1
        value -= 10
        num_aces -= 1
    return value

def is_button_pressed(button):
    global last_pressed_time
    current_time = time.ticks_ms()
    if not button.value() and (current_time - last_pressed_time > debounce_delay * 1000):
        last_pressed_time = current_time
        return True
    return False

def game(player_value, dealer_value):
    global balance, bet

    if dealer_value > BLACKJACK or player_value > dealer_value:
        print("Victory! Player wins!")
        balance += bet * 2
    elif player_value == dealer_value:
        print("Draw! Player draws.")
        balance += bet
    else:
        print("Game over! Dealer wins.")
        
def game2(player_value1,player_value2,dealer_value):
    global hand_bust2,hand_bust1,balance, bet1, bet2
    
    if hand_bust2 == 0 or hand_bust1 == 0:
        dealer_turn()
        dealer_value = hand_value(dealer)
        
    print(player_value1,player_value2,dealer_value)
    
    
    if hand_bust1 == 1 and hand_bust2 == 0:
        if dealer_value > BLACKJACK or player_value2 > dealer_value:
            print("Hand1 busts, Hand2 wins")
            balance += bet2 * 2
        elif player_value2 == dealer_value:
            print("Hand1 busts, Hand2 draws with dealer.")
            balance += bet2
        else:
            print("Game over! Dealer wins.")
    
    elif hand_bust1 == 0 and hand_bust2 == 1:
        if dealer_value > BLACKJACK or player_value1 > dealer_value:
            print("Hand2 busts, Hand1 wins")
            balance += bet1 * 2
        elif player_value1 == dealer_value:
            print("Hand2 busts, Hand1 draws with dealer.")
            balance += bet1
        else:
            print("Game over! Dealer wins.")
    
    elif hand_bust1 == 1 and hand_bust2 == 1:
        print("Game over! Both hands bust, Dealer wins.")
    
    else:
        if dealer_value > BLACKJACK or player_value2 > dealer_value:
            print("Hand2 wins")
            balance += bet2 * 2
        elif player_value2 == dealer_value:
            print("Hand2 draws with dealer.")
            balance += bet2
        else:
            print("Hand2 busts, Dealer wins.")
        
        if dealer_value > BLACKJACK or player_value1 > dealer_value:
            print("Hand1 wins")
            balance += bet1 * 2
        elif player_value1 == dealer_value:
            print("Hand1 draws with dealer.")
            balance += bet1
        else:
            print("Hand1 busts, Dealer wins.")
            
    end_split = 1
    hand_bust1 = 0
    hand_bust2 = 0

def check_blackjack(player_value, dealer_value):
    global balance, bet, blackjack_round_start
    if blackjack_round_start == 1:
        if player_value == BLACKJACK or dealer_value == BLACKJACK:
            if player_value == BLACKJACK and dealer_value == BLACKJACK:
                print("Both player and dealer have blackjack. It's a draw!")
                balance += bet
            elif player_value == BLACKJACK:
                print("Player wins with a blackjack!")
                balance += bet * BLACKJACK_PAYOUT
            else:
                print("Dealer wins with a blackjack!")
            reset_game()
            return True
        return False

def dealer_turn():
    global dealer, dealer_value, shuffled_deck
    while dealer_value <= DEALER_MIN:
        dealer.append(shuffled_deck.pop())
        dealer_value = hand_value(dealer)
        print("Dealer's hand:", dealer, "-> Total Value:", dealer_value)

def reset_game():
    global dealer, player, shuffled_deck, balance, bet, blackjack_round_start
        
    # Custom shuffling logic instead of `random.shuffle`
    deck = [rank + suit for suit in ['S', 'H', 'D', 'C'] for rank in 
        ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]
    shuffled_deck = sorted(deck, key=lambda x: random.random())

    dealer, player = [shuffled_deck.pop() for _ in range(2)], [shuffled_deck.pop() for _ in range(2)]
    
    print("\nNew Game!")
    print("Current balance:", balance)
    
    blackjack_round_start = 1
    
    while True:
        try:
            bet = int(input("\nEnter your bet: "))
            if bet <= 0:
                print("Bet cannot be zero! Please enter a valid amount.")
            elif bet > balance:
                print("Insufficient balance! Bet lower.")
            else:
                break
        except ValueError:
            print("Invalid input! Please enter a numeric value.")

    
    balance -= bet

    print("Dealer's hand:", dealer, "-> Total Value:", hand_value(dealer))
    print("Player's hand:", player, "-> Total Value:", hand_value(player))

def hit(player):
    player.append(shuffled_deck.pop())
    player_value = hand_value(player)
    print("Player's hand:", player, "-> Total Value:", player_value)
    
    if player_value > BLACKJACK:
        print("\nGame over! Player busts.")
        reset_game()

def hit2(player):
    global current_hand,hand_bust1,hand_bust2,end_split
    
    if current_hand == 1:
        player.append(shuffled_deck.pop())
        player_value = hand_value(hand1)
        print("Player's hand 1:", player, "-> Total Value:", player_value)
        
        if player_value > BLACKJACK:
            print("\n First hand busts.")
            hand_bust1 = 1
            current_hand = 2
        
    else:
        player.append(shuffled_deck.pop())
        player_value = hand_value(hand2)
        print("Player's hand 2:", player, "-> Total Value:", player_value)
        
        if player_value > BLACKJACK:
            print("\n Second hand busts.")
            hand_bust2 = 1
            end_split = 1
        
            game2(player_value1,player_value2,dealer_value)
            
    
def pass1():
    dealer_turn()
    dealer_value = hand_value(dealer)  # Ensure dealer's value is updated after their turn
    game(player_value, dealer_value)

def pass2():
    global current_hand,ha
    
    if current_hand == 2:
         game2(player_value1,player_value2,dealer_value)
         end_split = 1
    elif current_hand == 1:
        print("\nplayer passes hand 1!")
        current_hand = 2
    
def double(player):
    global bet, balance
    
    player.append(shuffled_deck.pop())
    player_value = hand_value(player)
    print("Player's hand:", player, "-> Total Value:", player_value)
    
    balance -= bet
    bet += bet
    print("\nbet incrised to:", bet,"\n")
    
    if player_value > BLACKJACK:
        print("Game over! Player busts.")
        reset_game()
    else:
        dealer_turn()
        dealer_value = hand_value(dealer)   # Ensure dealer's value is updated after their turn
        game(player_value, dealer_value)
        reset_game()
        
def double1(player):
    global current_hand,hand_bust1,hand_bust2,end_split
    
    if current_hand == 1:
        player.append(shuffled_deck.pop())
        player_value = hand_value(hand1)
        print("Player's hand 1:", player, "-> Total Value:", player_value)
        
        if player_value > BLACKJACK:
            print("\n First hand busts.")
            hand_bust1 = 1
        
        current_hand = 2
        
    else:
        player.append(shuffled_deck.pop())
        player_value = hand_value(hand2)
        print("Player's hand 2:", player, "-> Total Value:", player_value)
        
        if player_value > BLACKJACK:
            print("\n First hand busts.")
            hand_bust2 = 1
            end_split = 1
        
        game2(player_value1,player_value2,dealer_value)

last_pressed_time = 0  # Timestamp of the last button press
debounce_delay = 0.3  # 300ms debounce delay
reset_game()

while True:
    player_value = hand_value(player)
    dealer_value = hand_value(dealer)
    current_time = time.ticks_ms()  # Get the current time in milliseconds

    if check_blackjack(player_value, dealer_value):
        continue

    if is_button_pressed(button_hit):
        print("\nButton pressed! Player hits.")
        hit(player)
        blackjack_round_start = 0
        continue

    # Player passes
    elif not button_pass.value() and (current_time - last_pressed_time > debounce_delay * 1000):
        last_pressed_time = current_time
        print("\nPlayer passes.")
        
        blackjack_round_start = 0
        pass1()
        reset_game()
        
    elif is_button_pressed(button_double):
        print("\nButton pressed! Player doubles.")
        
        blackjack_round_start = 0
        double(player)
        
    elif is_button_pressed(button_split):
    # Check if splitting is allowed
        if len(player) == 2 and player[0][:-1] == player[1][:-1]:  # Compare ranks of the two cards
            print("\nPlayer splits.")

            # Create two hands
            hand1 = [player[0], shuffled_deck.pop()]  # First card + new card
            hand2 = [player[1], shuffled_deck.pop()]  # Second card + new card

            bet2 = bet
            balance -= bet2

            print("Hand 1:", hand1, "-> Total Value:", hand_value(hand1))
            print("Hand 2:", hand2, "-> Total Value:", hand_value(hand2))
            
            current_hand = 1
            split_check = 1
            print("currently playing Hand 1:", hand1, "-> Total Value:", hand_value(hand1))
            
            # loop for playing split hands
            while True:
                player_value1 = hand_value(hand1)
                player_value2 = hand_value(hand2)
                dealer_value = hand_value(dealer)
                current_time = time.ticks_ms()  # Get the current time in milliseconds
                bet1 = bet 
                bet2 = bet
                
                if is_button_pressed(button_hit):
                    print("\nButton pressed! Player hits.")
                    if current_hand == 1:
                        hit2(hand1)
                        blackjack_round_start = 0
                    else:
                        hit2(hand2)
                        blackjack_round_start = 0
                        if hand_bust2 == 1:
                            end_split = 1
 
                 # Player passes
                elif not button_pass.value() and (current_time - last_pressed_time > debounce_delay * 1000):
                    last_pressed_time = current_time
                    print("\nPlayer passes.")
                    
                    blackjack_round_start = 0
                    
                    if current_hand == 2:
                        pass2()
                        end_split = 1
                    else:
                        pass2()
                    
                elif is_button_pressed(button_double): 
                    print("\nButton pressed! Player doubles.")
                    
                    blackjack_round_start = 0
                    
                    if current_hand == 1:
                        double1(hand1)
                        blackjack_round_start = 0
                    else:
                        double1(hand2)
                        blackjack_round_start = 0
                        end_split = 1
                        
                
                if end_split == 1:
                    end_split = 0
                    hand_bust1 = 0
                    hand_bust2 = 0
                    reset_game()
                    break
                    
    time.sleep(0.05)

