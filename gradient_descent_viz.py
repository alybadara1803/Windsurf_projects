import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc


def u_shaped_function(x):
    """U-shaped function: f(x) = x^2"""
    return x ** 2


def u_shaped_derivative(x):
    """Derivative of U-shaped function: f'(x) = 2x"""
    return 2 * x


def gradient_descent(start_x, learning_rate, n_iterations=50):
    """
    Perform gradient descent on U-shaped function.
    
    Args:
        start_x: Starting position
        learning_rate: Learning rate (step size)
        n_iterations: Number of iterations
        
    Returns:
        List of (x, y) points showing the path
    """
    path = []
    x = start_x
    
    for _ in range(n_iterations):
        y = u_shaped_function(x)
        path.append((x, y))
        
        gradient = u_shaped_derivative(x)
        x = x - learning_rate * gradient
        
        # Stop if converged (very small gradient)
        if abs(gradient) < 0.001:
            y = u_shaped_function(x)
            path.append((x, y))
            break
    
    return path


# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Gradient Descent Visualization", className="text-center mb-4"),
            html.P("Explore how learning rate affects convergence on a U-shaped curve", 
                   className="text-center text-muted mb-4"),
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Learning Rate:", className="fw-bold"),
                    dcc.Slider(
                        id='learning-rate',
                        min=0.001,
                        max=0.5,
                        step=0.001,
                        value=0.1,
                        marks={0.001: '0.001', 0.05: '0.05', 0.1: '0.1', 
                               0.2: '0.2', 0.3: '0.3', 0.5: '0.5'},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Div(id='learning-rate-value', className="mt-2 mb-3"),
                    
                    html.Label("Starting Position:", className="fw-bold"),
                    dcc.Slider(
                        id='start-position',
                        min=-5,
                        max=5,
                        step=0.1,
                        value=4,
                        marks={-5: '-5', -2.5: '-2.5', 0: '0', 2.5: '2.5', 5: '5'},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Div(id='start-position-value', className="mt-2 mb-3"),
                    
                    html.Label("Number of Iterations:", className="fw-bold"),
                    dcc.Slider(
                        id='iterations',
                        min=10,
                        max=100,
                        step=5,
                        value=50,
                        marks={10: '10', 30: '30', 50: '50', 70: '70', 100: '100'},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Div(id='iterations-value', className="mt-2"),
                ])
            ], className="mb-4")
        ], width=4),
        
        dbc.Col([
            dcc.Graph(id='gradient-descent-plot', style={'height': '600px'})
        ], width=8)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='convergence-info', className="mt-3")
        ], width=12)
    ])
], fluid=True)


@app.callback(
    [Output('learning-rate-value', 'children'),
     Output('start-position-value', 'children'),
     Output('iterations-value', 'children'),
     Output('gradient-descent-plot', 'figure'),
     Output('convergence-info', 'children')],
    [Input('learning-rate', 'value'),
     Input('start-position', 'value'),
     Input('iterations', 'value')]
)
def update_visualization(learning_rate, start_x, n_iterations):
    # Update slider value displays
    lr_text = f"Learning Rate: {learning_rate:.3f}"
    start_text = f"Starting Position: {start_x:.1f}"
    iter_text = f"Iterations: {n_iterations}"
    
    # Generate U-shaped curve
    x_curve = np.linspace(-5, 5, 200)
    y_curve = u_shaped_function(x_curve)
    
    # Run gradient descent
    path = gradient_descent(start_x, learning_rate, n_iterations)
    path_x = [p[0] for p in path]
    path_y = [p[1] for p in path]
    
    # Determine convergence status
    final_x = path_x[-1]
    final_y = path_y[-1]
    converged = abs(final_x) < 0.1
    iterations_used = len(path)
    
    # Create the plot
    fig = go.Figure()
    
    # Add U-shaped curve
    fig.add_trace(go.Scatter(
        x=x_curve,
        y=y_curve,
        mode='lines',
        name='U-shaped curve (f(x) = x²)',
        line=dict(color='lightblue', width=3)
    ))
    
    # Add gradient descent path
    fig.add_trace(go.Scatter(
        x=path_x,
        y=path_y,
        mode='lines+markers',
        name='Gradient descent path',
        line=dict(color='red', width=2),
        marker=dict(size=8, color='red')
    ))
    
    # Add starting point
    fig.add_trace(go.Scatter(
        x=[path_x[0]],
        y=[path_y[0]],
        mode='markers',
        name='Start',
        marker=dict(size=15, color='green', symbol='circle')
    ))
    
    # Add ending point
    fig.add_trace(go.Scatter(
        x=[path_x[-1]],
        y=[path_y[-1]],
        mode='markers',
        name='End',
        marker=dict(size=15, color='blue', symbol='x')
    ))
    
    fig.update_layout(
        title='Gradient Descent on U-shaped Curve',
        xaxis_title='x',
        yaxis_title='f(x) = x²',
        hovermode='x unified',
        legend=dict(x=0.02, y=0.98),
        template='plotly_white'
    )
    
    # Convergence info
    if converged:
        info_color = "success"
        info_text = f"✓ Converged to minimum at x = {final_x:.4f} in {iterations_used} iterations"
    else:
        if learning_rate > 0.25:
            info_color = "danger"
            info_text = f"✗ Learning rate too high! Diverging or oscillating. Final x = {final_x:.4f}"
        else:
            info_color = "warning"
            info_text = f"⚠ Not fully converged. Final x = {final_x:.4f} after {iterations_used} iterations"
    
    convergence_alert = dbc.Alert(info_text, color=info_color)
    
    return lr_text, start_text, iter_text, fig, convergence_alert


if __name__ == '__main__':
    app.run(debug=True)
