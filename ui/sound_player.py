from pygame import mixer
from engine import GameEvent


class SoundPlayer:
    """
    Plays sound effects corresponding to different events in the chess game.
    """

    def __init__(self):
        """
        Initialize the sound player by starting the pygame mixer.
        """
        mixer.init()

    def handle_event(self, event):
        """
        Handle a game event by playing the corresponding sound effect.

        Args:
            event (GameEvent): The game event.
        """
        self.play_sound_effect(event)

    def play_sound_effect(self, event: GameEvent):
        """
        Play a sound effect corresponding to a game event.

        Args:
            event (GameEvent): The game event.
        """
        sound_path = self.get_sound_path(event)
        self.play_sound(sound_path)

    @staticmethod
    def get_sound_path(event: GameEvent) -> str:
        """
        Returns the sound file path corresponding to the game event.

        Args:
            event (GameEvent): The game event.

        Returns:
            str: The path to the sound file.
        """
        match event:
            case GameEvent.CAPTURE:
                return "sounds/capture.mp3"
            case GameEvent.CASTLE:
                return "sounds/castle.mp3"
            case GameEvent.PROMOTION:
                return "sounds/promote.mp3"
            case GameEvent.NOTIFICATION:
                return "sounds/notify.mp3"
            case GameEvent.CHECK:
                return "sounds/check.mp3"
            case GameEvent.CHECKMATE:
                return "sounds/checkmate.mp3"
            case _:
                return "sounds/move.mp3"

    @staticmethod
    def play_sound(sound_path: str):
        """
        Load and play a sound from the provided file path.

        Args:
            sound_path (str): The path to the sound file.
        """
        mixer.music.load(sound_path)
        mixer.music.play()
