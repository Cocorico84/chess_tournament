class HomeMenuView:
    """
    Display the menu with choices the user can have
    """

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
    """
    This class contains function to get the tournament informations and choose which tournament is active
    """

    def get_info(self):
        tournament_name = input("What name do you want to call it ? ")
        tournament_location = input("Where is the location of your tournament ? ")
        tournament_round = int(input("How many rounds do you want ? "))
        tournament_description = input("Describe your tournament ")
        tournament_time_control = input("What is your time control? ")
        print(f'Your tournament called "{tournament_name}" is created')
        return tournament_name, tournament_location, tournament_round, tournament_description, tournament_time_control

    def tournament_in_progress_selected(self, tournaments: list):
        print("Tournament choices : ", [tournament.name for tournament in tournaments])
        choice = input("Which active tournaments do you want ? ")
        return choice

    def display_error_tournament_active(self):
        print("You have already a tournament in progress")


class PlayerView:
    """
    Retrieve player informations, which tournament add the player, and input to change the rank of the player
    """

    def add_player(self):
        choice = input("Add a player in the database ? Y/N ")
        if choice == 'Y':
            player_first_name = input("What is the first name of the player ? ")
            player_last_name = input("What is the last name of the player ? ")
            player_birth = input("What is the birth ? DD-MM-YYYY ")
            player_gender = input("What is the gender of the player ? ")
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
    """
    This view displays matches and retrieve the result of the match
    """

    def display_active_tournament(self, tournament):
        print(f"The tournament selected is {tournament}")

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
    """
    A view to print a sentence to show if the round is over or not.
    """

    def display_if_round_over(self, number):
        if number == 0:
            print('The round is over, a new round is automatically launched')
        else:
            print("The round is not over")

    def error_no_active_tournament(self):
        print("There is no active tournament, please create one before launching rounds")


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

    def display_players_report(self, players: list):
        for player in players:
            print(f"The first name of the player is {player.first_name}, the last name is {player.last_name}, the "
                  f"date of birth is {player.birth}, the gender is {player.gender}, the rank is {player.rank} an"
                  f"d has {player.point} points")

    def display_tournament(self, tournaments: list):
        for tournament in tournaments:
            print(f"The name of the tournament is {tournament.name}, based in {tournament.location}, has started at "
                  f"{tournament.date}, has {tournament.number_of_turns} rounds")

    def display_rounds(self, rounds):
        for round in rounds:
            for key, value in round.items():
                print(f"The round {key} has these matches : {value}")

    def display_matches(self, matches):
        for match in matches:
            if match['winner'] != 'D':
                print(f"The pair {match['pair']} has been played and the winner is {match['winner']}")
            else:
                print(f"The pair {match['pair']} has been played and it is a draw")

    def display_tournament_names(self, tournaments: list):
        print("Tournament choices : ", [tournament.name for tournament in tournaments])


class QuitView:
    def __call__(self):
        print("Bye")
