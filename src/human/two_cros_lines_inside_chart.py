## FROM HERE
## https://stackoverflow.com/questions/73428753/plotly-how-to-display-y-values-when-hovering-on-two-subplots-sharing-x-axis

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plotly_stl(results):

    fig = make_subplots(
        rows=3 + len(results.seasonal.columns),
        cols=1,
        shared_xaxes=False,
    )

    precision = 2
    customdataName = [
        results.observed.name.capitalize(),
        results.trend.name.capitalize(),
        results.seasonal.columns[0].capitalize(),
        results.seasonal.columns[1].capitalize(),
        results.resid.name.capitalize(),
    ]
    customdata = np.stack(
        (
            results.observed,
            results.trend,
            results.seasonal[results.seasonal.columns[0]],
            results.seasonal[results.seasonal.columns[1]],
            results.resid,
        ), 
        axis=-1
    )
    fig.append_trace(
        go.Scatter(
            name=customdataName[0], 
            mode='lines', 
            x=results.observed.index,
            y=results.observed,
            line=dict(
                shape='linear',
                # color='blue', # 'rgb(100, 10, 100)', 
                width=2,
                # dash='dash',
            ),
            customdata=customdata,                                 
            hovertemplate='<br>'.join([
                'Datetime: %{x:%Y-%m-%d:%h}',
                '<b>'+customdataName[0]+'</b><b>'+f": %{{y:.{precision}f}}"+'</b>',
                customdataName[1] + ": %{customdata[1]:.2f}",
                customdataName[2] + ": %{customdata[2]:.2f}",
                customdataName[3] + ": %{customdata[3]:.2f}",
                customdataName[4] + ": %{customdata[4]:.2f}",
                '<extra></extra>',
            ]),
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    
    fig['layout']['yaxis']['title'] = customdataName[0]
    fig.append_trace(
        go.Scatter(
            name=customdataName[1], 
            mode='lines', 
            x=results.trend.index,
            y=results.trend,
            line=dict(
                shape='linear',
                #color='blue', #'rgb(100, 10, 100)', 
                width=2,
                #dash='dash'
            ),
            customdata=customdata,                                 
            hovertemplate='<br>'.join([
                'Datetime: %{x:%Y-%m-%d:%h}',
                '<b>'+customdataName[1]+'</b><b>'+f": %{{y:.{precision}f}}"+'</b>',
                customdataName[0] + ": %{customdata[0]:.2f}",
                customdataName[2] + ": %{customdata[2]:.2f}",
                customdataName[3] + ": %{customdata[3]:.2f}",
                customdataName[4] + ": %{customdata[4]:.2f}",
                '<extra></extra>'
            ]),
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    fig['layout']['yaxis2']['title'] = customdataName[1]

    for i in range(len(results.seasonal.columns)):
        another = 3 - i
        fig.append_trace(
            go.Scatter(
                name=customdataName[2+i], 
                mode='lines', 
                x=results.seasonal.index,
                y=results.seasonal[results.seasonal.columns[i]],
                line=dict(
                    shape='linear',
                    # color='blue', #'rgb(100, 10, 100)', 
                    width=2,
                    # dash='dash'
                ),
                customdata=customdata,           
                hovertemplate='<br>'.join([
                    'Datetime: %{x:%Y-%m-%d:%h}',
                    '<b>'+customdataName[2+i]+'</b><b>'+f": %{{y:.{precision}f}}"+'</b>',
                    customdataName[0] + ": %{customdata[0]:.2f}",
                    customdataName[1] + ": %{customdata[1]:.2f}",
                    customdataName[another] + f": %{{customdata[{another}]:.{precision}f}}",
                    customdataName[4] + ": %{customdata[4]:.2f}",
                    '<extra></extra>',
                ]), 
                showlegend=False,
            ),
            row=3 + i,
            col=1,
        )
        fig['layout']['yaxis'+str(3+i)]['title'] = customdataName[2+i]
    
    fig.append_trace(
        go.Scatter(
            name=customdataName[4], 
            mode='lines', 
            x=results.resid.index,
            y=results.resid,
            line=dict(
                shape='linear',
                # color='blue', #'rgb(100, 10, 100)', 
                width=2,
                # dash='dash'
            ),   
            customdata=customdata,                                 
            hovertemplate='<br>'.join([
                'Datetime: %{x:%Y-%m-%d:%h}',
                '<b>'+customdataName[4]+'</b><b>'+f": %{{y:.{precision}f}}"+'</b>',
                customdataName[0] + ": %{customdata[0]:.2f}",
                customdataName[1] + ": %{customdata[1]:.2f}",
                customdataName[2] + ": %{customdata[2]:.2f}",
                customdataName[3] + ": %{customdata[3]:.2f}",
                '<extra></extra>',
            ]),                            
            showlegend=False,
        ),
        row=3 + len(results.seasonal.columns),
        col=1,
    )
    fig['layout']['yaxis'+str(3+len(results.seasonal.columns))]['title'] = customdataName[-1]
    fig['layout']['xaxis'+str(3+len(results.seasonal.columns))]['title'] = 'Datetime'

    fig.update_layout(
        height=800,
        width=1000,
        legend_tracegroupgap = 330,
        hovermode='x unified',
        legend_traceorder="normal",
        # plot_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_traces(xaxis='x{}'.format(str(3+len(results.seasonal.columns))))
    fig.show()
    plotly_stl(results_mstl)