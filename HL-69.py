import RPi.GPIO as GPIO



class HCR:
    def __init__(self, AO, DO):
        self.AO = AO
        self.DO = DO
