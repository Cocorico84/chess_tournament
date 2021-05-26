class HomeMenuView:
    def __init__(self, menu):
        self.menu = menu

    def _display_menu(self):
        print("\nWelcome to our chess manager:")
        for key, entry in self.menu.items():
            print(f"{key}: {entry.option}")

    def get_user_choice(self):
        while True:
            self._display_menu()
            choice = input(">> ")
            if choice in self.menu:
                return self.menu[choice]


class TournamentView:
    def get_info(self):
        tournament_name = input("What name do you want to call it ? ")
        tournament_location = input("Where is the location of your tournament ? ")
        tournament_round = int(input("How many rounds do you want ? "))
        print(f'Your tournament called "{tournament_name}" is created')
        return tournament_name, tournament_location, tournament_round


class PlayerView:
    def add_player(self):
        choice = input("Add a player in the database ? Y/N ")
        if choice == 'Y':
            player_first_name = input("What is the first name of the player ? ")
            player_last_name = input("What is the last name of the player ? ")
            player_birth = input("What is the birth ? DD-MM-YYYY")
            player_gender = input("What is the gender of the player ?")
            print(f'The player "{player_first_name} {player_last_name}" is created')
            return player_first_name, player_last_name, player_birth, player_gender
        else:
            existing_player_choice = input("Do you want to add an existing player in a tournament ? Y/N ")
            if existing_player_choice == 'Y':
                player_first_name = input("What is the first name of the player ? ")
                player_last_name = input("What is the last name of the player ? ")
                return player_first_name, player_last_name, None, None

    def choose_tournament_to_add_player(self):
        tournament = input("Which tournament is the player in ? ")
        print(f'The player has been added in "{tournament}" tournament')
        return tournament

    def get_first_name_last_name(self):
        player_first_name = input("What is the first name of the player ? ")
        player_last_name = input("What is the last name of the player ? ")
        player_rank = int(input("What is his current rank ? "))
        print(f"The rank of player {player_first_name} {player_last_name} is {player_rank}")
        return player_first_name, player_last_name, player_rank


class MatchView:
    def display_matches(self, pairs):
        print({i: pair for i, pair in enumerate(pairs, 0)})

    def get_match_played(self):
        choice = int(input("Which match has been played ? "))
        return choice

    def ask_if_draw(self):
        draw = input("Is it a draw ? Y/N ")
        return draw

    def get_the_winner(self):
        winner = int(input("Who's the winner ? "))
        return winner


class RoundView:
    def get_tournament_choice(self):
        choice = input("Which tournament do you want to launch round ? ")
        return choice

    def display_if_round_over(self, number):
        if number == 0:
            print('The round is over, a new round is automatically launched')
        else:
            print("The round is not over")


class ReportView:
    def __init__(self):
        self._choices = {
            1: "All players in alphabetical order",
            2: "All players in rank order",
            3: "All players of a tournament in alphabetical order",
            4: "All players of a tournament in rank order",
            5: "All tournaments",
            6: "All rounds of a tournament",
            7: "All matches of a tournament"
        }

    def _display_choices(self):
        for key, value in self._choices.items():
            print(f"{key}: {value}")

    def report_choice(self):
        self._display_choices()
        choice = int(input("What is your choice ? "))
        return choice

    def get_tournament_choice(self):
        choice = input("Which tournament do you want to see in details ? ")
        return choice


class QuitView:
    def __call__(self):
        print("Bye")
