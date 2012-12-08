
import os,sys
import yaml


class NotDirectoryError(Exception):

    pass

class DataError(Exception):

    pass

class BibObject(dict):

    def __init__(self,d,path):
        self.path=path
        dict.__init__(self,d)

    def save(self):
        f=file(self.path,"w")
        f.write(yaml.dump(dict(self)))
        f.close()


class Datadir(object):

    def __init__(self,dirname):

        self.bibobjects=[]
        self.orig_paths=[]
        self.dirname=dirname
        if os.path.isdir(dirname):
            for root,dirs,files in os.walk(dirname):
                for name in files:
                    if name.endswith(".yaml"):
                        path=os.path.join(root,name)
                        data=yaml.load(file(path))
                        if type(data) is not dict:
                            raise DataError("File %s does not contain a dictionary" % path)
                        self.orig_paths.append(path)
                        self.bibobjects.append(BibObject(data,path))
        else:
            raise NotDirectoryError("%s is not a directory" % dirname) 

    def __iter__(self):

        return iter(self.bibobjects)
        

