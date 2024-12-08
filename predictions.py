import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def get_wjp_data(csv_file):
    raw_data = pd.read_csv(csv_file)
    
    years = raw_data.columns[1:].tolist()
    
    processed_data = {
        'year': years
    }
    
    wjp_factors = {
        'f1': 'Factor 1: Constraints on Government Powers',
        'f2': 'Factor 2: Absence of Corruption',
        'f3': 'Factor 3: Open Government',
        'f4': 'Factor 4: Fundamental Rights',
        'f5': 'Factor 5: Order and Security',
        'f6': 'Factor 6: Regulatory Enforcement',
        'f7': 'Factor 7: Civil Justice',
        'f8': 'Factor 8: Criminal Justice'
    }
    
    for factor_key, factor_name in wjp_factors.items():
        factor_scores = raw_data[raw_data['key'] == factor_name].iloc[0, 1:]
        processed_data[factor_key] = pd.to_numeric(factor_scores).tolist()
    
    return processed_data

def predict_future_trends(data, years_ahead=2):
    year_nums = np.array([int(year.split('-')[0]) for year in data['year']])
    future_years = np.arange(year_nums[0], year_nums[-1] + years_ahead + 1)
    
    predictions = {}
    confidence_scores = {}
    
    for factor in [f'f{i}' for i in range(1, 9)]:
        X = year_nums.reshape(-1, 1)
        y = np.array(data[factor])
        
        model = LinearRegression()
        model.fit(X, y)
        
        X_future = future_years.reshape(-1, 1)
        y_pred = model.predict(X_future)
        
        predictions[factor] = y_pred
        confidence_scores[factor] = r2_score(y, model.predict(X))
    
    return {
        'years': future_years,
        'predictions': predictions,
        'confidence': confidence_scores
    }

def plot_predictions(data, prediction_results):
    fig = make_subplots(rows=4, cols=2, 
                       subplot_titles=[f'Factor {i}: Predictions' for i in range(1, 9)])
    
    factor_names = [
        'Constraints on Government Powers',
        'Absence of Corruption',
        'Open Government',
        'Fundamental Rights',
        'Order and Security',
        'Regulatory Enforcement',
        'Civil Justice',
        'Criminal Justice'
    ]
    
    for i, factor in enumerate([f'f{i}' for i in range(1, 9)]):
        row = (i // 2) + 1
        col = (i % 2) + 1
        
        year_nums = [int(year.split('-')[0]) for year in data['year']]
        
        fig.add_trace(
            go.Scatter(
                x=year_nums,
                y=data[factor],
                name='Actual',
                line=dict(color='blue'),
                showlegend=False
            ),
            row=row, col=col
        )
        
        fig.add_trace(
            go.Scatter(
                x=prediction_results['years'],
                y=prediction_results['predictions'][factor],
                name='Predicted',
                line=dict(color='red', dash='dash'),
                showlegend=False
            ),
            row=row, col=col
        )
        
        conf_score = prediction_results['confidence'][factor]
        fig.add_annotation(
            text=f'Confidence: {conf_score:.2f}',
            xref='x domain',
            yref='y domain',
            x=0.05,
            y=0.95,
            showarrow=False,
            row=row,
            col=col
        )
        
        fig.update_xaxes(
            dtick=1,
            tickangle=45,
            row=row,
            col=col
        )
    
    fig.update_layout(
        height=1500, 
        width=1200, 
        title_text='WJP Factors Predictions',
        showlegend=False
    )
    return fig

def main():
    wjp_data = get_wjp_data('RussianFederation.csv')
    predictions = predict_future_trends(wjp_data, years_ahead=5)
    prediction_plot = plot_predictions(wjp_data, predictions)
    prediction_plot.show()

if __name__ == "__main__":
    main()