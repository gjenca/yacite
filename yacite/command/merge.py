# -*- coding: utf-8 -*-

import sys

from yacite.types import Datadir
from yacite.exception import *
from yacite.types import BibRecord
import yacite.utils.sane_yaml as sane_yaml
from yacite.utils.misc import describe_record
from yacite.command.command import YaciteCommand

class Merge(YaciteCommand):


    help="merge records with datadir - see the docs for merge rules"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("datadir")
        subparser.add_argument("-u","--union",help="take union of lists - original and new",
            dest="uname",action="append",default=[])
        subparser.add_argument("-s","--set",help="replace orginal values by new value",
            dest="sname",action="append",default=[])
        subparser.add_argument("-v","--verbose",action="store_true",help="be verbose")
        subparser.add_argument("-q","--quiet",action="store_true",help="be quiet")

    def __init__(self,ns):
        self.verbose=ns.verbose
        self.quiet=ns.quiet
        self.datadir_name=ns.datadir
        self.datadir=Datadir(self.datadir_name)
        self.union_names=ns.uname
        self.set_names=ns.sname

    def execute(self):

        bounced_records=0
        bounced_fields_num=0
        for i,rec in enumerate(sane_yaml.load_all(sys.stdin)):
            if type(rec) is not dict:
                raise DataError("merge: expecting dict as %s in stream, got %s instead" % (describe_record(i,rec),type(rec)))
            matches=self.datadir.list_matching(rec)
            if len(matches)>1:
                raise DataError("merge: %s in stream matches multiple records in datadir" %  describe_record(i,rec))
            elif len(matches)==1:
                match=matches[0]
                bounced=False
                bounced_fields=[]
                for field_name in rec:
                    if field_name not in match:
                        print >>sys.stderr,"merge: SET %s[%s] to %s (new field)" %(match["key"],field_name,rec[field_name])
                        match[field_name]=rec[field_name]
                    elif match[field_name]!=rec[field_name]:
                        if field_name in self.set_names:
                            if not self.quiet:
                                print >>sys.stderr,"merge: SET %s[%s] to %s" %(match["key"],field_name,rec[field_name])
                            match[field_name]=rec[field_name]
                        elif field_name in self.union_names:
                            if type(rec[field_name]) is list and type(match[field_name]) is list:
                                if not set(match[field_name])>=set(rec[field_name]):
                                    match[field_name].extend(rec[field_name])
                                    match[field_name]=list(set(match[field_name]))
                                    if not self.quiet:
                                        print >>sys.stderr,"merge: SET %s[%s] to %s (union)" %(match["key"],field_name,match[field_name])
                            else:
                                raise DataError(
                                 "merge: union of non-lists requested: %s in stream, file='%s', name='%s"
                                % (describe_record(i,rec),match.path,field_name))
                        else:
                            bounced=True
                            bounced_fields_num+=1
                            bounced_fields.append(field_name)
                if bounced:
                    bounced_records=bounced_records+1
                    if self.verbose and bounced_fields:
                        print >>sys.stderr,"merge: %s, file '%s':fields %s bounced" % (describe_record(i,rec),match.path,",".join(bounced_fields))
                match.save()
            else:
                newrecord=BibRecord(rec,datadir=self.datadir)
                newrecord.dirty=True
                newrecord.save()
                self.datadir.append(newrecord)
                if not self.quiet:
                    print >>sys.stderr,"merge: Created new record: %s" % newrecord.path
        if bounced_fields_num and not self.quiet and not self.verbose:
            print >>sys.stderr,"merge: %d fields in %d records bounced" % (bounced_fields_num,bounced_records)
            print >>sys.stderr,"merge: Use -v to see identify these fields, use -q to supress this message."      
