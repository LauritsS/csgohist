from flask import Flask, render_template
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import requests, pymongo
import plotly.graph_objects as go

def index():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["csgo"]
    mycol = mydb["csgohistory"]

    unique_names = mycol.distinct('weapon')

    for weapon in unique_names:
        print(weapon)


if __name__ == '__main__':
    index()  