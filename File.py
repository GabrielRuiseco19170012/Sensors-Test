import pickle
from DataList import DataList
from os import path


class File(object):

    @staticmethod
    def saveData(data):
        outfile = open('Data.bin', 'wb')
        pickle.dump(data, outfile)
        outfile.close()
        return True

    @staticmethod
    def readData():
        newDict = DataList()
        if path.exists('Data.bin'):
            infile = open('Data.bin', 'rb')
            newDict = pickle.load(infile)
            infile.close()
        return newDict
