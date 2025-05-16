import random
import time
import LCD_lib as lcd
from machine import Pin,SPI,PWM
import framebuf
import os
import gc

gc.collect()

button_hit = Pin(15,Pin.IN,Pin.PULL_UP)
button_pass = Pin(17,Pin.IN,Pin.PULL_UP)
button_double = Pin(19 ,Pin.IN,Pin.PULL_UP)

value_up = Pin(2,Pin.IN,Pin.PULL_UP)
value_down = Pin(18,Pin.IN,Pin.PULL_UP)
value_add = Pin(20,Pin.IN,Pin.PULL_UP)
value_remove = Pin(16,Pin.IN,Pin.PULL_UP)
set_value = Pin(3,Pin.IN,Pin.PULL_UP)

# Constants
BLACKJACK = 21
DEALER_MIN = 16
BLACKJACK_PAYOUT = 2.5

size = 3
card_size = 5
card_number_offsets = {
    1: 0,
    2: 50,
    3: 100,
    4: 150
}
row_offsets ={
    1: 0 + 5,
    2: 60 + 10,
    3: 120 + 15        
    }

LCD = lcd.LCD_1inch3()
LCD.fill(0)
LCD.show()

last_pressed_time = 0  # Timestamp of the last button press
balance = 0
bet = 0

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

def balance_input():
    global balance
    joystick_value = [1,5,10,25,50,100,250,500,1000,1000,1]
    current_joystick_value = 0
    
    while True:
        LCD.fill(0)
        LCD.text(f"balance:{balance}",0,150, LCD.white)
        ammount = joystick_value[current_joystick_value]
        LCD.text(f"ammount:{ammount}",0,160, LCD.white)
        
        if current_joystick_value == 9:
            current_joystick_value = 0
            
        if current_joystick_value == -1:
            current_joystick_value = 8      

        if is_button_pressed(value_up):
            current_joystick_value = current_joystick_value + 1
            continue
        
        if is_button_pressed(value_down):
            current_joystick_value = current_joystick_value - 1
            continue
        
        if is_button_pressed(value_add):
            balance = balance + joystick_value[current_joystick_value] 
            continue
        
        if is_button_pressed(value_remove):
            balance = balance - joystick_value[current_joystick_value]
            continue
        
        if is_button_pressed(set_value):
            break
        
        LCD.show()
        
def bet_input():
    global bet
    joystick_value = [1, 5, 10, 25, 50, 100, 250, 500, 1000]
    current_joystick_value = 0
    bet = 0  # Initialize bet here
    
    while True:
        LCD.fill(0)  # Clear the screen each loop iteration
        LCD.text(f"Balance: {balance}", 0, 160, LCD.white)
        LCD.text(f"Bet: {bet}", 0, 170, LCD.white)
        amount = joystick_value[current_joystick_value]
        LCD.text(f"Amount: {amount}", 0, 180, LCD.white)
        
        # Handling joystick value cycling
        if current_joystick_value == len(joystick_value):  # If we reach the end of the list
            current_joystick_value = 0
        if current_joystick_value == -1:  # If we go below the start of the list
            current_joystick_value = len(joystick_value) - 1
        
        # Button logic
        if is_button_pressed(value_up):
            current_joystick_value += 1
            continue
        
        if is_button_pressed(value_down):
            current_joystick_value -= 1
            continue
        
        if is_button_pressed(value_add):
            bet += joystick_value[current_joystick_value]
            continue
        
        if is_button_pressed(value_remove):
            bet -= joystick_value[current_joystick_value]
            continue
        
        if is_button_pressed(set_value):
            break  # Exit the loop when set_value button is pressed
        
        LCD.show()  # Update the LCD screen with the new values
        
def is_button_pressed(button):
    global last_pressed_time
    current_time = time.ticks_ms()
    if not button.value() and (current_time - last_pressed_time > debounce_delay * 1000):
        last_pressed_time = current_time
        return True
    return False

def game(player_value, dealer_value):
    global balance, bet
    
    LCD.fill(0)
    
    if dealer_value > BLACKJACK or player_value > dealer_value:
        print("PLAYER WON")
        balance += bet * 2
        LCD.text("PLAYER WON",70 ,100 , LCD.green)
        
    elif player_value == dealer_value:
        print("PLAYER DRAWS")
        balance += bet
        LCD.text("PLAYER DRAWS",70 ,100 , LCD.white)
        
    else:
        print("PLAYER LOSSES")
        LCD.text("PLAYER LOSSES",70 ,100 , LCD.red)
        
    LCD.show()
    time.sleep(4.5)

def check_blackjack(player_value, dealer_value):
    global balance, bet, blackjack_round_start
    if blackjack_round_start == 1:
        if player_value == BLACKJACK or dealer_value == BLACKJACK:
            time.sleep(2)
            LCD.fill(0)
            if player_value == BLACKJACK and dealer_value == BLACKJACK:
                print("Both player and dealer have blackjack. It's a draw!")
                balance += bet
                LCD.text("PLAYER DRAWS",70 ,100 , LCD.white)
            elif player_value == BLACKJACK:
                print("Player wins with a blackjack!")
                balance += bet * BLACKJACK_PAYOUT
                LCD.text("PLAYER WON",70 ,100 , LCD.green)
            else:
                print("Dealer wins with a blackjack!")
                LCD.text("PLAYER LOSSES",70 ,100 , LCD.red)
            reset_game()
            return True
        return False

def dealer_turn():
    global dealer, dealer_value, shuffled_deck
    
    while dealer_value <= DEALER_MIN:
        dealer.append(shuffled_deck.pop())
        dealer_value = hand_value(dealer)
    
        card_number = 3
        
        for i in range(1, len(dealer) + 1):
            cards = dealer.copy()
            
            first_card = cards.pop(i - 1)
            
            current_suite = first_card[-1]
            current_card_value = first_card[:-1]
            
            suite_selection(2, i, current_card_value, current_suite)
            LCD.show()
            
            print("Dealer's hand:", dealer, "-> Total Value:", dealer_value)
            
            time.sleep(1)

def diamonds(card_rank,card_number):
    
    LCD.fill_rect(0 * card_size + offset_cards, 1 * card_size + vertical_offset, 9 * card_size, 12 * card_size, LCD.green)
    LCD.fill_rect(1 * card_size + offset_cards, 2 * card_size + vertical_offset, 7 * card_size, 10 * card_size, LCD.white)
    
    LCD.fill_rect(0 * size + offset_diamonds, 3 * size + 24 + vertical_offset, 7 * size, 3 * size, 184)
    LCD.fill_rect(1 * size + offset_diamonds, 2 * size + 24 + vertical_offset, 5 * size, 5 * size, 184)
    LCD.fill_rect(3 * size + offset_diamonds, 0 * size + 24 + vertical_offset, 1 * size, 9 * size, LCD.red)
    LCD.fill_rect(2 * size + offset_diamonds, 1 * size + 24 + vertical_offset, 3 * size, 7 * size, LCD.red)
    LCD.fill_rect(1 * size + offset_diamonds, 3 * size + 24 + vertical_offset, 5 * size, 3 * size, LCD.red)
    LCD.fill_rect(0 * size + offset_diamonds, 4 * size + 24 + vertical_offset, 7 * size, 1 * size, LCD.red)
    
    LCD.text(card_rank,22 + text_offset,12 + vertical_offset, LCD.black)
    LCD.show()

def spades(card_rank,card_number):
    
    LCD.fill_rect(0 * card_size + offset_cards, 1 * card_size + vertical_offset, 9 * card_size, 12 * card_size, LCD.green)
    LCD.fill_rect(1 * card_size + offset_cards, 2 * card_size + vertical_offset, 7 * card_size, 10 * card_size, LCD.white)
    
    LCD.fill_rect(3 * size + offset_spades, 8 * size + 24 + vertical_offset, 3 * size, 1 * size, 21083)
    LCD.fill_rect(4 * size + offset_spades, 0 * size + 24 + vertical_offset, 1 * size, 9 * size, LCD.black)
    LCD.fill_rect(3 * size + offset_spades, 1 * size + 24 + vertical_offset, 3 * size, 6 * size, LCD.black)
    LCD.fill_rect(0 * size + offset_spades, 4 * size + 24 + vertical_offset, 9 * size, 3 * size, LCD.black)
    LCD.fill_rect(1 * size + offset_spades, 3 * size + 24 + vertical_offset, 2 * size, 5 * size, LCD.black)
    LCD.fill_rect(6 * size + offset_spades, 3 * size + 24 + vertical_offset, 2 * size, 5 * size, LCD.black)
    LCD.fill_rect(2 * size + offset_spades, 2 * size + 24 + vertical_offset, 5 * size, 1 * size, LCD.black)
    LCD.fill_rect(1 * size + offset_spades, 3 * size + 24 + vertical_offset, 7 * size, 1 * size, LCD.black)
    LCD.fill_rect(3 * size + offset_spades, 9 * size + 24 + vertical_offset, 3 * size, 1 * size, LCD.black)
    
    LCD.text(card_rank,22 + text_offset,12 + vertical_offset, LCD.black)
    LCD.show()
    
def hearts(card_rank,card_number):
    
    LCD.fill_rect(0 * card_size + offset_cards, 1 * card_size + vertical_offset, 9 * card_size, 12 * card_size, LCD.green)
    LCD.fill_rect(1 * card_size + offset_cards, 2 * card_size + vertical_offset, 7 * card_size, 10 * card_size, LCD.white)
    
    LCD.fill_rect(1 * size + offset_hearts, 0 * size + 24 + vertical_offset, 7 * size, 1 * size, LCD.red)
    LCD.fill_rect(0 * size + offset_hearts, 1 * size + 24 + vertical_offset, 9 * size, 3 * size, LCD.red)
    LCD.fill_rect(0 * size + offset_hearts, 4 * size + 24 + vertical_offset, 9 * size, 1 * size, 184)
    LCD.fill_rect(1 * size + offset_hearts, 4 * size + 24 + vertical_offset, 7 * size, 1 * size, LCD.red)
    LCD.fill_rect(1 * size + offset_hearts, 5 * size + 24 + vertical_offset, 7 * size, 1 * size, LCD.red)
    LCD.fill_rect(2 * size + offset_hearts, 6 * size + 24 + vertical_offset, 5 * size, 1 * size, LCD.red)
    LCD.fill_rect(3 * size + offset_hearts, 7 * size + 24 + vertical_offset, 3 * size, 1 * size, LCD.red)
    LCD.fill_rect(4 * size + offset_hearts, 8 * size + 24 + vertical_offset, 1 * size, 1 * size, LCD.red)
    LCD.fill_rect(3 * size + offset_hearts, 0 * size + 24 + vertical_offset, 3 * size, 1 * size, 184)
    LCD.fill_rect(4 * size + offset_hearts, 0 * size + 24 + vertical_offset, 1 * size, 2 * size, LCD.white)
    
    LCD.text(card_rank,22 + text_offset,12 + vertical_offset, LCD.black)
    LCD.show()

def clubs(card_rank,card_number):
    
    LCD.fill_rect(0 * card_size + offset_cards, 1 * card_size + vertical_offset, 9 * card_size, 12 * card_size, LCD.green)
    LCD.fill_rect(1 * card_size + offset_cards, 2 * card_size + vertical_offset, 7 * card_size, 10 * card_size, LCD.white)

    LCD.fill_rect(3 * size + offset_clubs, 8 * size + 24 + vertical_offset, 3 * size, 1 * size, 21083)
    LCD.fill_rect(0 * size + offset_clubs, 4 * size + 24 + vertical_offset, 9 * size, 3 * size, LCD.black)
    LCD.fill_rect(1 * size + offset_clubs, 3 * size + 24 + vertical_offset, 7 * size, 5 * size, LCD.black)
    LCD.fill_rect(2 * size + offset_clubs, 3 * size + 24 + vertical_offset, 5 * size, 1 * size, LCD.white)
    LCD.fill_rect(3 * size + offset_clubs, 7 * size + 24 + vertical_offset, 3 * size, 1 * size, LCD.white)
    LCD.fill_rect(4 * size + offset_clubs, 7 * size + 24 + vertical_offset, 1 * size, 3 * size, LCD.black)
    LCD.fill_rect(3 * size + offset_clubs, 0 * size + 24 + vertical_offset, 3 * size, 4 * size, LCD.black)
    LCD.fill_rect(2 * size + offset_clubs, 1 * size + 24 + vertical_offset, 5 * size, 2 * size, LCD.black)
    LCD.fill_rect(3 * size + offset_clubs, 9 * size + 24 + vertical_offset, 3 * size, 1 * size, LCD.black)
    
    LCD.text(card_rank,22 + text_offset,12 + vertical_offset, LCD.black)
    LCD.show()

def suite_selection(card_row,card_number,card_rank,card_suite):
    global offset_diamonds, offset_clubs, offset_spades, offset_hearts
    global offset_cards, text_offset, vertical_offset
    
    vertical_offset = row_offsets[card_row]
    card_number_offset = card_number_offsets.get(card_number, 0)
    
    
        
    offset_diamonds = 13 + card_number_offset
    offset_clubs = 9 + card_number_offset
    offset_spades = 9 + card_number_offset
    offset_hearts = 9 + card_number_offset
    offset_cards = card_number_offset
    text_offset = card_number_offset + 9

    # Use a dispatch dictionary for suite selection
    suite_functions = {
        "D": diamonds,
        "H": hearts,
        "S": spades,
        "C": clubs
    }

    if card_suite in suite_functions:
        suite_functions[card_suite](card_rank, card_number)

def reset_game():
    global dealer, player, shuffled_deck, balance, bet, blackjack_round_start
    LCD.fill(0)
    
    # Custom shuffling logic instead of `random.shuffle`
    deck = [rank + suit for suit in ['S', 'H', 'D', 'C'] for rank in 
        ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]
    shuffled_deck = sorted(deck, key=lambda x: random.random())

    dealer, player = [shuffled_deck.pop() for _ in range(2)], [shuffled_deck.pop() for _ in range(2)]
    
    bet_input()
    balance -= bet
    
    LCD.fill(0)
    
    for i in range(1, len(player) + 1):
        cards = player.copy()
        
        first_card = cards.pop(i - 1)
        
        current_suite = first_card[-1]
        current_card_value = first_card[:-1]
        
        suite_selection(1, i, current_card_value, current_suite)
        
    for i in range(1, len(dealer) + 1):
        cards = dealer.copy()
        
        first_card = cards.pop(i - 1)
        
        current_suite = first_card[-1]
        current_card_value = first_card[:-1]
        
        suite_selection(2, i, current_card_value, current_suite)
    
    '''
    FOR TESTING
    dealer = []
    player = []
    
    print("value first, suit second")
    for i in range(2):
        cards = input("eter dealers cards:")
        dealer.append(cards)
    for i in range(2):
        cards = input("eter players cards:")
        player.append(cards)
    '''
    
    print("\nNew Game!")
    print("Current balance:", balance)
    
    blackjack_round_start = 1

    print("Dealer's hand:", dealer, "-> Total Value:", hand_value(dealer))
    print("Player's hand:", player, "-> Total Value:", hand_value(player))
    
    LCD.text("h>",220, 30 , LCD.white)
    LCD.text("p>",220, 90 , LCD.white)
    LCD.text("d>",220, 145 , LCD.white)
    
    LCD.text(f"balance:{balance}",0,150, LCD.white)
    LCD.text(f"bet:{bet}",0,160, LCD.white)
    
    LCD.show()

def hit(player):
    player.append(shuffled_deck.pop())
    player_value = hand_value(player)
    card_number = 3
    
    print("Player's hand:", player, "-> Total Value:", player_value)
    
    LCD.text("h>",220, 30 , LCD.white)
    LCD.text("p>",220, 90 , LCD.white)
    LCD.text("d>",220, 145 , LCD.white)
     
    for i in range(1, len(player) + 1):
        cards = player.copy()
        
        first_card = cards.pop(i - 1)
        
        current_suite = first_card[-1]
        current_card_value = first_card[:-1]
        
        suite_selection(1, i, current_card_value, current_suite)
    
    if player_value > BLACKJACK:
        
        time.sleep(2)
        
        LCD.fill(0)
        
        print("PLAYER BUSTS")
        LCD.text("PLAYER LOSSES",70 ,100 , LCD.red)
        
        LCD.show()
        time.sleep(2)
        reset_game()
    
def pass1():
    dealer_turn()
    dealer_value = hand_value(dealer)  # Ensure dealer's value is updated after their turn
    game(player_value, dealer_value)
    
def double(player):
    global bet, balance,player_value,dealer_value
    
    player.append(shuffled_deck.pop())
    player_value = hand_value(player)
    card_number = 3
    
    print("Player's hand:", player, "-> Total Value:", player_value)
    
    LCD.text("h>",220, 30 , LCD.white)
    LCD.text("p>",220, 90 , LCD.white)
    LCD.text("d>",220, 145 , LCD.white)
     
    for i in range(1, len(player) + 1):
        cards = player.copy()
        
        first_card = cards.pop(i - 1)
        
        current_suite = first_card[-1]
        current_card_value = first_card[:-1]
        
        suite_selection(1, i, current_card_value, current_suite)
    
    time.sleep(2)
        
    print("Player's hand:", player, "-> Total Value:", player_value)
    
    balance -= bet
    bet += bet
    print("\nbet incrised to:", bet,"\n")
    
    if player_value > BLACKJACK:
        LCD.fill(0)
        
        print("PLAYER BUSTS")
        LCD.text("PLAYER BUSTS",70 ,100 , LCD.white)
        
        LCD.show()
        time.sleep(4.5)
        reset_game()
    else:
        dealer_turn()
        dealer_value = hand_value(dealer)   # Ensure dealer's value is updated after their turn
        game(player_value, dealer_value)
        reset_game()

last_pressed_time = 0  # Timestamp of the last button press
debounce_delay = 0.3  # 300ms debounce delay
balance_input()
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
                    
    time.sleep(0.05)
