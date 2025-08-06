from PyQt5 import QtWidgets, QtWebEngineWidgets
import plotly.graph_objects as go
from utils.load_save_data import transactions_observable
from PyQt5.QtCore import QDate
from observables.visible_tags import visibleTags

class HighLevelSavingsBarChart(QtWidgets.QWidget):
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
        transactions = list(transactions_observable.get_data().values())


        startDate = self.start.get_data()
        endDate = self.end.get_data()

        tag_amounts = {
            "Income": 0,
            "Expenses": 0,
        }
        tag_colors = {
            "Income": "#00a545",  # Green for income
            "Expenses": "#e74c3c",  # Red for expenses
        }  # Dictionary to store the color of each tag

        # Filter transactions by the selected date range and visible tags
        for transaction in transactions:
            # Convert the transaction date from string "MM/DD/YYYY" to QDate
            transaction_date = QDate.fromString(transaction.date, 'MM/dd/yyyy')
            # Only include transactions within the date range
            if startDate <= transaction_date <= endDate:
                if not transaction.tags:
                    # If the transaction has no tags, accumulate it to the "No Tag" category
                    tag_amounts["Expenses"] += transaction.amount
                else:
                    for tag in transaction.tags:
                        tag_name = tag['tag_name']
                        # Only include the tag if it's in the list of visible tags
                        # Store the color and accumulate amounts
                        if tag_name == "Savings":
                            continue  # Ignore savings tag for this high-level breakdown"

                        if tag_name == "Income":
                            tag_amounts["Income"] += transaction.amount
                        else:
                            tag_amounts["Expenses"] += transaction.amount

        # Check if there are any valid amounts
        if len(tag_amounts) == 0:
            # If there are no valid transactions, display an empty message or a default message
            self.browser.setHtml("<h1>No data available for the selected date range.</h1>")
            return

        # Prepare data for the horizontal bar chart
        tags = list(tag_amounts.keys())
        amounts_orig = list(tag_amounts.values())
        amounts = [abs(x) for x in amounts_orig]

        # Calculate the total amount for percentage calculation
        total_amount = sum(amounts)
        percentages = [round((amount / total_amount) * 100) for amount in amounts]  # Rounded percentages
        rounded_amounts = [f"${round(amount, 2)}" for amount in amounts]

        # Create the horizontal bar chart using Plotly
        fig = go.Figure()

        # Add horizontal bars
        fig.add_trace(go.Bar(
            y=tags,
            x=percentages,
            orientation='h',  # Horizontal bars
            marker=dict(color=[tag_colors[tag] for tag in tags]),  # Custom colors for each tag
            text=rounded_amounts,  # Show the actual amount sum on the bars
            textposition='inside',
            hoverinfo='x+text',  # Show the percentage and amount on hover
        ))

        # Update layout settings
        fig.update_layout(
            title="Expenses VS Income Bar Chart",
            xaxis_title="Percentage",
            yaxis_title="Tag",
            paper_bgcolor='#19232D',
            plot_bgcolor='#19232D',
            font=dict(color='white'),
            xaxis=dict(tickformat='.1f%'),
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
