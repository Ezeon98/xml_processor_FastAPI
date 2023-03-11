"""Decorador para propiedades de clase"""

# pylint: disable=class-camelcase, invalid-name


class classproperty:
    """Decorator para propiedades de clase"""

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        """getter"""
        del owner_self
        return self.fget(owner_cls)
