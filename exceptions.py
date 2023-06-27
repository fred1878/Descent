class Impossible(Exception):
    """Exception raised when an action is impossible to be performed.

    The reason is given as the exception message. Use raise Impossible("An exception message")
    """


class QuitWithoutSaving(SystemExit):
    """Can be raised to exit the game without automatically saving."""


class RoomNotFound(Exception):
    """ Exception raised when attempting to generate a room which has a type
    that has not been accounted for"""
