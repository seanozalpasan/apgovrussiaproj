import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

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

def make_factor_dashboard(data):
    factor_labels = [
        'Factor 1: Constraints on Government Powers',
        'Factor 2: Absence of Corruption',
        'Factor 3: Open Government',
        'Factor 4: Fundamental Rights',
        'Factor 5: Order and Security',
        'Factor 6: Regulatory Enforcement',
        'Factor 7: Civil Justice',
        'Factor 8: Criminal Justice'
    ]

    plot_colors = [
        '#1f77b4',  # blue
        '#ff7f0e',  # orange
        '#2ca02c',  # green
        '#d62728',  # red
        '#9467bd',  # purple
        '#8c564b',  # brown
        '#e377c2',  # pink
        '#7f7f7f'   # gray
    ]

    dashboard = make_subplots(
        rows=4, 
        cols=2, 
        subplot_titles=factor_labels,
        vertical_spacing=0.15,
        horizontal_spacing=0.15
    )

    for i, factor_key in enumerate(['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8']):
        row_num = (i // 2) + 1
        col_num = (i % 2) + 1
        
        dashboard.add_trace(
            go.Scatter(
                x=data['year'],
                y=data[factor_key],
                name=factor_labels[i],
                line=dict(color=plot_colors[i], width=2),
                mode='lines+markers+text',
                text=[f'{score:.3f}' for score in data[factor_key]],
                textposition='top center',
                textfont=dict(size=10),
            ),
            row=row_num,
            col=col_num
        )
        
        dashboard.update_yaxes(range=[-0.05, 1.05], row=row_num, col=col_num)

    # Make it look nice
    dashboard.update_layout(
        height=1500,
        width=1200,
        title_text="Russian Federation WJP Factors Trends (2015-2024)",
        showlegend=False,
        template="plotly_white",
        margin=dict(t=100, b=50, l=50, r=50)
    )

    for row in range(1, 5):
        for col in range(1, 3):
            dashboard.update_xaxes(title_text="Year", row=row, col=col)
            dashboard.update_yaxes(title_text="Score", row=row, col=col)

    return dashboard

def main():
    wjp_data = get_wjp_data('RussianFederation.csv')
    dashboard = make_factor_dashboard(wjp_data)
    dashboard.show()

if __name__ == "__main__":
    main()