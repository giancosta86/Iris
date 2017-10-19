"""
:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

import unittest

from info.gianlucacosta.iris.ioc import Container, TransientRegistration, SingletonRegistration


class MyIocClass:
    _instances = 0

    def __init__(self):
        MyIocClass._instances += 1
        self.val = 0

    def dispose(self):
        MyIocClass._instances -= 1


class ContainerTests(unittest.TestCase):
    def setUp(self):
        MyIocClass._instances = 0
        self._container = Container()


    def testInstanceScopeForRegisterTransient(self):
        self._container.registerTransient(MyIocClass, lambda container, key: MyIocClass())

        alpha = self._container.resolve(MyIocClass)
        beta = self._container.resolve(MyIocClass)

        alpha.val = 9
        beta.val = 10

        self.assertEquals(2, MyIocClass._instances)
        self.assertNotEquals(alpha.val, beta.val)


    def testInstanceScopeForRegisterSingleton(self):
        self._container.registerSingleton(MyIocClass, lambda container, key: MyIocClass())

        alpha = self._container.resolve(MyIocClass)
        beta = self._container.resolve(MyIocClass)

        alpha.val = 9
        beta.val = 10

        self.assertEquals(1, MyIocClass._instances)
        self.assertEquals(alpha.val, beta.val)


    def testAddRegistrationWhenUsingADuplicateKey(self):
        transientRegistration = TransientRegistration(lambda container, key: MyIocClass())
        singletonRegistration = SingletonRegistration(lambda container, key: MyIocClass())

        self._container.addRegistration(MyIocClass, transientRegistration)
        self.assertRaises(KeyError, self._container.addRegistration, MyIocClass, singletonRegistration)


    def testFactoryMethodWithTransientRegistration(self):
        self.assertRaises(ValueError, self._container.registerTransient, MyIocClass, None)


    def testFactoryMethodWithSingletonRegistration(self):
        self.assertRaises(ValueError, self._container.registerSingleton, MyIocClass, None)


    def testResolveWhenUsingAnUnknownKey(self):
        self.assertRaises(KeyError, self._container.resolve, "Unknown key")


    def testDisposeOnSingletonInstancesWhenADisposalFunctionIsPassed(self):
        self._container.registerSingleton(
            MyIocClass,
            lambda container, key: MyIocClass(),
            lambda instance: instance.dispose())

        self._container.resolve(MyIocClass)

        self._container.dispose()

        self.assertEquals(0, MyIocClass._instances)


    def testDisposeOnSingletonInstancesWhenNoDisposalFunctionIsPassed(self):
        self._container.registerSingleton(
            MyIocClass,
            lambda container, key: MyIocClass())

        self._container.resolve(MyIocClass)

        self._container.dispose()

        self.assertEquals(1, MyIocClass._instances)


    def testDisposeOnTransientInstances(self):
        self._container.registerTransient(MyIocClass, lambda container, key: MyIocClass())

        self._container.resolve(MyIocClass)
        self._container.resolve(MyIocClass)

        self._container.dispose()
        self.assertEquals(2, MyIocClass._instances)


    def testMethodChaining(self):
        self._container \
            .registerTransient(MyIocClass, lambda container, key: MyIocClass()) \
            .resolve(MyIocClass)

        self.assertEquals(1, MyIocClass._instances)