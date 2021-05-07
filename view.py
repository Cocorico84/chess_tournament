from tinydb import Query


class HomeMenuView:
    def __init__(self, menu):
        self.menu = menu

    def _display_menu(self):
        print("\nAccueil de notre jeu:")
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
        print(f'Your tournament called "{tournament_name}" is created')
        return tournament_name


class PlayerView:
    def get_info(self):
        player_name = input("What is the name of the player ? ")
        print(f'The player "{player_name}" is created')
        return player_name


class MatchView:
    def _display_matches(self, pairs):
        print({i: pair for i, pair in enumerate(pairs, 0)})

    def get_match_played(self):
        choice = int(input("Which match has been played ? "))
        return choice

    def get_the_winner(self):
        winner = int(input("Who's the winner ? "))
        return winner


class ReportView:
    def __init__(self):
        self._choices = {
            1: ("All players in alphabetical order", self.players_alpha_report),
            2: ("All players in rank order", self.players_ranking_report),
            3: ("All players of a tournament in alphabetical order", self.players_alpha_report),
            4: ("All players of a tournament in rank order", self.players_ranking_report),
            5: ("All tournaments", self.get_all_tournaments),
            6: ("All rounds of a tournament", self.get_rounds_of_tournament),
            7: ("All matches of a tournament", self.get_matches_of_tournament)
        }

    def _display_choices(self):
        for key, value in self._choices.items():
            print(f"{key}: {value[0]}")

    def report_choice(self):
        self._display_choices()
        choice = input("What is your choice ? ")
        return choice

    def players_alpha_report(self, db, tournament=None):
        '''
        assure all players have a last name
        '''
        for player in sorted(db.load_player_data(), key=lambda x: x.last_name):
            print(player)

    def players_ranking_report(self, db, tournament=None):
        for player in sorted(db.load_player_data(), key=lambda x: x.rank, reverse=True):
            print({'first_name': player.first_name, 'last_name': player.last_name, 'ranking': player.rank})

    def get_all_tournaments(self, db=None):
        for tournament in db.load_tournament_data():
            print(tournament)

    def get_rounds_of_tournament(self, db=None, tournament_choice=None):
        tournaments_table = db.table("tournaments")
        tournament = Query()
        rounds = tournaments_table.search(tournament[tournament_choice])
        for round in rounds:
            print(round)

    def get_matches_of_tournament(self, db=None, tournament_choice=None):
        tournaments_table = db.table("tournaments")
        tournament = Query()
        matches = tournaments_table.search(tournament[tournament_choice])
        for match in matches:
            print(match)


class QuitView:
    def __call__(self):
        print("Bye")
