class GameEventNotifier:
    """
    Manages event notifications for the chess game.

    Keeps track of subscribed observers and notifies them when game events occur.
    """

    def __init__(self):
        """
        Initialize a GameEventNotifier with an empty list of observers.
        """
        self._observers = []

    def subscribe(self, observer):
        """
        Add an observer to the list of subscribers.

        Args:
            observer: The observer to be added to the list of subscribers.
        """
        self._observers.append(observer)

    def notify(self, event):
        """
        Notify all subscribed observers of a specific game event.

        Args:
            event: The event that has occurred.
        """
        for observer in self._observers:
            observer.handle_event(event)
