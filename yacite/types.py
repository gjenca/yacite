# -*- coding: utf-8 -*-
import os,sys,errno,re
import yaml
import unicodedata
import tempfile
import shutil

from yacite.exception import *
import yacite.utils.sane_yaml as sane_yaml
from yacite.utils.misc import strip_accents

w_pattern = re.compile('[\W_]+')

def just_alnum(x):
    return w_pattern.sub('',x)

def makekey(bib_rec,datadir):

    if any(name not in bib_rec for name in ("title","year","authors")):
        raise IncompleteDataError("Cannot create key without title, year and authors")
    author="".join(bib_rec["authors"][0].split(",")[0].lower().split())
    title=""
    for w in bib_rec["title"].split():
        w=just_alnum(w)
        title=title+w.lower()
        if len(title)>=4:
            break
    year="%s" % bib_rec["year"]
    keyprefix="%s%s%s" % (author,year,title)
    keyprefix=strip_accents(keyprefix)
    if datadir is None:
        return keyprefix
    if keyprefix in datadir.keys:
        for i in range(1,10):
            key="%s-%d" % (keyprefix,i)
            if key not in datadir.keys:
                break
    else:
        key=keyprefix
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
        return just_alnum(str(x).lower())
    except:
        print(type(x),x)
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
        if "year" not in self:
            self["year"]="NOYEAR"
        if "title" not in self:
            self["title"]="NOTITLE"
        if not "key" in self:
            self["key"]=makekey(self,self.datadir)
        if self.path is None:
            if self.datadir is None:
                raise SaveError("Cannot save: no path and no datadir given")
            if ("myown" in self) and self["myown"]:
                pathdir="%s/myown/%s/" % (self.datadir.dirname,self["year"])
            else:
                pathdir="%s/%s/" % (self.datadir.dirname,self["year"])
            mkdir_p(pathdir)
            self.path=pathdir+("%s.yaml" % self["key"])
        f=tempfile.NamedTemporaryFile(delete=False,mode="w")
        f.write(sane_yaml.dump(dict(self)))
        f.close()
        shutil.move(f.name,self.path)

    def _same_position(self,other):

        for k1 in ("article-number","art_number","article_number"):
            for k2 in ("article-number","art_number","article_number"):
                if k1 in self and k2 in other and self[k1]==other[k2] and \
                    (exists_and_is_almost_same(self,other,"volume") \
                        or ("volume" not in self and "volume" not in other)) and \
                    (exists_and_is_almost_same(self,other,"number") \
                        or ("number" not in self and "number" not in other)):
                    return True

        if all(exists_and_is_almost_same(self,other,key) \
            for key in ("volume","startpage")):
                return True

        return False

    def _same_source(self,other):

        return any(exists_and_is_almost_same(self,other,key) \
            for key in ("journal","series"))

    def same_authors(self,other,preprocess=lambda x: x):

        def _surname(author):
            return "".join(author.split(",")[0].lower().split())

        if "authors" in self and "authors" in other:
            if len(self["authors"])!=len(other["authors"]):
                return False
            l1=[_surname(preprocess(author)) for author in self["authors"]]
            l2=[_surname(preprocess(author)) for author in other["authors"]]
            l1.sort()
            l2.sort()
            return l1==l2
        return False

    def match(self,other):

        # if keys are present, it is trivial
        if "key" in self and "key" in other:
            return self["key"]==other["key"]

        # a distinct startpage, both greater than 1
        # means no match
        if "startpage" in self and "startpage" in other and \
            (type(self["startpage"]) is not int or self["startpage"]>1) and \
            (type(self["startpage"]) is not int or self["startpage"]>1) and \
            self["startpage"]!=other["startpage"]:
            return False

        # distinct length (not too short) means no match
        try:
            self_l=self["endpage"]-self["startpage"]
            other_l=other["endpage"]-other["startpage"]
            if self_l>2 and other_l>2 and self_l!=other_l:
                return False
        except:
            # non numeric page numbers
            pass

        if self.same_authors(other) and all(exists_and_is_almost_same(self,other,key) \
            for key in ("title","year")):
            return True

        same_position=self._same_position(other)

        if same_position and exists_and_is_almost_same(self,other,"title"):
            return True

        if same_position and self._same_source(other):
            return True

        return False

class Datadir(list):

    def append(self,bib_rec):

        list.append(self,bib_rec)
        if "key" in bib_rec:
            self.keys[bib_rec["key"]]=bib_rec

    def __init__(self,dirname):

        list.__init__(self)
        self.keys={}
        self.dirname=dirname
        if os.path.isdir(dirname):
            for root,dirs,files in os.walk(dirname):
                for name in files:
                    if name.endswith(".yaml"):
                        path=os.path.join(root,name)
                        data=sane_yaml.load(open(path))
                        if type(data) is not dict:
                            raise DataError("File %s does not contain a dictionary" % path)
                        self.append(BibRecord(data,path=path,datadir=self))
        else:
            raise NotDirectoryError("%s is not a directory" % dirname)


    def list_matching(self,pattern):

        if "key" in pattern and pattern["key"] in self.keys:
            return [self.keys[pattern["key"]]]
        else:
            return [bib_rec for bib_rec in self if bib_rec.match(pattern)]
