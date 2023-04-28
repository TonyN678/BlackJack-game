from oop import Card
import random
import subprocess  # needed to clear the console


# The symbol or the suit for the cards
HEARTS = chr(9829)  # Character 9829 is '♥'.
DIAMONDS = chr(9830)  # Character 9830 is '♦'.
SPADES = chr(9824)  # Character 9824 is '♠'.
CLUBS = chr(9827)  # Character 9827 is '♣'.


# (A list of chr codes is at https://inventwithpython.com/charactermap)
# overscore = u'\ufe26'  # unicode for the sign " Combining conjoining macron "
# low_line = u'\u0332'   # unicode for the sign " low line "


suit_list = [HEARTS, DIAMONDS, CLUBS, SPADES]  # list of all the suit
rank_list = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']  # list of all the card rank
card_deck = []  # the list of all cards( Card class includes suit+rank ) in the deck


# function to put all Card(rank, suit) objects in a list
# The cards will be in the form of an object (rank, suit)
def make_list_of_card():
    for rank_Element in rank_list:
        for suit_Element in suit_list:
            object1 = Card(rank_Element, suit_Element)  # object1 is an instance of Card class
            card_deck.append(object1)  # insert the card object "object1" into the card_deck
    # NC/ print(card_deck) --> for review error


# both_Card[[0], [1]] is nested list, 0 is player card, 1 is dealer card
both_Card = [[], []]


# function to randomly give out 2 cards for both player and dealer
def card_deal():
    for i in range(0, 2):
        player_card = random.choice(card_deck)  # pick a random card from the card_deck
        both_Card[0].append(player_card)  # put that random card into the player's hand at index 0
        card_deck.remove(player_card)  # remove that random card from the card_deck to avoid repetition
        dealer_card = random.choice(card_deck)
        both_Card[1].append(dealer_card)
        card_deck.remove(dealer_card)
# NC/   print(f"Your cards: {both_Card[0]}")  --> for review error


# get the total value of a hand
# the value is taken from the list "both_Card[]" at index 0 or 1
def get_hand(hand):
    value = 0
    for card in hand:
        if str(card.rank) in ('K', 'Q', 'J'):  # Face cards are worth 10 points.
            value += 10
        elif str(card.rank) in "A":
            if 11 + value > 21:
                value += 1  # Ace is worth 1 if the hand's value exceeds 21 when adding 11
            else:
                value += 11  # Ace is worth 11 if the hand's value NOT exceeds 21 when adding 11
        else:
            value += card.rank  # The other card worth their own ranks
    return value


# function to illustrate the card interface
# which based on the person which is Dealer(not show) or Player(show)
def card_print(lists, card_display='FRONT'):
    rows = ['', '', '', '', '', '']  # The text to display on each row.
#    rows[0] += ' ___  '

    for card in lists:
        if card_display == 'BACK':  # Print a card's back( for dealer card)
            if lists.index(card) == 0:  # the dealer's hand will be print with 1 up and 1 down
                rows[0] += ' ___  '
                rows[1] += '|{} | '.format(str(card.rank).ljust(2))  # move the number left by 2 units
                rows[2] += '| {} | '.format(card.suit)  # the suit image will be at the middle
                rows[3] += '| {}| '.format(str(card.rank).rjust(2, '_'))  # move the number right 2 units, put '_' there
            else:
                rows[0] += ' ___  '
                rows[1] += '|## | '
                rows[2] += '|###| '
                rows[3] += '|_##| '
        else:  # print the card front face for player's card
            rows[0] += ' ___  '
            rows[1] += '|{} | '.format(str(card.rank).ljust(2))
            rows[2] += '| {} | '.format(card.suit)
            rows[3] += '| {}| '.format(str(card.rank).rjust(2, '_'))

    for row in rows:
        print(row)  # print all the row in the list, which is the parts of card interface


# This function prints out the Dealer and Player cards, the scores
# 'val' attribute is the status signalling the stage of the game
def print_funct(val):
    if val == 'playing':  # At the start of the game when the player still want to draw
        print("Dealer's card:")
        card_print(both_Card[1], card_display='BACK')
        print("Player's card:")
        card_print(both_Card[0], card_display='FRONT')
        hand = get_hand(both_Card[0])
        print("Score: " + str(hand))
    elif val == 'ending':  # At the end of the game when everyone need to show their hands
        print("Dealer's card:")
        card_print(both_Card[1], card_display='FRONT')
        hand_dealer = get_hand(both_Card[1])
        print("Score: " + str(hand_dealer))
        print("\nPlayer's card:")
        card_print(both_Card[0], card_display='FRONT')
        hand = get_hand(both_Card[0])
        print("Score: " + str(hand))


# the function is used to ask the player
# if he wants to draw or stay first,
# then the dealer algorithm for drawing card
# and the result of the round winner
def after_math():
    # function to ask for player choice, Draw or Stay
    for i in range(1, 11):
        print_funct("playing")  # print both side cards at status:playing

        # i >= 2 means at index 2 is the third card drawn
        if i > 1:
            card_deck.remove(both_Card[0][i])  # remove the third card to avoid repetition

        # Ask the player's decision to Draw or Stay
        player_input = input("Want to Draw or Stay: D/S ? ")
        if player_input in "D":
            subprocess.call('cls', shell=True)  # clear the console
            both_Card[0].append(random.choice(card_deck))  # insert a third card into the player's hand
#  NC/      print(f" Your cards: {both_Card[0]}\n{get_hand(both_Card[0])}")  # f-string to print 2 variables on 2 lines

            # player's hand value exceed 21 == stop drawing
            if get_hand(both_Card[0]) > 21:
                break

        # Player chose to Stay == stop drawing
        elif player_input in "S":
            break

    # Algorithm that decides if the dealer should stay or draw
    for i in range(1, 11):
        if get_hand(both_Card[1]) < 17:
            both_Card[1].append(random.choice(card_deck))
            if i > 1:
                card_deck.remove(both_Card[1][i])
            if get_hand(both_Card[1]) > 21:
                # print(f"{both_Card[1]}\n{get_hand(both_Card[1])}")
                break
            elif 17 <= get_hand(both_Card[1]) <= 21:
                # print(f"{both_Card[1]}\n{get_hand(both_Card[1])}")
                break
            else:
                pass

#    print(f" Dealer' cards: {both_Card[1]}\n{get_hand(both_Card[1])}")
    subprocess.call('cls', shell=True)
    print_funct("ending")

    # Check if both hands are less than or equal to 21
    if get_hand(both_Card[1]) < 22 and get_hand(both_Card[0]) < 22:
        # Check if both hands have the same value
        if get_hand(both_Card[1]) == get_hand(both_Card[0]):
            print("\nGuess that we're even now, Good Game")
        # Check if dealer's hand is less than the player's hand
        elif get_hand(both_Card[1]) < get_hand(both_Card[0]):
            print("\nYou've won  :))")
            return 'WIN'
        # Dealer's hand is greater than player's hand
        else:
            print("\nUnlucky :<")
            return 'LOSE'
    # Check if dealer's hand is greater than 21 and player's hand is less than or equal to 21
    elif get_hand(both_Card[1]) > 21 and get_hand(both_Card[0]) < 22:
        print("\nCheers, you won >_<")
        return 'WIN'
    # Check if player's hand is greater than 21 and dealer's hand is less than or equal to 21
    elif get_hand(both_Card[1]) < 22 and get_hand(both_Card[0]) > 21:
        print("\nForget it :______")
        return 'LOSE'
    # Neither the player nor the dealer wins
    else:
        print("\nOk never-mind that")


def balance_monitor():
    # Set the initial player balance to 10000
    player_balance = 10000

    # Keep playing while the player has money left
    while player_balance > 0:
        # Display the player's current balance
        print("You're currently have: " + str(player_balance) + " dollars")

        # Ask the player how much they want to bet
        bet_val = int(input("How much you want to bet: "))

        # If the bet is higher than the player's available funds, issue a warning
        if bet_val > player_balance:
            print("Warning: Your input amount is higher than your available funds.")
        else:
            # Otherwise, proceed with the game
            make_list_of_card()
            card_deal()
            player_status = after_math()

            # If the player wins, add the bet amount to their balance
            if player_status == 'WIN':
                player_balance += bet_val

            # If the player loses, subtract the bet amount from their balance
            elif player_status == 'LOSE':
                player_balance -= bet_val

            # If it's a tie, do nothing
            else:
                player_balance += 0

            # Display the player's updated balance
            print("\nYour balance is: " + str(player_balance))

            # Clear the cards from the game
            for sub_list in both_Card:
                sub_list.clear()

            # Ask the player if they want to play another round
            while True:
                opinion = input("\nAnother round (Y/N) ?  ")
                subprocess.call('cls', shell=True)

                # If they enter an invalid letter, ask again
                if opinion not in ('Y', 'N'):
                    print("Wrong letter, choose again !!!")
                else:
                    break

            # If they choose not to play another round, exit the loop
            if opinion == 'N':
                break

    # Display the player's final balance
    print("Your total balance is now:  " + str(player_balance) + "dollars")


# Call the balance_monitor function to start the game
balance_monitor()


# hello

