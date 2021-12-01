class StateMachine:
    def __init__(self, states):
        self.__states = states

    def update(self, player_view, commands):
        while len(self.__states) > 0 and self.__states[0].finished(player_view):
            del self.__states[0]
        if len(self.__states) > 0:
            self.__states[0].update(player_view, commands)

    def finished(self):
        return len(self.__states) == 0
