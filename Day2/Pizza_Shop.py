import json
import re
import webbrowser
from datetime import datetime
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / 'pizza_shop_state.json'
number_of_pizzas = 0  # using assignment operator to initialize a variable
pizzas = []  # using list data structure to store pizza orders
status_options = ['pending', 'preparing', 'ready', 'delivered']  # list of possible order statuses
cost_by_size = {
    'small': 5.0,
    'medium': 7.5,
    'large': 10.0,
    'su': 12.0
}  # using dict data structure to store pizza size costs


def load_state():
    global number_of_pizzas, pizzas
    if not STATE_FILE.exists():
        return
    try:
        with STATE_FILE.open('r', encoding='utf-8') as f:
            state = json.load(f)
        pizzas = [normalize_pizza_order(pizza) for pizza in state.get('pizzas', [])]
        if pizzas:
            number_of_pizzas = max(pizza.get('order_number', 0) for pizza in pizzas)
        else:
            number_of_pizzas = 0
        print(f"Loaded {len(pizzas)} pizza orders from state file.")
    except (json.JSONDecodeError, OSError):
        print('Could not read state file. Starting with empty order data.')
        pizzas = []
        number_of_pizzas = 0


def save_state():
    try:
        with STATE_FILE.open('w', encoding='utf-8') as f:
            json.dump({'pizzas': pizzas}, f, indent=2)
    except OSError:
        print('Failed to save state file.')


def normalize_pizza_order(pizza):
    timestamp = get_current_timestamp()
    pizza.setdefault('order_number', 0)
    pizza.setdefault('order_name', '')
    pizza.setdefault('order_phone', '')
    pizza.setdefault('location', '')
    pizza.setdefault('size', '')
    pizza.setdefault('toppings', '')
    pizza.setdefault('status', status_options[0])
    pizza.setdefault('cost', 0.0)
    pizza.setdefault('created_at', timestamp)
    pizza.setdefault('updated_at', timestamp)
    return pizza


def get_current_timestamp():
    return datetime.now().isoformat(sep=' ', timespec='seconds')


def format_timestamp(timestamp):
    return timestamp if timestamp else 'N/A'


def validate_phone(phone):
    digits = re.sub(r'\D', '', phone)
    if len(digits) < 10 or len(digits) > 15:
        return False
    if digits.startswith('0') or digits.startswith('44'):
        return True
    return False


def validate_uk_postcode(postcode):
    normalized = postcode.strip().upper().replace(' ', '')
    pattern = re.compile(
        r'^(?:[A-Z]{1,2}\d{1,2}[A-Z]?|[A-Z]{1,2}\d[A-Z]|GIR)\d[A-Z]{2}$'
    )
    return bool(pattern.match(normalized))


def print_menu():
    print('Welcome to the Pizza Shop!')
    print('1. Order a pizza')
    print('2. View all pizzas')
    print('3. Total order count')
    print('4. Total order value')
    print('5. Update order status')
    print('6. Generate HTML report')
    print('7. Exit')


def update_order_status():
    if not pizzas:
        print('No pizza orders to update.')
        return

    try:
        order_number = int(input('Enter order number to update: ').strip())
    except ValueError:
        print('Invalid order number.')
        return

    matched = next((pizza for pizza in pizzas if pizza['order_number'] == order_number), None)
    if not matched:
        print('Order number not found.')
        return

    print('Status options:')
    for idx, status in enumerate(status_options, start=1):
        print(f"{idx}. {status}")

    choice = input('Choose new status: ').strip()
    try:
        status_index = int(choice) - 1
        new_status = status_options[status_index]
    except (ValueError, IndexError):
        print('Invalid status choice.')
        return

    matched['status'] = new_status  # using assignment operator to change order state
    matched['updated_at'] = get_current_timestamp()
    save_state()  # persist after state change
    print(f"Order {order_number} status updated to {new_status}.")


def generate_html_report():
    report_file = Path(__file__).resolve().parent / 'pizza_shop_report.html'

    # calculate breakdown by size and totals
    size_breakdown = {}  # dict to store count and value by size
    for pizza in pizzas:
        size = pizza['size']
        if size not in size_breakdown:
            size_breakdown[size] = {'count': 0, 'total': 0.0}
        size_breakdown[size]['count'] += 1
        size_breakdown[size]['total'] += pizza['cost']

    total_orders = len(pizzas)
    total_value = sum(pizza['cost'] for pizza in pizzas)

    # generate HTML with Bootstrap from CDN
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pizza Shop Dashboard Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css"/>
    <style>
        body {{
            background-color: #f8f9fa;
            padding: 20px;
        }}
        .dashboard {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 30px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 15px;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .dashboard-header {{
            display: flex;
            align-items: center;
            gap: 18px;
            margin-bottom: 24px;
        }}
        .pizza-logo {{
            width: 72px;
            height: 72px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #ffd54f 0%, #ffb300 100%);
            border-radius: 22px;
            box-shadow: 0 8px 18px rgba(0,0,0,0.12);
        }}
        .pizza-logo svg {{
            width: 44px;
            height: 44px;
        }}
        table {{
            font-size: 14px;
        }}
        .status-badge {{
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}
        .status-pending {{
            background-color: #ffc107;
            color: #000;
        }}
        .status-preparing {{
            background-color: #17a2b8;
            color: #fff;
        }}
        .status-ready {{
            background-color: #28a745;
            color: #fff;
        }}
        .status-delivered {{
            background-color: #6c757d;
            color: #fff;
        }}
        #map {{
            width: 100%;
            height: 420px;
            border-radius: 12px;
            margin-bottom: 24px;
        }}
    </style>
</head>
<body>
    <div class="container-lg">
        <div class="dashboard-header">
            <div class="pizza-logo">
                <svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <circle cx="32" cy="32" r="30" fill="#f5d07b" stroke="#cc8a2f" stroke-width="4"/>
                    <path d="M10 32c0-8.8 7.2-16 16-16 1.6 0 3.2.2 4.7.6l7.9 23.7-28.6 9.6C10.8 47.1 10 39.7 10 32Z" fill="#f2bb4f"/>
                    <circle cx="25" cy="37" r="4" fill="#d65a32"/>
                    <circle cx="36" cy="27" r="4" fill="#d65a32"/>
                    <circle cx="42" cy="38" r="4" fill="#d65a32"/>
                    <path d="M32 6c14.3 0 26 11.7 26 26S46.3 58 32 58 6 46.3 6 32 17.7 6 32 6Z" fill="none" stroke="#bf7d3f" stroke-width="3" opacity="0.35"/>
                </svg>
            </div>
            <h1 class="mb-0">Pizza Shop Dashboard Report</h1>
        </div>

        <div class="row mb-4">
            <div class="col-md-6">
                <div class="stat-card">
                    <div class="stat-label">Total Orders</div>
                    <div class="stat-value">{total_orders}</div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="stat-card">
                    <div class="stat-label">Total Revenue</div>
                    <div class="stat-value">${total_value:.2f}</div>
                </div>
            </div>
        </div>

        <div class="dashboard">
            <h3 class="mb-3">Revenue Breakdown by Size</h3>
            <table class="table table-striped">
                <thead class="table-dark">
                    <tr>
                        <th>Pizza Size</th>
                        <th>Count</th>
                        <th>Total Value</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
"""

    for size in sorted(size_breakdown.keys()):
        count = size_breakdown[size]['count']
        total = size_breakdown[size]['total']
        percentage = (total / total_value * 100) if total_value > 0 else 0
        html_content += f"""                    <tr>
                        <td><strong>{size.upper()}</strong></td>
                        <td>{count}</td>
                        <td>${total:.2f}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
"""

    html_content += """                </tbody>
            </table>
        </div>

        <div class="dashboard">
            <h3 class="mb-3">Order Location Map</h3>
            <div id="map"></div>
        </div>

        <div class="dashboard">
            <h3 class="mb-3">All Orders</h3>
            <table class="table table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Order #</th>
                        <th>Size</th>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Location</th>
                        <th>Toppings</th>
                        <th>Status</th>
                        <th>Cost</th>
                        <th>Created</th>
                        <th>Updated</th>
                    </tr>
                </thead>
                <tbody>
"""

    for pizza in pizzas:
        status = pizza['status']
        status_class = f"status-{status}"
        created_at = format_timestamp(pizza.get('created_at'))
        updated_at = format_timestamp(pizza.get('updated_at'))
        html_content += f"""                    <tr>
                        <td>#{pizza['order_number']}</td>
                        <td><strong>{pizza['size'].upper()}</strong></td>
                        <td>{pizza.get('order_name', 'N/A')}</td>
                        <td>{pizza.get('order_phone', 'N/A')}</td>
                        <td>{pizza.get('location', 'N/A')}</td>
                        <td>{pizza['toppings']}</td>
                        <td><span class=\"status-badge {status_class}\">{status.upper()}</span></td>
                        <td>${pizza['cost']:.2f}</td>
                        <td>{created_at}</td>
                        <td>{updated_at}</td>
                    </tr>
"""

    html_content += """                </tbody>
            </table>
        </div>

        <footer class=\"text-center text-muted mt-5\">
            <p>Generated by Pizza Shop System</p>
        </footer>
    </div>

    <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js\"></script>
    <script src=\"https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js\"></script>
    <script>
        const orderMarkers = [
"""

    for pizza in pizzas:
        html_content += f"""            {{ location: \"{pizza.get('location', 'N/A')}\", order_name: \"{pizza.get('order_name', 'N/A')}\", status: \"{pizza['status']}\", cost: {pizza['cost']:.2f} }},\n"""

    html_content += """        ];

        const postcodeCoordinates = {
            'L1': [53.4025, -2.9910],
            'L2': [53.4095, -2.9824],
            'L3': [53.4097, -2.9879],
            'L4': [53.4177, -3.0002],
            'L5': [53.4244, -2.9999],
            'L6': [53.4352, -2.9812],
            'L7': [53.4397, -2.9778],
            'L8': [53.4478, -2.9880],
            'L9': [53.4462, -2.9475],
            'L10': [53.4717, -2.9660],
            'L11': [53.4565, -3.0047],
            'L12': [53.4308, -2.9804],
            'L13': [53.4046, -2.9944],
            'L14': [53.4038, -2.9701],
            'L15': [53.3827, -2.9787],
            'L16': [53.3807, -2.9735],
            'L17': [53.3796, -2.9938],
            'L18': [53.3552, -3.0016],
            'L19': [53.3650, -2.9739],
            'L20': [53.3820, -2.9303],
            'L21': [53.3820, -2.9303],
            'L22': [53.3820, -2.9303],
            'L23': [53.3820, -2.9303],
            'L24': [53.3820, -2.9303],
            'L25': [53.3820, -2.9303],
            'L26': [53.3820, -2.9303],
            'L27': [53.3820, -2.9303],
            'L28': [53.3820, -2.9303],
            'L29': [53.3820, -2.9303],
            'L30': [53.3820, -2.9303],
            'L31': [53.3820, -2.9303],
            'L32': [53.3820, -2.9303],
            'L33': [53.3820, -2.9303],
            'L34': [53.3820, -2.9303],
            'L35': [53.3820, -2.9303],
            'L36': [53.3820, -2.9303],
            'L37': [53.3820, -2.9303],
            'L38': [53.3820, -2.9303],
            'L39': [53.3820, -2.9303],
            'L40': [53.3820, -2.9303],
            'L41': [53.3820, -2.9303],
            'L42': [53.3820, -2.9303],
            'L43': [53.3820, -2.9303],
            'L44': [53.3820, -2.9303],
            'L45': [53.3820, -2.9303],
            'L46': [53.3820, -2.9303],
            'L47': [53.3820, -2.9303],
            'L48': [53.3820, -2.9303],
            'L49': [53.3820, -2.9303],
            'L50': [53.3820, -2.9303],
            'CH49': [53.4100, -3.1600]
        };

        const map = L.map('map').setView([53.408, -2.991], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        const markers = [];
        orderMarkers.forEach(order => {
            const prefix = order.location.split(' ')[0];
            const coords = postcodeCoordinates[prefix] || [53.408, -2.991];
            const marker = L.marker(coords).addTo(map);
            marker.bindPopup(`<strong>${order.order_name}</strong><br>${order.location}<br>${order.status} - £${order.cost.toFixed(2)}`);
            markers.push(marker);
        });

        if (markers.length) {
            const group = L.featureGroup(markers);
            map.fitBounds(group.getBounds().pad(0.2));
        }
    </script>
</body>
</html>
"""

    try:
        with report_file.open('w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML report generated: {report_file}")
        print('Opening the report in your default browser...')
        webbrowser.open(report_file.resolve().as_uri())
    except OSError:
        print('Failed to generate HTML report.')


load_state()

while True:
    print_menu()
    choice = input('Please enter your choice: ').strip()

    if choice == '1':
        name = input('Enter customer name: ').strip()
        while True:
            phone = input('Enter customer phone: ').strip()
            if validate_phone(phone):
                break
            print('Invalid phone number. Enter a UK phone number with 10 to 15 digits.')

        while True:
            location = input('Enter location (UK postcode): ').strip()
            if validate_uk_postcode(location):
                location = location.upper()
                break
            print('Invalid UK postcode. Please enter a valid postcode like SW1A 1AA.')

        size = input('Choose pizza size (small, medium, large, su): ').strip().lower()
        toppings = input('Choose toppings (comma separated): ')

        if size not in cost_by_size:  # using membership operator to validate size
            print('Invalid size. Please choose small, medium, large, or su.')
            continue

        number_of_pizzas += 1
        cost = cost_by_size[size]  # using dict lookup to get pizza cost
        timestamp = get_current_timestamp()

        pizza = {
            'order_number': number_of_pizzas,
            'order_name': name,
            'order_phone': phone,
            'location': location,
            'size': size,
            'toppings': toppings,
            'status': status_options[0],  # order starts as pending
            'cost': cost,  # store the pizza cost
            'created_at': timestamp,
            'updated_at': timestamp,
        }
        pizzas.append(pizza)  # add the pizza order to the list
        save_state()  # persist after state change

        print(f"You ordered a {size} pizza with {toppings}. Order status: {pizza['status']}. Cost: ${pizza['cost']:.2f}")
    elif choice == '2':
        if not pizzas:
            print('No pizza orders yet.')
        else:
            print('Current pizza orders:')
            for pizza in pizzas:
                print(
                    f"Order {pizza['order_number']}: {pizza['size']} pizza for {pizza.get('order_name', 'N/A')} "
                    f"({pizza.get('order_phone', 'N/A')}) at {pizza.get('location', 'N/A')} with {pizza['toppings']} "
                    f"- status: {pizza['status']} - cost: ${pizza['cost']:.2f} "
                    f"- created: {format_timestamp(pizza.get('created_at'))} - updated: {format_timestamp(pizza.get('updated_at'))}"
                )
    elif choice == '3':
        total_count = len(pizzas)  # using len() to count orders
        print(f'Total order count: {total_count}')
    elif choice == '4':
        total_value = sum(pizza['cost'] for pizza in pizzas)  # using sum and comprehension to total order value
        print(f'Total order value: ${total_value:.2f}')
    elif choice == '5':
        update_order_status()
    elif choice == '6':
        generate_html_report()
    elif choice == '7':
        print('Thank you for visiting the Pizza Shop. Goodbye!')
        break
    else:
        print('Invalid choice. Please try again.')