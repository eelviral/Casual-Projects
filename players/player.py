from utils import TeamType


class Player:
    """
    A class to represent a player in the game of Chess.
    """

    def __init__(self, name: str, team: TeamType):
        """
        Initializes a Player with a name and a team.

        Args:
            name (str): The name of the player.
            team (TeamType): The team that the player belongs to.
        """
        self.name = name
        self.team = team
