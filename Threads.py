import threading
from DataList import DataList

threads = []


class MyThreads:
    
    @staticmethod
    def addThread(name):
        threads.append(name)

    @staticmethod
    def checkThread(name):
        for x in threads:
            if x == name:
                return true
                
            
