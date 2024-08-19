from flask import Flask
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("data/Cleaned Jobs NG.csv")


from . import views
