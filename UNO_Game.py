import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Install Pillow if needed: pip install pillow
import random

# Constants for game configuration
color = ('RED', 'GREEN', 'BLUE', 'YELLOW')
rank = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw2', 'Draw4', 'Wild')
ctype = {
    '0': 'number', '1': 'number', '2': 'number', '3': 'number', '4': 'number',
    '5': 'number', '6': 'number', '7': 'number', '8': 'number', '9': 'number',
    'Skip': 'action', 'Reverse': 'action', 'Draw2': 'action',
    'Draw4': 'action_nocolor', 'Wild': 'action_nocolor'
}

# Card class
class Card:
    def __init__(self, color, rank):
        self.rank = rank
        self.color = color if ctype[rank] != 'action_nocolor' else None
        self.cardtype = ctype[rank]

    def __str__(self):
        return f"{self.color or ''} {self.rank}".strip()

    def get_image_path(self):
        if self.color:
            return f"assets/{self.color}_{self.rank}.png"
        else:
            return f"assets/{self.rank}.png"

# Deck class
class Deck:
    def __init__(self):
        self.deck = []
        for clr in color:
            for ran in rank:
                if ctype[ran] != 'action_nocolor':
                    self.deck.append(Card(clr, ran))
                    self.deck.append(Card(clr, ran))
                else:
                    self.deck.append(Card(clr, ran))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

# Hand class
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, index):
        return self.cards.pop(index)

    def no_of_cards(self):
        return len(self.cards)

# Game Logic Functions
def single_card_check(top_card, card):
    """Checks if a card is valid to play."""
    return (
        card.color == top_card.color or
        card.rank == top_card.rank or
        card.cardtype == 'action_nocolor'
    )

def play_action_card(card):
    """Handles action card effects."""
    global turn, top_card
    if card.rank == 'Skip':
        turn = 'Player' if turn == 'Pc' else 'Pc'
    elif card.rank == 'Reverse':
        turn = 'Player' if turn == 'Pc' else 'Pc'
    elif card.rank == 'Draw2':
        for _ in range(2):
            (pc_hand if turn == 'Player' else player_hand).add_card(deck.deal())
    elif card.rank == 'Draw4':
        for _ in range(4):
            (pc_hand if turn == 'Player' else player_hand).add_card(deck.deal())
        choose_color(card)
    elif card.rank == 'Wild':
        choose_color(card)

def choose_color(card):
    """Prompts the user to choose a color for Wild and Draw4 cards."""
    def set_color(selected_color):
        card.color = selected_color
        update_top_card()
        color_window.destroy()

    color_window = tk.Toplevel(root)
    color_window.title("Choose a Color")
    for clr in color:
        btn = tk.Button(color_window, text=clr, bg=clr.lower(), command=lambda clr=clr: set_color(clr))
        btn.pack(fill=tk.BOTH)

def update_top_card():
    """Updates the top card display."""
    card_image = ImageTk.PhotoImage(Image.open(top_card.get_image_path()).resize((100, 150)))
    top_card_label.config(image=card_image)
    top_card_label.image = card_image
    current_card_label.config(text=f"Current Card: {top_card}")

def update_hand():
    """Displays the player's cards."""
    for widget in player_frame.winfo_children():
        widget.destroy()
    for idx, card in enumerate(player_hand.cards):
        card_image = ImageTk.PhotoImage(Image.open(card.get_image_path()).resize((100, 150)))
        btn = tk.Button(player_frame, image=card_image, command=lambda idx=idx: play_card(idx))
        btn.image = card_image  # Keep reference
        btn.pack(side=tk.LEFT)

def update_pc_status():
    """Updates the PC's card count display."""
    pc_status_label.config(text=f"PC has {pc_hand.no_of_cards()} cards")

def pc_turn():
    """Handles the PC's turn."""
    global top_card, turn
    playable_card = next((card for card in pc_hand.cards if single_card_check(top_card, card)), None)
    if playable_card:
        pc_hand.cards.remove(playable_card)
        top_card = playable_card
        update_top_card()
        if top_card.cardtype == 'action':
            play_action_card(top_card)
        if pc_hand.no_of_cards() == 0:
            messagebox.showinfo("UNO", "PC Wins!")
            root.quit()
    else:
        pc_hand.add_card(deck.deal())
    update_pc_status()
    turn = 'Player'

def play_card(idx):
    """Handles the player's action to play a card."""
    global top_card, turn
    card = player_hand.cards[idx]
    if single_card_check(top_card, card):
        player_hand.remove_card(idx)
        top_card = card
        update_top_card()
        update_hand()
        if top_card.cardtype == 'action':
            play_action_card(top_card)
        if player_hand.no_of_cards() == 0:
            messagebox.showinfo("UNO", "You Win!")
            root.quit()
        turn = 'Pc'
        pc_turn()
    else:
        messagebox.showerror("UNO", "Invalid Card!")

def pull_card():
    """Handles the player pulling a card from the deck."""
    card = deck.deal()
    player_hand.add_card(card)
    update_hand()

# Game Setup
deck = Deck()
deck.shuffle()

player_hand = Hand()
pc_hand = Hand()
for _ in range(7):
    player_hand.add_card(deck.deal())
    pc_hand.add_card(deck.deal())

top_card = deck.deal()
while top_card.cardtype == 'action_nocolor':
    top_card = deck.deal()

turn = 'Player'

# GUI Setup
root = tk.Tk()
root.title("UNO Game")

# Top Card Display
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

top_card_label = tk.Label(top_frame, text="Top Card", bg="white")
top_card_label.pack()

current_card_label = tk.Label(top_frame, text=f"Current Card: {top_card}", font=("Arial", 14))
current_card_label.pack()

# Player Hand Display
player_frame = tk.Frame(root)
player_frame.pack(pady=10)

# Action Buttons
pull_button = tk.Button(root, text="Pull Card", font=("Arial", 14), command=pull_card)
pull_button.pack(pady=5)

# PC Status
pc_status_label = tk.Label(root, text=f"PC has {pc_hand.no_of_cards()} cards", font=("Arial", 16))
pc_status_label.pack(pady=5)

# Initial Display Updates
update_top_card()
update_hand()
update_pc_status()

# Main Loop
root.mainloop()
