class DataList(object):

    def __init__(self, myData=None):
        if myData is None:
            myData = []
        self.myData = myData

    def getDataList(self):
        return self.myData

    def setDataList(self, newData):
        self.myData = newData

    def addData(self, data):
        self.myData.append(data)

    def getData(self, index=None, name=None):
        if index is not None:
            return self.myData[index]
        elif name is not None:
            i = 0
            for x in self.myData:
                if (getattr(x,'idName')) == name:
                    return x
                i += 1
        else:
            return None

    def removeData(self, index=None, name=None):
        if index is not None:
            self.myData.pop(index)
            return True
        elif name is not None:
            i = 0
            for x in self.myData:
                if x['name'] == name:
                    self.myData.pop(i)
                    return True
                i += 1
        else:
            return None
