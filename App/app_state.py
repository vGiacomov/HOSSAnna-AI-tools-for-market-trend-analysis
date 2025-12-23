from PySide6.QtCore import QObject, Signal


class AppStateSignal(QObject):
    changed = Signal()  # Sygnał zmiany stanu (język lub motyw)


_signal_emitter = AppStateSignal()


class AppState:
    _current_language = "English"
    _current_theme = "light"

    state_changed = _signal_emitter.changed

    @classmethod
    def get_language(cls):
        return cls._current_language

    @classmethod
    def set_language(cls, language):
        if cls._current_language != language:
            cls._current_language = language
            cls.state_changed.emit()  # Powiadom wszystkich o zmianie!

    @classmethod
    def get_theme(cls):
        return cls._current_theme

    @classmethod
    def set_theme(cls, theme):
        if cls._current_theme != theme:
            cls._current_theme = theme
            cls.state_changed.emit()  # Powiadom wszystkich o zmianie!
