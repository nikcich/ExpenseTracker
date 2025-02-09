from PyQt5 import QtWidgets, QtWebEngineWidgets
import plotly.graph_objects as go
from utils.load_save_data import transactions_observable
from PyQt5.QtCore import QDate
from observables.visible_tags import visibleTags

class TagBarChart(QtWidgets.QWidget):
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

        # Aggregate amounts by tag
        tag_amounts = {}
        tag_colors = {}  # Dictionary to store the color of each tag

        # Get the list of visible tags
        visible_tags = visibleTags.get_data()

        # Add a "No Tag" entry for transactions without any tags
        no_tag_amount = 0

        # Filter transactions by the selected date range and visible tags
        for transaction in transactions:
            # Convert the transaction date from string "MM/DD/YYYY" to QDate
            transaction_date = QDate.fromString(transaction.date, 'MM/dd/yyyy')
            # Only include transactions within the date range
            if startDate <= transaction_date <= endDate:
                if not transaction.tags:
                    # If the transaction has no tags, accumulate it to the "No Tag" category
                    no_tag_amount += transaction.amount
                else:
                    for tag in transaction.tags:
                        tag_name = tag['tag_name']
                        tag_color = tag['color']  # Get the color for the tag

                        # Only include the tag if it's in the list of visible tags
                        if tag_name in visible_tags:
                            # Store the color and accumulate amounts
                            if tag_name not in tag_amounts:
                                tag_amounts[tag_name] = 0
                                tag_colors[tag_name] = tag_color  # Assign the color to the tag
                        
                            tag_amounts[tag_name] += transaction.amount

        # Add "No Tag" section if there are any transactions without tags
        if no_tag_amount > 0:
            tag_amounts["No Tag"] = no_tag_amount
            tag_colors["No Tag"] = "#777"  # A neutral gray color for "No Tag"

        # Check if there are any valid amounts
        if len(tag_amounts) == 0:
            # If there are no valid transactions, display an empty message or a default message
            self.browser.setHtml("<h1>No data available for the selected date range.</h1>")
            return

        # Prepare data for the horizontal bar chart
        tags = list(tag_amounts.keys())
        amounts = list(tag_amounts.values())

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
            title="Transaction Amounts by Tag",
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
