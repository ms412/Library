
__author__ = 'oper'

import yaml
import json

class DictTreeLib(object):
    '''
    Dictionary Tree Object Library
    handles nested dictionary trees
    '''
    def __init__(self,tree):
        self.tree = tree
        print('Debug DictTreeLib Class',self.tree)
        #print('Kexs',self.tree.keys())

    def printOut(self):
        print('DictTreeLib PrintOut:',self.tree)
        return self.tree

    def getTree(self):
        return self.tree

    def setTree(self,tree):
        '''
        set an new tree
        '''
        self.tree = tree

    def selectTree(self,path):
        '''
        Select the subtree you would like to access
        path = path to the subtree
        '''
        return self.tree.get(path)

    def listNode(self):
        '''
        Lists all nodes available at the current tree level
        '''
        return self.tree.keys()

    def listLeafs(self):
        return self.tree.values()

    def addNode(self,sub,value):
        '''
        Adds a new node at the current tree level
        '''
        self.tree[sub]=value

    def delNode(self,key):
        '''
        Deletes a node from the current tree level
        '''
        del self.tree[key]

    def findNode(self,key):
        '''
        Finds all Nodes with the given name and returns them
        '''
        result = []
        self._findNode(self.tree,key,result)
        return result

    def _findNode(self,obj,key,result):

        for k, v in obj.items():
            if key in k:
                result.append(obj[k])
            if isinstance(v,dict):
                item = self._findkey(v,key,result)
                if item is not None:
                    result.append(item)


class tree(DictTreeLib):
    """
    Dictionary Tree Manager
    """
    def __init__(self, config = None):
        """
        Constructor, parses and stores the configuration
        """
        self.config=config
        self.treeRoot = DictTreeLib(self.config)
        print('Class Tree print Root tree object',self.treeRoot)
        self.treePointer = self.treeRoot

    def debug(self):
        print('Output:',yaml.dump(self.treePointer.printOut(),default_flow_style=False))

    def openYaml(self, filename):
        '''
        opens a file Yaml and reads the content
        '''
        handle = open(filename, 'r')
        tempCfg = yaml.load(handle,yaml.BaseLoader)
        handle.close()
        self.treeRoot = DictTreeLib(tempCfg)
        self.treePointer = self.treeRoot
        #print ('Test',self.config)

    def loadJson(self,jsonstr):

        jdata = json.loads(jsonstr)
        self.treeRoot = DictTreeLib(jdata)
        self.treePointer = self.treeRoot
        return True

    def loadDict(self,dict):
        self.treeRoot = dict
        self.treePointer = self.treeRoot

    def list(self):
        return self.treePointer.listNode()

    def listLeafs(self):
        return self.treePointer.listLeafs()

    def test(self,path):
        help = self.select(path)
        return self.__class__(help)

    def select(self,path):
        '''
        selects a subtree of the tree
        and creates a new DictTreeLib object on which
        all modification can be done
        '''
        tempobj=self.treePointer

        for x in path.split('.'):
            temp = tempobj.selectTree(x)
            tempobj = DictTreeLib(temp)


        self.treePointer = tempobj
        print('Treepointer',self.treePointer)
        return self.treePointer

    def delNode(self,key):
        self.treePointer.delNode(key)

    def add(self,key,value):
        print('ADD',key,value)
        self.treePointer.addNode(key,value)

    def reset(self):
        self.treePointer = DictTreeLib(self.config)

    def merge(self,dict):
       # print('printtree',self.treeRoot.getTree())
        return self._merge(self.treeRoot.getTree(),dict)

    def _merge(self, dict1, dict2):
        print('Merge',dict1,dict2)
        """ Recursively merges dict2 into dict1 """
        if not isinstance(dict1, dict) or not isinstance(dict2, dict):
            return dict2
        for k in dict2:
            print('k',k)
            if k in dict1:
                dict1[k] = self._merge(dict1[k], dict2[k])
            else:
                dict1[k] = dict2[k]
        return dict1

    def delete(self,dict):

        return self._delete_new(self.treeRoot.getTree(),dict)

        #return self._delete(self.config,dict)

    def _delete_old(self, dict1,dict2):
        print('Debug1',dict1,dict2)
        if not isinstance(dict2, dict):
            for z in dict2.split(','):
                print('Debug2',z,dict2,dict1)
                del dict1[z]
            return dict1

        for k in dict2:
            if k in dict1:
                if not dict2[k]:
                    del dict1[k]
                else:
                    self._delete(dict1[k], dict2[k])
            else:
                dict1[k] = dict2[k]
        return dict1

    def _delete(self,dict1,dict2):
        print('Debug',dict1,dict2)
        for k in dict2:
            if k in dict1:
                if not dict2[k]:
                    del dict1[k]
                else:
                    self._delete(dict1[k],dict2[k])
        return dict1

    def _delete_new(self,dict1,dict2):
        print('¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦')
        print('Debug new:',dict1, dict2)
        for key,value in dict2.items():
            if isinstance(value,dict):
                temp1 = dict1.get(key)
                temp2 = dict2.get(key)
                self._delete_new(temp1,temp2)
            else:
                print('Delete',key)
                del dict1[key]

        return


    def leafPath(self,tree):
        '''
        returns the path to each leaf of the tree, returns tree
        '''

        for key,value in tree.items():
            if not isinstance(value,dict):
                yield tuple([key, value])
            else:
                for subpath in self.leafPath(value):
                    yield (key,)+ subpath

       # return list(self)



    def compare(self,dictB):

        for k2,v2 in dictB.items():
            print ('B',k2,v2)
            print ('A',self.list())
            if k2 in self.list():
                print('key found',k2)
                if isinstance(v2,dict):
                    print('is Node',k2)
                    temp = self.select(k2)
                    print('pointer',temp)
                    self.compare(dictB[k2])
                    self.treePointer = temp
                    print('return von itteration',self.treePointer)
                else:
                    print('is Leaf',k2,'Value',v2)
                    #temp = self.select(k2)
                    self.add(k2, v2)
                    return
            else:
                print('Add Key to dictA Key:',k2,'value',v2)
                self.add(k2,v2)



if __name__ == '__main__':

    add_dict = {'MESSAGE':{'TYPE':'CONFIG','MODE':'ADD'},'DEVICES':{'MCP23017_2':{'Port5':{'HWID':5,'MODE':'BINARY-IN','INTERVAL':30}}}}
    del_dict1 = {'MESSAGE':{'TYPE':'CONFIG','MODE':'DEL'},'DEVICES':{'MCP23017_2':{'Port5':''}}}
    del_dict2 = {'MESSAGE':{'TYPE':'CONFIG','MODE':'DEL'},'DEVICES':{'MCP23017_2':{'Port5':'','Port2':''}}}
    del_dict3 = {'MESSAGE':{'TYPE':'CONFIG','MODE':'DEL'},'DEVICES':{'MCP23017_2':''}}

    cfg = Tree()
    cfg.openYaml('../config/config.yaml')


#    cfg.reset()
  #  cfg.select('DEVICES.DEVICE03.PORT300')
    print('Cfg:',cfg.list())

    cfg.merge(add_dict)
    print('Debug')
    cfg.debug()
    print('Delete Subtree')
    cfg.delete(del_dict3)
    print('Debug')
    cfg.debug()

   # cfg.delet('NAME')
   # cfg.add('test','value')
  #  print('Compare Test')
  #  print('List1',cfg.list())
  #  cfg.reset()
  #  print('List2',cfg.list())
   # cfg.compare(A)
  #  cfg.compareX(A)
   # print('List',list(cfg.leafPath('BINARY-OUT')))
  #  print('Print',cfg.leafPath(A))
  #  for item in cfg.leafPath(A):
        #print('Item',item,len(item))
   #     cfg.testNode2(list(item))
   # cfg.saveYaml('newtree')


