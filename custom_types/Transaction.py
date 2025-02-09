from datetime import datetime

class Transaction:
    def __init__(self, tags=None, date=None, description="", amount=0.0, source=""):
        # Default to empty list if no tags provided
        self.tags = tags if tags is not None else []
        
        # If no date is provided, set it to the current date
        self.date = date if date else datetime.now().strftime("%m/%d/%Y")
        
        self.description = description
        self.amount = amount
        self.source = source

    def __repr__(self):
        return (f"Transaction(tags={self.tags}, date={self.date}, "
                f"description={self.description}, amount={self.amount}, source={self.source})")

    def add_tag(self, tag):
        """Adds a tag to the transaction"""
        self.tags.append(tag)

    def remove_tag(self, tag):
        """Removes a tag from the transaction"""
        if tag in self.tags:
            self.tags.remove(tag)

    def set_tags(self, tgs):
        self.tags = tgs

    def update_amount(self, new_amount):
        """Updates the amount for the transaction"""
        self.amount = new_amount

    def update_description(self, new_description):
        """Updates the description of the transaction"""
        self.description = new_description

    def update_source(self, new_source):
        """Updates the source of the transaction"""
        self.source = new_source

# Example of usage:
# transaction = Transaction(tags=["Groceries", "Instacart"], date="02/02/2025", description="IC* INSTACART SAN FRANCISCO CA", amount=212.32, source="Credit Card")
