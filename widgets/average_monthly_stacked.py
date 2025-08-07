from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore
import plotly.graph_objects as go
from utils.load_save_data import transactions_observable
from PyQt5.QtCore import QDate
from observables.visible_tags import visibleTags

class AverageMonthlyStackedBarChart(QtWidgets.QWidget):
    def __init__(self, start, end):
        super().__init__()

        # Create the QWebEngineView widget to display the chart
        self.browser = QtWebEngineWidgets.QWebEngineView(self)


        self.data_sum_label = QtWidgets.QLabel("", self)
        self.data_sum_label.setAlignment(QtCore.Qt.AlignLeft)
        self.data_sum_label.setStyleSheet("font-size: 16px; color: white; font-weight: bold;")
        
        # Layout setup
        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.browser, stretch=1)
        vlayout.addWidget(self.data_sum_label)

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

        visible_tags = visibleTags.get_data()

        tag_amounts = {tag: 0 for tag in visible_tags}
        tag_amounts['No Tag'] = 0
        months = {}
        
        # Get the list of visible tags

        # Filter transactions by the selected date range
        for transaction in transactions:
            # Convert the transaction date from string "MM/DD/YYYY" to QDate
            transaction_date = QDate.fromString(transaction.date, 'MM/dd/yyyy')

            # Only include transactions within the date range
            if startDate <= transaction_date <= endDate:
                # Get the year and month (e.g., '2025-02' for February 2025)
                month_year = transaction_date.toString('yyyy-MM')
                months[month_year] = True

                # Check if the transaction has any visible tags
                transaction_tags = [tag['tag_name'] for tag in transaction.tags]

                if transaction_tags:
                    # If the transaction has tags, include only if at least one is visible
                    for tag in transaction_tags:
                        if tag in visible_tags:
                            tag_amounts[tag] += transaction.amount
                else:
                    # If the transaction has no tags, accumulate it in the "No Tag" category
                    tag_amounts['No Tag'] += transaction.amount


        for key, value in tag_amounts.items():
            try:
                tag_amounts[key] = abs(float(value))
            except (ValueError, TypeError):
                tag_amounts[key] = 0.0

        # Step 2: Prepare data for a single average value per tag
        data = {}
        num_months = max(len(months), 1)  # Avoid division by zero

        for tag in visible_tags:
            data[tag] = [round(tag_amounts.get(tag, 0.0) / num_months, 2)]

        # Include 'No Tag' separately
        data['No Tag'] = [round(tag_amounts.get('No Tag', 0.0) / num_months, 2)]

        total_sum = sum(tag_amounts.values())/ num_months
        self.data_sum_label.setText(f"Average monthly over period: ${total_sum:,.2f}")

        # Step 3: Create the stacked bar chart
        fig = go.Figure()

        for tag in visible_tags:
            fig.add_trace(go.Bar(
                x=["Average"],
                y=data[tag],
                name=tag,
                text=[f"${amount:.2f}" for amount in data[tag]],
                textposition='inside',
                hovertemplate=(
                    f"<b>{tag}</b><br>"
                    "Category: %{x}<br>"
                    "Average Amount: $%{y:.2f}<extra></extra>"
                )
            ))

        fig.add_trace(go.Bar(
            x=["Average"],
            y=data["No Tag"],
            name="No Tag",
            text=[f"${amount:.2f}" for amount in data["No Tag"]],
            textposition='inside',
            hovertemplate=(
                "<b>No Tag</b><br>"
                "Category: %{x}<br>"
                "Average Amount: $%{y:.2f}<extra></extra>"
            )
        ))

        # Step 4: Layout
        fig.update_layout(
            title="Average Monthly Expense per Tag",
            xaxis_title="",
            yaxis_title="Average Amount Spent",
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