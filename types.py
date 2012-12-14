# -*- coding: utf-8 -*-
import os,sys,errno,re
import yaml
import unicodedata
import tempfile
import shutil

from yacite.exception import *
from yacite.utils.sane_yaml import yaml_dump_encoded, yaml_load_as_unicode

w_pattern = re.compile('[\W_]+')

def just_alnum(x):
    return w_pattern.sub('',x)

def makekey(bi,datadir):

    if any(name not in bi for name in ("title","year","authors")):
        raise IncompleteDataError("Cannot create key without title, year and authors")
    author=u"".join(bi["authors"][0].split(u",")[0].lower().split())
    title=u""
    for w in bi["title"].split():
        w=just_alnum(w)
        title=title+w.lower()
        if len(title)>=4:
            break
    year=u"%s" % bi["year"]
    keyprefix=u"%s%s%s" % (author,year,title)
    if datadir is None:
        return keyprefix
    if keyprefix in datadir.keys:
        for i in range(1,10):
            key=u"%s-%d" % (keyprefix,i)
            if key not in datadir.keys:
                break
    else:
        key=keyprefix
    zkey=[]
    for c in unicodedata.normalize('NFKD',key):
        if not unicodedata.combining(c):
            zkey.append(c)
    key=u"".join(zkey)
    return(key)
                

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def clean_string(x):
    try:
        return just_alnum(unicode(x).lower())
    except:
        print type(x),x
        raise

def exists_and_is_almost_same(d1,d2,key):
    if (key in d1) and \
        (key in d2):
        if d1[key] == d2[key]:
            return True
        l1,l2 = (x[:] if type(x) is list else [x] for x in (d1[key],d2[key]))
        if len(l1) != len(l2):
            return False
        for l in l1,l2:
            for i,x in enumerate(l):
                l[i]=clean_string(x)
        l1.sort()
        l2.sort()
        return l1 == l2
    return False

class BibRecord(dict):

    def __init__(self,d,path=None,datadir=None):
        self.path=path
        self.datadir=datadir
        self.dirty=False
        dict.__init__(self,d)

    def __setitem__(self,key,value):
        self.dirty=True
        dict.__setitem__(self,key,value)


    def save(self):
        if not self.dirty:
            return
        if not "key" in self:
            self["key"]=makekey(self,self.datadir)
        if self.path is None:
            if self.datadir is None:
                raise SaveError("Cannot save: no path and no datadir given") 
            if not "year" in self:
                year="none"
            else:
                year=self["year"]
            if ("myown" in self) and self["myown"]:
                pathdir="%s/myown/%s/" % (self.datadir.dirname,year)
            else:
                pathdir="%s/%s/" % (self.datadir.dirname,year)
            mkdir_p(pathdir)
            self.path=pathdir+("%s.yaml" % self["key"].encode("ascii"))
        f=tempfile.NamedTemporaryFile(delete=False)
        f.write(yaml_dump_encoded(dict(self)))
        f.close()
        shutil.move(f.name,self.path)

    def match(self,other):
        
        if "key" in self and \
            "key" in other and\
            self["key"]==other["key"]:
            return True

        for k1 in ("article-number","art_number"):
            for k2 in ("article-number","art_number"):
                if k1 in self and k2 in other and self[k1]==other[k2]:
                    return True

        if all(exists_and_is_almost_same(self,other,key) \
            for key in ("title","year","authors")):
                return True

        if all(exists_and_is_almost_same(self,other,key) \
            for key in ("journal","volume","startpage")):
                return True

        return False

class Datadir(list):

    def append(self,bi):

        list.append(self,bi)
        if "key" in bi:
            self.keys.append(bi["key"])

    def __init__(self,dirname):

        list.__init__(self)
        self.dirname=dirname
        self.keys=[]
        if os.path.isdir(dirname):
            for root,dirs,files in os.walk(dirname):
                for name in files:
                    if name.endswith(".yaml"):
                        path=os.path.join(root,name)
                        data=yaml_load_as_unicode(file(path))
                        if type(data) is not dict:
                            raise DataError("File %s does not contain a dictionary" % path)
                        self.append(BibRecord(data,path=path,datadir=self))
        else:
            raise NotDirectoryError("%s is not a directory" % dirname) 


    def list_matching(self,pattern):
        
        return [bi for bi in self if bi.match(pattern)]
