from PyQt5 import QtWidgets, QtWebEngineWidgets
import plotly.graph_objects as go
from load_save_data import transactions_observable
from PyQt5.QtCore import QDate
from visible_tags import visibleTags

class RadarChart(QtWidgets.QWidget):
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

        # Prepare data for the radar chart
        tags = list(tag_amounts.keys())
        amounts = list(tag_amounts.values())

        # Create the radar chart using Plotly
        fig = go.Figure(go.Scatterpolar(
            r=amounts,
            theta=tags,
            fill='toself',  # Fill the area of the chart
            marker=dict(color=[tag_colors.get(tag, 'rgba(0, 0, 255, 0.6)') for tag in tags])  # Custom colors
        ))

        # Update the layout
        fig.update_layout(
            title="Transaction Amounts by Tag (Radar Chart)",
            template="plotly_dark",
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(amounts) * 1.1]  # Set the max range for better scaling
                ),
            ),
            showlegend=False
        )

        fig.update_layout(paper_bgcolor='#19232D', plot_bgcolor='#19232D')
        
        js_code = '''<script>
                        document.body.style.backgroundColor = "#19232D";  // Set background color to black
                        document.body.style.margin = 0;
                        document.body.style.padding = 0;
                    </script>'''

        chart_html = fig.to_html(include_plotlyjs='cdn', full_html=False)
        full_html = chart_html + js_code

        # Embed the chart in the QWebEngineView
        self.browser.setHtml(full_html)
