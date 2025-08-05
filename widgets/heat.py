from PyQt5 import QtWidgets, QtWebEngineWidgets
import plotly.graph_objects as go
from utils.load_save_data import transactions_observable
from PyQt5.QtCore import QDate
from observables.visible_tags import visibleTags
import pandas as pd

class DailyHeatmapChart(QtWidgets.QWidget):
    def __init__(self, start, end):
        super().__init__()

        # Create the QWebEngineView widget to display the chart
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        
        # Layout setup
        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.browser, stretch=1)

        self.start = start
        self.end = end
        start.add_observer(self.onDateRangeChange)
        end.add_observer(self.onDateRangeChange)

        self.resize(1000, 800)
        self.show_graph()
        transactions_observable.add_observer(self.show_graph)
        visibleTags.add_observer(self.show_graph)
    
    def onDateRangeChange(self):
        self.show_graph()
        
    def show_graph(self):
        # Get the list of transactions
        transactions = transactions_observable.get_expenses()

        startDate = self.start.get_data()
        endDate = self.end.get_data()

        # Aggregate amounts by day
        daily_amounts = {}
        
        # Get the list of visible tags
        visible_tags = visibleTags.get_data()

        # Filter transactions by the selected date range
        for transaction in transactions:
            # Convert the transaction date from string "MM/DD/YYYY" to QDate
            transaction_date = QDate.fromString(transaction.date, 'MM/dd/yyyy')

            # Only include transactions within the date range
            if startDate <= transaction_date <= endDate:
                # Check if the transaction has any visible tags
                transaction_tags = [tag['tag_name'] for tag in transaction.tags]

                if transaction_tags:
                    # If the transaction has tags, include only if at least one is visible
                    if any(tag in visible_tags for tag in transaction_tags):
                        # Get the date (e.g., '2025-02-08' for February 8, 2025)
                        date_str = transaction_date.toString('yyyy-MM-dd')
                        
                        # Accumulate the amount for each day, rounded to the nearest cent
                        if date_str not in daily_amounts:
                            daily_amounts[date_str] = 0
                        
                        daily_amounts[date_str] += round(transaction.amount, 2)

        # Prepare data for the heatmap chart
        dates = pd.date_range(startDate.toString('yyyy-MM-dd'), endDate.toString('yyyy-MM-dd'))
        amounts = [round(daily_amounts.get(date.strftime('%Y-%m-%d'), 0), 2) for date in dates]

        # Create a DataFrame for the heatmap
        df = pd.DataFrame({'date': dates, 'amount': amounts})
        df['day'] = df['date'].dt.dayofweek
        df['week'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time)

        num_weeks = len(df['week'].unique())
        label_interval = max(1, num_weeks // 10)

        # Create the heatmap chart using Plotly
        fig = go.Figure(data=go.Heatmap(
            z=df['amount'],
            x=df['week'],
            y=df['day'],
            colorscale='Viridis',
            hovertext=df['date'].dt.strftime('%Y-%m-%d') + '<br>' + df['amount'].astype(str),
            hoverinfo='text',
            xgap=5,
            ygap=5
        ))

        # Update layout settings
        fig.update_layout(
            title="Spending by Day",
            xaxis_title="Week Of",
            yaxis_title="Day of Week",
            yaxis=dict(
                tickmode='array',
                tickvals=[0, 1, 2, 3, 4, 5, 6],
                ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                showgrid=False,
                zeroline=False,
                ticklen=10,
            ),
            xaxis=dict(
                tickmode='array',
                tickvals=df['week'].unique()[::label_interval],
                ticktext=[date.strftime('%b %d') for date in df['week'].unique()[::label_interval]],
                showgrid=False,
                zeroline=False,
            ),
            paper_bgcolor='#19232D',
            plot_bgcolor='#19232D',
            font=dict(color='white'),
            margin=dict(l=100, r=50, t=50, b=50),
            xaxis_showgrid=False,
            yaxis_showgrid=False,
        )
        
        js_code = '''<script>
                        document.body.style.backgroundColor = "#19232D";  // Set background color to black
                        document.body.style.margin = 0;
                        document.body.style.padding = 0;
                    </script>'''

        # Get the HTML of the chart
        chart_html = fig.to_html(include_plotlyjs='cdn', full_html=False)

        # Combine the HTML and the JS
        full_html = chart_html + js_code

        # Embed the chart with custom JS into the QWebEngineView
        self.browser.setHtml(full_html)