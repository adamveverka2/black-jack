import random
from machine import Pin
import time
import fun

button_hit = Pin(2, Pin.IN, Pin.PULL_UP)
button_pass = Pin(3, Pin.IN, Pin.PULL_UP)
button_double = Pin(4, Pin.IN, Pin.PULL_UP)
button_split = Pin(5, Pin.IN, Pin.PULL_UP)


# Constants
BLACKJACK = 21
DEALER_MIN = 16
BLACKJACK_PAYOUT = 2.5
DEBOUNCE_DELAY = 0.3  # 300ms debounce delay

# Globals
balance = int(input("Input starting money: "))
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
    while value > BLACKJACK and num_aces > 0:
        value -= 10
        num_aces -= 1
    return value

def is_button_pressed(button):
    global last_pressed_time
    current_time = time.ticks_ms()
    if not button.value() and (current_time - last_pressed_time > DEBOUNCE_DELAY * 1000):
        last_pressed_time = current_time
        return True
    return False

def game(player_value, dealer_value):
    global balance, bet

    if player_value > 21:
        print("Game over! Player busts. Dealer wins.")
    elif dealer_value > 21 or player_value > dealer_value:
        print("Victory! Player wins!")
        balance += bet * 2
    elif player_value == dealer_value:
        print("Draw! Player draws.")
        balance += bet
    else:
        print("Game over! Dealer wins.")

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
        new_card = fun.hit(dealer, shuffled_deck)
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
    
    bet = int(input("\nEnter your bet: "))
    while bet > balance:
        print("Insufficient balance! Bet lower.")
        bet = int(input("\nEnter your bet: "))
    balance -= bet

    print("Dealer's hand:", dealer, "-> Total Value:", hand_value(dealer))
    print("Player's hand:", player, "-> Total Value:", hand_value(player))

# Main Loop

split_check = 0
blackjack_round_start = 1
last_pressed_time = 0  # Timestamp of the last button press
debounce_delay = 0.3  # 300ms debounce delay
reset_game()

def hit(player):
    global split_check, current_hand,hand_value1, hand_value2
    player.append(shuffled_deck.pop())
    player_value = hand_value(player)
    print("Player's hand:", player, "-> Total Value:", player_value)
    
    if player_value > BLACKJACK:
        if split_check == 0:
            print("\nGame over! Player busts.")
            reset_game()
        else:
            if current_hand == 1:
                print("\n hand! busts.")
                print("currently playing Hand 2:", hand2, "-> Total Value:", hand_value(hand2))
                current_hand = 2
            else:
                if hand_value1 <= BLACKJACK:
                    game(player_value, dealer_value)
                else:
                    print("\nGame over! Player busts.")
                     
def pass1():
    dealer_turn()
    dealer_value = hand_value(dealer)  # Ensure dealer's value is updated after their turn
    game(player_value, dealer_value)
    
def pass2():
    global current_hand,player_value2,player_value1
    if current_hand == 2:
        dealer_turn()
        dealer_value = hand_value(dealer)  # Ensure dealer's value is updated after their turn
        game(player_value1, dealer_value)
        game(player_value2, dealer_value)
    
    if current_hand == 1:
        current_hand = 2
        print("currently playing Hand 2:", hand2, "-> Total Value:", hand_value(hand2))

        
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
        
    
    dealer_turn()
    dealer_value = hand_value(dealer)   # Ensure dealer's value is updated after their turn
    
    game(player_value, dealer_value)
    

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
        reset_game()
            
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

                if is_button_pressed(button_hit):
                    print("\nButton pressed! Player hits.")
                    if current_hand == 1:
                        hit(hand1)
                        blackjack_round_start = 0
                        continue
                    else:
                        hit(hand2)
                        blackjack_round_start = 0
                        continue
 
                 # Player passes
                elif not button_pass.value() and (current_time - last_pressed_time > debounce_delay * 1000):
                    last_pressed_time = current_time
                    print("\nPlayer passes.")
                    
                    blackjack_round_start = 0
                    pass2()
                    
                    if current_hand == 2:
                        pass2()
                        reset_game()
                    
                elif is_button_pressed(button_double): #doesn't work
                    print("\nButton pressed! Player doubles.")
                    
                    blackjack_round_start = 0
       
    time.sleep(0.05)
