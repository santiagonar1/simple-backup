#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Problem description:

Author: Santiago Narváez Rivas.
Date:
"""
class Observable:
    def __init__(self):
        self._observers = set()

    def add_observer(self, observer):
        self._observers.add(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, event):
        for observer in self._observers:
            observer.update(self, event)


class Observer:
    def update(self, observable, event):
        raise NotImplemented('This method is Abstract!')



