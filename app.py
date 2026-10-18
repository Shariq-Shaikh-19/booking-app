
from flask import Flask, render_template, request
import uuid

app = Flask(__name__)

match = {
    "name": "India vs Australia",
    "team1": "India",
    "team2": "Australia",
    "date": "25 August 2026",
    "time": "7:30 PM",
    "stadium": "Wankhede Stadium"
}

ticket_prices = {
    "General": 500,
    "East Stand": 1000,
    "West Stand": 1500,
    "VIP": 3000
}


@app.route("/")
def home():
    return render_template(
        "index.html",
        match=match,
        ticket_prices=ticket_prices
    )


@app.route("/generate-ticket", methods=["POST"])
def generate_ticket():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    category = request.form.get("category", "")
    tickets_input = request.form.get("tickets", "")

    if not name:
        return "Full name is required.", 400

    if not email or "@" not in email:
        return "Please enter a valid email address.", 400

    if not phone.isdigit() or len(phone) != 10:
        return "Phone number must contain 10 digits.", 400

    if category not in ticket_prices:
        return "Invalid ticket category.", 400

    try:
        tickets = int(tickets_input)
    except (ValueError, TypeError):
        return "Invalid number of tickets.", 400

    if not 1 <= tickets <= 10:
        return "Select between 1 and 10 tickets.", 400

    price_per_ticket = ticket_prices[category]
    total_price = price_per_ticket * tickets

    ticket = {
        "id": "TKT-" + str(uuid.uuid4())[:8].upper(),
        "name": name,
        "email": email,
        "phone": phone,
        "category": category,
        "tickets": tickets,
        "price": price_per_ticket,
        "total": total_price
    }

    return render_template(
        "ticket.html",
        match=match,
        ticket=ticket
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
