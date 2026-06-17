"""Reporting functions for the budget tracker."""

import csv
import html
import os
import shutil
import subprocess
import sys
import webbrowser
from collections import defaultdict
from pathlib import Path
from statistics import mean

EXPORT_DIR = Path(__file__).resolve().parent


def _open_file(filename, browser=False):
    """Open a file in the system default application."""
    try:
        if browser:
            webbrowser.open(Path(filename).resolve().as_uri())
            return
        if sys.platform.startswith("win"):
            os.startfile(filename)
        elif sys.platform == "darwin":
            subprocess.run(["open", filename], check=False)
        else:
            subprocess.run(["xdg-open", filename], check=False)
    except Exception as exc:
        print(f"Unable to open file automatically: {exc}")


def _open_csv_in_excel(filename):
    """Try to open a CSV file specifically in Excel on Windows."""
    if not sys.platform.startswith("win"):
        _open_file(filename)
        return

    if shutil.which("excel"):
        try:
            subprocess.run(["excel", str(filename)], check=False)
            return
        except Exception as exc:
            print(f"Excel launch failed: {exc}")

    if shutil.which("cmd"):
        try:
            subprocess.run(["cmd", "/c", "start", "", "excel", str(filename)], check=False)
            return
        except Exception as exc:
            print(f"Excel launch failed: {exc}")

    print("Excel was not found on PATH; opening CSV with the default application instead.")
    _open_file(filename)


def _open_html_in_browser(filename):
    """Open an HTML file in a web browser."""
    filepath = Path(filename).resolve()
    uri = filepath.as_uri()

    if sys.platform.startswith("win"):
        explicit_browsers = [
            "msedge.exe", "chrome.exe", "firefox.exe",
            "iexplore.exe"
        ]
        for browser_exe in explicit_browsers:
            browser_path = shutil.which(browser_exe.replace(".exe", ""))
            if browser_path:
                try:
                    subprocess.Popen([browser_path, str(filepath)])
                    return
                except Exception:
                    continue
        
        try:
            os.startfile(str(filepath), "open")
            return
        except Exception as exc:
            print(f"Failed to open with os.startfile: {exc}")

    try:
        if webbrowser.open(uri, new=2):
            return
    except Exception as exc:
        print(f"Browser launch failed: {exc}")

    browser_names = []
    if sys.platform == "darwin":
        browser_names = ["open"]
    else:
        browser_names = ["xdg-open", "google-chrome", "firefox", "chromium"]

    for browser_name in browser_names:
        browser_path = shutil.which(browser_name)
        if browser_path:
            try:
                subprocess.run([browser_path, uri], check=False)
                return
            except Exception:
                continue

    print("Could not open HTML file automatically in a browser.")
    print(f"Open the file manually: {filepath}")


def group_by_category(expenses):
    """Group expenses by category."""
    grouped = defaultdict(list)
    for expense in expenses:
        grouped[expense["category"]].append(expense)
    return grouped


def monthly_summary(expenses):
    """Return a summary report for a list of expenses."""
    if not expenses:
        return {
            "count": 0,
            "total": 0.0,
            "average": 0.0,
            "largest": 0.0,
            "smallest": 0.0,
        }

    amounts = [expense["amount"] for expense in expenses]
    return {
        "count": len(amounts),
        "total": sum(amounts),
        "average": mean(amounts),
        "largest": max(amounts),
        "smallest": min(amounts),
    }


def print_report(expenses):
    """Print an overall report for the current expenses."""
    print("\n=== Budget Summary ===")
    if not expenses:
        print("No expenses have been added yet.")
        print("Choose option 1 to add an expense first.")
        return

    print("Displaying current expense report...")
    summary = monthly_summary(expenses)
    print(f"Expense count: {summary['count']}")
    print(f"Total spent: ${summary['total']:.2f}")
    print(f"Average expense: ${summary['average']:.2f}")
    print(f"Largest expense: ${summary['largest']:.2f}")
    print(f"Smallest expense: ${summary['smallest']:.2f}")

    by_category = group_by_category(expenses)
    for category, items in sorted(by_category.items()):
        category_summary = monthly_summary(items)
        print(f"  {category}: ${category_summary['total']:.2f} ({category_summary['count']} item(s))")

    print("\nReport complete. Return to the menu to continue.")


def export_expenses_csv(expenses, filename=None):
    """Export the current expenses to a CSV file."""
    if not expenses:
        print("No expenses to export.")
        return

    filename = Path(filename) if filename else EXPORT_DIR / "budget_expenses.csv"
    with filename.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["date", "category", "amount", "description"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for expense in expenses:
            writer.writerow(
                {
                    "date": expense["date"],
                    "category": expense["category"],
                    "amount": f"{expense['amount']:.2f}",
                    "description": expense["description"],
                }
            )

    print(f"CSV export saved to {filename}")
    _open_csv_in_excel(str(filename))


def export_expenses_html(expenses, filename=None):
    """Export the current expenses to an HTML file."""
    if not expenses:
        print("No expenses to export.")
        return

    filename = Path(filename) if filename else EXPORT_DIR / "budget_expenses.html"
    rows = []
    for expense in expenses:
        rows.append(
            """
            <tr>
                <td>{date}</td>
                <td>{category}</td>
                <td>${amount:.2f}</td>
                <td>{description}</td>
            </tr>
            """.format(
                date=html.escape(expense["date"]),
                category=html.escape(expense["category"]),
                amount=expense["amount"],
                description=html.escape(expense["description"]),
            )
        )

    html_content = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Budget Tracker Export</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 24px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #aaa; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Budget Expenses</h1>
    <p>Total expenses: {len(expenses)}</p>
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Category</th>
                <th>Amount</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            {''.join(rows)}
        </tbody>
    </table>
</body>
</html>
"""

    with filename.open("w", encoding="utf-8") as handle:
        handle.write(html_content)

    print(f"HTML export saved to {filename}")
    _open_html_in_browser(str(filename))
