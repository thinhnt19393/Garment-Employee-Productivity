import dash
from dash import dcc
from dash import html
from dash.html.Label import Label
from pandas.io.formats import style
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from dash import callback_context
from datetime import date

app = dash.Dash(
    __name__
)

df = pd.read_csv("preprocess_data.csv")
days = df["date"].unique()
dict_days = {days[i]:i+1 for i in range(len(days))}
df['number'] = [dict_days[day] for day in df.date]

colors = {"background": "#011833", "text": "#7FDBFF"}

app.title = "Productivity of garment employee"

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2("Start date and end date", ),
                            ]
                        ),
                        html.Div(
                            [
                                dcc.DatePickerSingle(
                                    id='my-date-picker-start',
                                    min_date_allowed=date(2015, 1, 1),
                                    max_date_allowed=date(2015, 3, 11),
                                    initial_visible_month=date(2015, 1, 1),
                                    date=date(2015, 1, 1)
                                ),
                                dcc.DatePickerSingle(
                                    id='my-date-picker-end',
                                    min_date_allowed=date(2015, 1, 1),
                                    max_date_allowed=date(2015, 3, 11),
                                    initial_visible_month=date(2015, 3, 11),
                                    date=date(2015, 3, 11),
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dcc.RangeSlider(id="slider-date", min=1,
                                    max=59,
                                    step=1, value=[1, 59],
                                    allowCross=False,
                                    className="mt-3",
                                    marks=None,
                                ),
                            ],
                            className="slider",
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2("Quarter"),
                            ]
                        ),
                        html.Div(
                            [
                                dcc.Checklist(id="checkbox_quarter",
                                    options = ["Quarter1", "Quarter2", "Quarter3", "Quarter4", "Quarter5"],
                                    value = ["Quarter1", "Quarter2", "Quarter3", "Quarter4", "Quarter5"],
                                )
                            ],
                            className="checklist",
                        ),
                    ]
                ),
            ],
            className="column",
            #style={
            #'display': 'inline-block',
            #'width': '300px',
            #'vertical-align': 'top'
            #},'''
        ),
        html.Div(dcc.Graph(id="actual_productivtiy"), className="chart",
        #style={
        #    'display': 'inline-block',
        #    'width': '900px',
        #    'height': '30px',
        #    'vertical-align': 'top',
        #    'margin-left': '50px'
        #}
        ),
    ],
    className="container",
    style={'display': 'flex', 'flex-direction': 'row'}
)

#Update date
@app.callback(
    Output('my-date-picker-start','date'),
    Output('my-date-picker-end','date'),
    Output('slider-date','value'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('slider-date', 'value'),
)
def update_date(start_date, end_date, slider_v):
    ctx = callback_context
    component_triggered = ctx.triggered[0]["prop_id"].split(".")[0]

    if component_triggered == 'slider-date':
        start_date = df[df.number == slider_v[0]]['date'].values[0]
        end_date = df[df.number == slider_v[1]]['date'].values[0]

    elif component_triggered == 'my-date-picker-start' or component_triggered == 'my-date-picker-end':
        num_start = df[df.date==start_date]['number'].values[0]
        num_end = df[df.date==end_date]['number'].values[0]
        slider_v = [num_start, num_end]

    return start_date, end_date, slider_v

#Update figure
@app.callback(
    Output("actual_productivtiy", "figure"),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('checkbox_quarter','value'),
)
def update_figure(start_date, end_date, checkbox_quarter):
    dff = df[((df.date>=start_date) & (df.date<=end_date) & (df.quarter.isin(checkbox_quarter)))]
    fig = px.line(
        dff,
        x="date",
        y="actual_productivity",
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="black",
        xaxis_showgrid=False, 
        yaxis_showgrid=False,
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)