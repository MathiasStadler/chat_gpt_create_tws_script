# FROM HERE
# https://stackoverflow.com/questions/73428753/plotly-how-to-display-y-values-when-hovering-on-two-subplots-sharing-x-axis

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf

df = yf.download("AAPL MSFT", start="2022-01-01", end="2022-07-01", group_by='ticker')
df.reset_index(inplace=True)

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

title = 'Price over time'
err = 'Price'

fig = make_subplots(rows=2, cols=1,
                    vertical_spacing = 0.05,
                    shared_xaxes=True,
                    subplot_titles=(title,""))

# AAPL
fig.add_trace(go.Scatter(x = df['Date'], 
                         y = df[('AAPL', 'Close')], 
                         line_color = 'green',
                         marker_color = 'green',
                         mode = 'lines+markers',
                         showlegend = True,
                         name = "AAPL",
                         stackgroup = 'one'),
              row = 1,
              col = 1,
              secondary_y = False)
# APPL $150 horizontal line
fig.add_trace(go.Scatter(x=df['Date'],
                         y=[125]*len(df['Date']),
                         mode='lines',
                         line_width=3,
                         line_color='black',
                         line_dash='dash',
                         showlegend=False,
                         name='APPL'
                        ),
              row=1,
              col=1,
              secondary_y=False)
                                   

# MSFT
fig.add_trace(go.Scatter(x= df['Date'], 
                         y = df[('MSFT', 'Close')], 
                         line_color = 'blue',
                         mode = 'lines+markers',
                         showlegend = True,
                         name = "MSFT",
                         stackgroup = 'one'),
              row = 2,
              col = 1,
              secondary_y = False)
# MSFT $150 horizontal line
fig.add_trace(go.Scatter(x=df['Date'],
                         y=[150]*len(df['Date']),
                         mode='lines',
                         line_width=3,
                         line_color='black',
                         line_dash='dash',
                         showlegend=False,
                         name='MSFT'
                        ),
              row=2,
              col=1,
              secondary_y=False)


fig.update_yaxes(tickprefix = '$')
fig.update_xaxes(type='date', range=[df['Date'].min(),df['Date'].max()])

#fig.add_hline(y=0, line_width=3, line_dash="dash", line_color="black")
fig.update_layout(#height=600, width=1400,
    hovermode = "x unified",
    legend_traceorder="normal")
fig.update_traces(xaxis='x2')

fig.show()

