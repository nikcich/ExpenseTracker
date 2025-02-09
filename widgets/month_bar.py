from PyQt5 import QtWidgets, QtWebEngineWidgets
import plotly.graph_objects as go
from utils.load_save_data import transactions_observable
from PyQt5.QtCore import QDate
from observables.visible_tags import visibleTags

class MonthlyBarChart(QtWidgets.QWidget):
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

        # Aggregate amounts by month
        monthly_amounts = {}
        no_tag_amount = 0  # To accumulate amounts for transactions with no tags
        
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
                        # Get the year and month (e.g., '2025-02' for February 2025)
                        month_year = transaction_date.toString('yyyy-MM')
                        
                        # Accumulate the amount for each month, rounded to the nearest cent
                        if month_year not in monthly_amounts:
                            monthly_amounts[month_year] = 0
                        
                        monthly_amounts[month_year] += round(transaction.amount, 2)
                else:
                    # If the transaction has no tags, accumulate it in the "No Tag" category
                    month_year = transaction_date.toString('yyyy-MM')
                    no_tag_amount += round(transaction.amount, 2)

        # If there are any transactions with no tags, add them to the monthly amounts
        if no_tag_amount > 0:
            if 'No Tag' not in monthly_amounts:
                monthly_amounts['No Tag'] = 0
            # Add the "No Tag" amount to the months it applies to
            monthly_amounts['No Tag'] += no_tag_amount

        # Prepare data for the bar chart
        months = list(monthly_amounts.keys())
        amounts = list(monthly_amounts.values())
        rounded_amounts = [f"${round(amount, 2)}" for amount in amounts]

        # Create the bar chart using Plotly
        fig = go.Figure()

        # Add bars for each month
        fig.add_trace(go.Bar(
            x=months,
            y=amounts,
            marker=dict(color='rgba(58, 71, 80, 1)'),  # Dark color for bars
            text=rounded_amounts,  # Display amounts on the bars
            textposition='inside',
            hoverinfo='x+y+text',  # Show x (month) and y (amount) on hover
        ))

        # Update layout settings
        fig.update_layout(
            title="Spending by Month",
            xaxis_title="Month",
            yaxis_title="Amount Spent",
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
