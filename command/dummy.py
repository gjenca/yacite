# -*- coding: utf-8 -*-


class Dummy(object):


    help="dummy command"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("arg")
        subparser.add_argument("--option",action="store_true")
        subparser.add_argument("-m","--module",dest="module",action="append",help="module",default=[])

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        print self.ns

        
        
