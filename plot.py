import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

df = pd.read_csv('mvo_sift.csv')

fig = px.line(df, x = 'FRAME', y = 'ERROR', title='MVO')
fig.show()