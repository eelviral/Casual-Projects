from engine.game_event import GameEvent


class GameEventNotifier:
    """
    A class that manages and broadcasts game events to all subscribed observers during a chess game.

    It maintains a list of subscribed observers and informs them when specific game events occur,
    such as a move being made, a checkmate, a stalemate, or a pawn promotion. Observers are expected to
    handle these events using a ``handle_event()`` method.
    """

    def __init__(self):
        """
        Construct a new GameEventNotifier object with an empty list of observers.

        Observers can be added to this list with the subscribe method and will then receive notifications
        of all game events.
        """
        self._observers = []

    def subscribe(self, observer):
        """
        Add an observer to the list of subscribers that get notified of game events.

        The observer object should have a ``handle_event()`` method which will be called when a game event occurs.

        Args:
            observer: An object subscribing to game events. It should have a ``handle_event()`` method.
        """
        self._observers.append(observer)

    def notify(self, event: GameEvent):
        """
        Notify all subscribed observers of a specific game event by calling their ``handle_event()`` method.

        The game event will be passed as an argument to the observer's ``handle_event()`` method.

        Args:
            event (GameEvent): The event that has occurred in the game.
        """
        for observer in self._observers:
            observer.handle_event(event)
