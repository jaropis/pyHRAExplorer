from numpy import concatenate, delete
from scipy import mean, var, sqrt, where

class Runs:
    def __init__(self, signal):
        