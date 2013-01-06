# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand

class Dummy(YaciteCommand):


    help="dummy command"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("arg")
        subparser.add_argument("--option",action="store_true")
        subparser.add_argument("-m","--module",dest="module",action="append",help="module",default=[])


    def execute(self):
        print self.ns

        
        
