from PyQt5 import QtWidgets, QtWebEngineWidgets
import plotly.graph_objects as go
from utils.load_save_data import transactions_observable
from PyQt5.QtCore import QDate
from observables.visible_tags import visibleTags

class MonthlyStackedBarChart(QtWidgets.QWidget):
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
        transactions = transactions_observable.get_data()

        startDate = self.start.get_data()
        endDate = self.end.get_data()

        # Aggregate amounts by month and tag
        monthly_tag_amounts = {}
        
        # Get the list of visible tags
        visible_tags = visibleTags.get_data()

        # Filter transactions by the selected date range
        for transaction in transactions:
            # Convert the transaction date from string "MM/DD/YYYY" to QDate
            transaction_date = QDate.fromString(transaction.date, 'MM/dd/yyyy')

            # Only include transactions within the date range
            if startDate <= transaction_date <= endDate:
                # Get the year and month (e.g., '2025-02' for February 2025)
                month_year = transaction_date.toString('yyyy-MM')
                
                # Initialize the dictionary for the month if not already present
                if month_year not in monthly_tag_amounts:
                    monthly_tag_amounts[month_year] = {tag: 0 for tag in visible_tags}
                    monthly_tag_amounts[month_year]['No Tag'] = 0

                # Check if the transaction has any visible tags
                transaction_tags = [tag['tag_name'] for tag in transaction.tags]

                if transaction_tags:
                    # If the transaction has tags, include only if at least one is visible
                    for tag in transaction_tags:
                        if tag in visible_tags:
                            monthly_tag_amounts[month_year][tag] += transaction.amount
                else:
                    # If the transaction has no tags, accumulate it in the "No Tag" category
                    monthly_tag_amounts[month_year]['No Tag'] += transaction.amount


        for outer_key, inner_dict in monthly_tag_amounts.items():
            for inner_key, value in inner_dict.items():
                try:
                    monthly_tag_amounts[outer_key][inner_key] = abs(float(value))
                except (ValueError, TypeError):
                    monthly_tag_amounts[outer_key][inner_key] = 0.0

        # Prepare data for the stacked bar chart
        months = sorted(monthly_tag_amounts.keys())
        data = {tag: [] for tag in visible_tags}
        data['No Tag'] = []

        for month in months:
            for tag in visible_tags:
                data[tag].append(round(monthly_tag_amounts[month][tag], 2))
            data['No Tag'].append(round(monthly_tag_amounts[month]['No Tag'], 2))

        # Create the stacked bar chart using Plotly
        fig = go.Figure()

        # Add bars for each tag
        for tag in visible_tags:
            fig.add_trace(go.Bar(
                x=months,
                y=data[tag],
                name=tag,
                text=[f"${amount}" for amount in data[tag]],
                textposition='inside',
                hoverinfo='x+y+text',
                hovertemplate='<b>'+tag+'</b><br>Month: %{x}<br>Amount: $%{y:.2f}<extra></extra>'
            ))

        # Add bars for "No Tag"
        fig.add_trace(go.Bar(
            x=months,
            y=data['No Tag'],
            name='No Tag',
            text=[f"${amount}" for amount in data['No Tag']],
            textposition='inside',
            hoverinfo='x+y+text',
            hovertemplate='<b>No Tag</b><br>Month: %{x}<br>Amount: $%{y}<extra></extra>'
        ))

        # Update layout settings
        fig.update_layout(
            title="Spending by Month and Tag",
            xaxis_title="Month",
            yaxis_title="Amount Spent",
            barmode='stack',
            paper_bgcolor='#19232D',
            plot_bgcolor='#19232D',
            font=dict(color='white'),
            margin=dict(l=100, r=50, t=50, b=50)
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