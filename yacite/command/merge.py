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
        subparser.add_argument("-d","--delete",help="delete these fields",
            dest="dname",action="append",default=[])
        subparser.add_argument("-v","--verbose",action="store_true",help="be verbose")
        subparser.add_argument("-q","--quiet",action="store_true",help="be quiet")

    def __init__(self,ns):
        super(Merge,self).__init__(ns)
        self.fields_to_change=self.ns.uname+self.ns.sname+self.ns.dname
        if len(self.fields_to_change)>len(set(self.fields_to_change)):
            raise DataError("merge: duplicite fieldnames in options")
        self.datadir=Datadir(self.ns.datadir)

    def execute(self):

        # 1. statistics
        bounced_fields_num=0
        bounced_records_num=0
        # 2. new_record, new_field, set, union, delete
        for i,rec in enumerate(sane_yaml.load_all(sys.stdin)):
            # 2.0. prepare:
            matches=self.datadir.list_matching(rec)
            if len(matches)>1:
                raise DataError("merge: %s in stream matches multiple records in datadir" \
                    % describe_record(i,rec))
            record_bounced=False
            if not matches:
                # 2.1 new record
                newrecord=BibRecord(rec,datadir=self.datadir)
                newrecord.dirty=True
                newrecord.save()
                self.datadir.append(newrecord)
                if not self.ns.quiet:
                    print >>sys.stderr,"merge: Created new record: %s" % newrecord.path
            else:
                match=matches[0]
                # 2.2. count bounced fields
                bounced_fields=[]
                for field_name in rec:
                    if field_name in match and match[field_name]!=rec[field_name] and field_name not in \
                        self.fields_to_change:
                            bounced_fields_num+=1
                            record_bounced=True
                            bounced_fields.append(field_name)
                if self.ns.verbose and bounced_fields:
                    print >>sys.stderr,"merge: %s, file '%s':fields %s bounced" \
                    % (describe_record(i,rec),match.path,",".join(bounced_fields))
                # 2.3. new_field
                for field_name in rec:
                    if field_name not in match:
                        if not self.ns.quiet:
                            print >>sys.stderr,"merge: SET %s[%s] to %s (new field)" \
                            % (match["key"],field_name,rec[field_name])
                        match[field_name]=rec[field_name]
                # 2.4. set
                for field_name in self.ns.sname:
                    if field_name in rec and field_name in match and match[field_name]!=rec[field_name]:
                        if not self.ns.quiet:
                            print >>sys.stderr,"merge: SET %s[%s] to %s" \
                                %(match["key"],field_name,rec[field_name])
                        match[field_name]=rec[field_name]
                # 2.5. union
                for field_name in self.ns.uname:
                    if type(rec[field_name]) is list and type(match[field_name]) is list:
                        if not set(match[field_name])>=set(rec[field_name]):
                            match[field_name].extend(rec[field_name])
                            match[field_name]=list(set(match[field_name]))
                            if not self.ns.quiet:
                                print >>sys.stderr,"merge: SET %s[%s] to %s (union)" \
                                    %(match["key"],field_name,match[field_name])
                    else:
                        raise DataError(
                            "merge: union of non-lists requested: %s in stream, file='%s', name='%s"
                            % (describe_record(i,rec),match.path,field_name))
                # 2.6. delete
                for field_name in self.ns.dname:
                    if field_name in match:
                        match.dirty=True
                        del match[field_name]
                        if not self.ns.quiet:
                            print >>sys.stderr,"merge: DELETE %s[%s]" % (match["key"],field_name)
                # 3. save changes
                match.save()
            if record_bounced:
                bounced_records_num+=1
        if bounced_fields_num and not self.ns.quiet:
            print >>sys.stderr,"merge: %d fields in %d records bounced" % (bounced_fields_num,bounced_records_num)
            if not self.ns.verbose:
                print >>sys.stderr,"merge: Use -v to see identify these fields, use -q to supress this message."
