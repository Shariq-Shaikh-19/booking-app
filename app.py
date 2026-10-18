from flask import Flask, render_template, request
import uuid

try:
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
        tickets = request.form.get("tickets", "")

        if not name:
            return "Full name is required."

        if not email:
            return "Email is required."

        if "@" not in email:
            return "Invalid email address."

        if not phone.isdigit():
            return "Phone number must contain only numbers."

        if len(phone) != 10:
            return "Phone number must contain 10 digits."

        if category not in ticket_prices:
            return "Invalid ticket category."

        try:
            tickets = int(tickets)

        except ValueError:
            return "Invalid number of tickets."


        if not 1 <= tickets <= 10:
            return "You must select at least one ticket."

        price_per_ticket = ticket_prices[category]

        total_price = price_per_ticket * tickets

        ticket_id = "TKT-" + str(uuid.uuid4())[:8].upper()

        ticket = {
            "id": ticket_id,
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

except Exception as e:
    print(f"The actual error is {e}")