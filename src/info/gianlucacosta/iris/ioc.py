"""
Inversion of Control utilities

:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""


class ContainerRegistration:
    """
    Generic IoC container registration.

    It can be used to create new registration systems.
    """

    def resolve(self, container, key):
        """
        Called whenever the related container is asked to resolve a key
        """
        raise NotImplementedError


    def dispose(self):
        """
        Called when dispose() is called on the related container
        """
        raise NotImplementedError


class TransientRegistration(ContainerRegistration):
    """
    Registers an object in a way that every call to the container's resolve()
    method returns a new object instance, that the container does not track:
    disposal of every instance is left to the client.
    """

    def __init__(self, factoryMethod):
        """
        The passed factory method will be called to create each object instance;
        the arguments passed each time are (container, key)
        """
        if factoryMethod is None:
            raise ValueError("Invalid factory method")

        self._factoryMethod = factoryMethod


    def resolve(self, container, key):
        return self._factoryMethod(container, key)


    def dispose(self):
        pass


class SingletonRegistration(ContainerRegistration):
    """
    Registers an object in a way that it's instantiated whenever it's resolved
    for the first time: subsequent calls to resolve() will return the same instance.
    """

    def __init__(self, factoryMethod, disposeMethod=None):
        """
        --factoryMethod is the factory method called when the singleton instance is created:
          its parameters are (container, key)

        --disposeMethod is optional. If specified, it's called, if the instance was created,
          when the container's dispose() method is called; it takes a single parameter: (instance)
        """
        if factoryMethod is None:
            raise ValueError("Invalid factory method")

        self._factoryMethod = factoryMethod
        self._disposeMethod = disposeMethod
        self._instance = None


    def resolve(self, container, key):
        if self._instance is None:
            self._instance = self._factoryMethod(container, key)

        return self._instance


    def dispose(self):
        instance = self._instance

        if (instance is not None) and (self._disposeMethod is not None):
            self._disposeMethod(instance)


class Container:
    """
    A simple IoC container. It supports transient and singleton registrations out of the box,
    but new registrations types can be created via OOP.
    """

    def __init__(self):
        self._registrations = {}


    def addRegistration(self, key, registration):
        """
        Binds an IoC registration to a given key. It should be used if you
        introduce custom registrations; otherwise, registerTransient() and registerSingleton()
        are usually shorter and simpler.
        Registering a key twice raises a KeyError.
        """
        if key in self._registrations:
            raise KeyError("Key already registered")

        self._registrations[key] = registration
        return self


    def registerTransient(self, key, factoryMethod):
        """
        Binds a factory method to a key: whenever the requested key is resolved,
        a new instance is created by calling factoryMethod(container, key).

        Transient instances are not managed by the container - it's up to the client
        to dispose of them.
        """
        return self.addRegistration(key, TransientRegistration(factoryMethod))


    def registerSingleton(self, key, factoryMethod, disposeMethod=None):
        """
        Binds a singleton instance to a key: whenever the requested key is resolved,
        if the instance is still None, it is created by calling factoryMethod(container, key);
        otherwise, it is just returned.

        When the client calls dispose() on the container, disposeMethod(instance) is called
        if the instance was previously created.
        """
        return self.addRegistration(key, SingletonRegistration(factoryMethod, disposeMethod))


    def resolve(self, key):
        """
        Resolves the requested key to an object instance, raising a KeyError if the key is missing
        """
        registration = self._registrations.get(key)

        if registration is None:
            raise KeyError("Unknown key: '{0}'".format(key))

        return registration.resolve(self, key)


    def dispose(self):
        """
        Disposes every performed registration; the container can then be used again
        """
        for registration in self._registrations.values():
            registration.dispose()

        self._registrations = {}