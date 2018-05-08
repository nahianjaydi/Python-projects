import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader

BASE_URL = "http://quotes.toscrape.com"


def read_quotes(filename):
    with open(filename, "r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def start_game(quotes):
    game_quote = choice(quotes)
    remaining_guesses = 4
    print("Here's a quote")
    print(game_quote["text"])
    print(game_quote["author"])
    guess = ""

    while guess.lower() != game_quote["author"].lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses}\n")
        if guess.lower() == game_quote["author"].lower():
            print("Congratulation!!! You Got It Right.")
            break
        remaining_guesses -= 1
        if remaining_guesses == 3:
            res = requests.get(f"{BASE_URL}{game_quote['bio_url']}")
            game_soup = BeautifulSoup(res.text, "html.parser")
            birth_date = game_soup.find(class_="author-born-date").get_text()
            birth_place = game_soup.find(class_="author-born-location").get_text()
            print(f"Here's a hint: The author was born in {birth_date} {birth_place}")
        elif remaining_guesses == 2:
            print(f"Hint: The author's first name start with: {game_quote['author'][0]}")
        elif remaining_guesses == 1:
            last_initial = game_quote["author"].split(" ")[1][0]
            print(f"Hint: The author's last name start with: {last_initial}")
        else:
            print(f"Sorry you ran out of guesses. The answer was {game_quote['author']}")

    print("Game Over!!")

    again = ""
    while again.lower() not in ("y", "yes", "n", "no"):
        again = input("Would you like to play again (y/n)?\n")
    if again.lower() in ("yes", "y"):
        return start_game(quotes)
    else:
        print("OK, Goodbye & Enjoy Life!!")


quotes = read_quotes("quotes.csv")
start_game(quotes)
