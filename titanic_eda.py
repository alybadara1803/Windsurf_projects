import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Load Titanic dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Data preprocessing
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
df['Fare'] = df['Fare'].fillna(df['Fare'].median())
df['Survived'] = df['Survived'].map({0: 'No', 1: 'Yes'})
df['Pclass'] = df['Pclass'].map({1: '1st', 2: '2nd', 3: '3rd'})

# Create age groups
df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 30, 50, 100], 
                        labels=['Child', 'Teenager', 'Young Adult', 'Adult', 'Senior'])

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Titanic Dataset - Exploratory Data Analysis", 
                   className="text-center mb-4", style={'color': '#2c3e50'}),
            html.Hr()
        ])
    ]),
    
    # Summary Statistics
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Dataset Overview", className="card-title"),
                    html.P(f"Total Passengers: {len(df)}", className="card-text"),
                    html.P(f"Survived: {len(df[df['Survived']=='Yes'])} ({len(df[df['Survived']=='Yes'])/len(df)*100:.1f}%)", 
                           className="card-text", style={'color': 'green'}),
                    html.P(f"Did Not Survive: {len(df[df['Survived']=='No'])} ({len(df[df['Survived']=='No'])/len(df)*100:.1f}%)", 
                           className="card-text", style={'color': 'red'}),
                ])
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Passenger Class Distribution", className="card-title"),
                    dcc.Graph(id='class-dist', figure={})
                ])
            ])
        ], width=8)
    ], className="mb-4"),
    
    # Main Visualizations
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Survival Rate by Passenger Class", className="card-title"),
                    dcc.Graph(id='survival-by-class', figure={})
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Survival Rate by Gender", className="card-title"),
                    dcc.Graph(id='survival-by-gender', figure={})
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Age Distribution", className="card-title"),
                    dcc.Graph(id='age-dist', figure={})
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Survival Rate by Age Group", className="card-title"),
                    dcc.Graph(id='survival-by-age', figure={})
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Fare Distribution by Survival", className="card-title"),
                    dcc.Graph(id='fare-dist', figure={})
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Survival Rate by Embarkation Port", className="card-title"),
                    dcc.Graph(id='survival-by-embarked', figure={})
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Interactive Filters
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Interactive Analysis", className="card-title"),
                    html.Label("Filter by Passenger Class:"),
                    dcc.Dropdown(
                        id='class-filter',
                        options=[{'label': 'All', 'value': 'All'}] + 
                                [{'label': cls, 'value': cls} for cls in df['Pclass'].unique()],
                        value='All',
                        className="mb-3"
                    ),
                    html.Label("Filter by Gender:"),
                    dcc.Dropdown(
                        id='gender-filter',
                        options=[{'label': 'All', 'value': 'All'}] + 
                                [{'label': gender, 'value': gender} for gender in df['Sex'].unique()],
                        value='All',
                        className="mb-3"
                    ),
                    html.Label("Filter by Age Group:"),
                    dcc.Dropdown(
                        id='age-filter',
                        options=[{'label': 'All', 'value': 'All'}] + 
                                [{'label': age, 'value': age} for age in df['AgeGroup'].unique()],
                        value='All'
                    ),
                ])
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Filtered Survival Rate", className="card-title"),
                    dcc.Graph(id='filtered-survival', figure={})
                ])
            ])
        ], width=8)
    ], className="mb-4"),
    
    # Correlation Heatmap
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Correlation Matrix (Numeric Features)", className="card-title"),
                    dcc.Graph(id='correlation-heatmap', figure={})
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Family Size Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Family Size Analysis", className="card-title"),
                    html.P("Family Size = SibSp (siblings/spouses) + Parch (parents/children) + 1", 
                           className="text-muted small mb-3"),
                    dcc.Graph(id='family-size', figure={})
                ])
            ])
        ])
    ])
], fluid=True)

# Callbacks
@callback(
    Output('class-dist', 'figure'),
    Output('survival-by-class', 'figure'),
    Output('survival-by-gender', 'figure'),
    Output('age-dist', 'figure'),
    Output('survival-by-age', 'figure'),
    Output('fare-dist', 'figure'),
    Output('survival-by-embarked', 'figure'),
    Output('correlation-heatmap', 'figure'),
    Output('family-size', 'figure'),
    Input('class-filter', 'value'),
    Input('gender-filter', 'value'),
    Input('age-filter', 'value')
)
def update_plots(class_filter, gender_filter, age_filter):
    # Apply filters
    filtered_df = df.copy()
    if class_filter != 'All':
        filtered_df = filtered_df[filtered_df['Pclass'] == class_filter]
    if gender_filter != 'All':
        filtered_df = filtered_df[filtered_df['Sex'] == gender_filter]
    if age_filter != 'All':
        filtered_df = filtered_df[filtered_df['AgeGroup'] == age_filter]
    
    # Class distribution
    class_dist = px.pie(filtered_df, names='Pclass', title='Passenger Class Distribution',
                        color_discrete_sequence=px.colors.sequential.Pastel)
    
    # Survival by class
    survival_class = px.bar(filtered_df.groupby('Pclass')['Survived'].value_counts(normalize=True).unstack() * 100,
                           title='Survival Rate by Passenger Class',
                           labels={'value': 'Percentage', 'Pclass': 'Passenger Class'},
                           barmode='group')
    survival_class.update_layout(yaxis_title='Survival Rate (%)')
    
    # Survival by gender
    survival_gender = px.bar(filtered_df.groupby('Sex')['Survived'].value_counts(normalize=True).unstack() * 100,
                            title='Survival Rate by Gender',
                            labels={'value': 'Percentage', 'Sex': 'Gender'},
                            barmode='group')
    survival_gender.update_layout(yaxis_title='Survival Rate (%)')
    
    # Age distribution
    age_dist = px.histogram(filtered_df, x='Age', nbins=30, title='Age Distribution',
                           color='Survived', marginal='box')
    
    # Survival by age group
    survival_age = px.bar(filtered_df.groupby('AgeGroup')['Survived'].value_counts(normalize=True).unstack() * 100,
                         title='Survival Rate by Age Group',
                         labels={'value': 'Percentage', 'AgeGroup': 'Age Group'},
                         barmode='group')
    survival_age.update_layout(yaxis_title='Survival Rate (%)')
    
    # Fare distribution
    fare_dist = px.box(filtered_df, x='Survived', y='Fare', title='Fare Distribution by Survival Status')
    
    # Survival by embarked
    survival_embarked = px.bar(filtered_df.groupby('Embarked')['Survived'].value_counts(normalize=True).unstack() * 100,
                              title='Survival Rate by Embarkation Port',
                              labels={'value': 'Percentage', 'Embarked': 'Port'},
                              barmode='group')
    survival_embarked.update_layout(yaxis_title='Survival Rate (%)')
    
    # Correlation heatmap
    numeric_df = df[['Age', 'Fare', 'SibSp', 'Parch']].copy()
    numeric_df['Survived_Num'] = df['Survived'].map({'No': 0, 'Yes': 1})
    corr_matrix = numeric_df.corr()
    
    heatmap = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    heatmap.update_layout(title='Correlation Matrix')
    
    # Family size analysis
    filtered_df['FamilySize'] = filtered_df['SibSp'] + filtered_df['Parch'] + 1
    family_size = px.bar(filtered_df.groupby('FamilySize')['Survived'].value_counts(normalize=True).unstack() * 100,
                        title='Survival Rate by Family Size',
                        labels={'value': 'Percentage', 'FamilySize': 'Family Size'},
                        barmode='group')
    family_size.update_layout(yaxis_title='Survival Rate (%)')
    
    return (class_dist, survival_class, survival_gender, age_dist, survival_age, 
            fare_dist, survival_embarked, heatmap, family_size)

@callback(
    Output('filtered-survival', 'figure'),
    Input('class-filter', 'value'),
    Input('gender-filter', 'value'),
    Input('age-filter', 'value')
)
def update_filtered_survival(class_filter, gender_filter, age_filter):
    filtered_df = df.copy()
    if class_filter != 'All':
        filtered_df = filtered_df[filtered_df['Pclass'] == class_filter]
    if gender_filter != 'All':
        filtered_df = filtered_df[filtered_df['Sex'] == gender_filter]
    if age_filter != 'All':
        filtered_df = filtered_df[filtered_df['AgeGroup'] == age_filter]
    
    survival_counts = filtered_df['Survived'].value_counts()
    
    fig = go.Figure(data=[
        go.Bar(name='Survived', x=['Survived'], y=[survival_counts.get('Yes', 0)], 
               marker_color='green'),
        go.Bar(name='Did Not Survive', x=['Did Not Survive'], y=[survival_counts.get('No', 0)], 
               marker_color='red')
    ])
    
    fig.update_layout(
        title=f'Survival Count (Total: {len(filtered_df)} passengers)',
        yaxis_title='Number of Passengers',
        barmode='group'
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
