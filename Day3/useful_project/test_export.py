"""Quick test of HTML export behavior."""

from data_store import create_expense
from reports import export_expenses_html

# Create test expense
expense = create_expense(25.50, "food", "lunch")
expenses = [expense]

# Export HTML and see what opens
export_expenses_html(expenses)
