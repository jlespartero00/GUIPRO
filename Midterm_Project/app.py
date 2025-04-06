from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

services = ["Portrait Photography", "Event Photography", "Documentary Photography"]
available_slots = {
    "Portrait Photography": [
        "2025-04-11 10:00",
        "2025-04-12 10:00",
        "2025-04-13 10:00",
        "2025-04-14 10:00",
        "2025-04-15 10:00"
    ],
    "Event Photography": [
        "2025-04-11 13:00",
        "2025-04-12 13:00",
        "2025-04-13 13:00",
        "2025-04-14 13:00",
        "2025-04-15 13:00"
    ],
    "Documentary Photography": [
        "2025-04-11 16:00",
        "2025-04-12 16:00",
        "2025-04-13 16:00",
        "2025-04-14 16:00",
        "2025-04-15 16:00"
    ]
}



bookings = []

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        service = request.form.get('service')
        booking_time = request.form.get('booking_time')
        special_requests = request.form.get('special_requests')

        if not name or not email or not service or not booking_time:
            return render_template('book.html', error="All fields are required!", services=services, available_slots=available_slots)

        if booking_time in available_slots[service]:
            available_slots[service].remove(booking_time)
            bookings.append({
                "name": name,
                "email": email,
                "service": service,
                "booking_time": booking_time,
                "special_requests": special_requests
            })
            return redirect(url_for('confirmation', name=name, booking_time=booking_time, service=service))
        else:
            return render_template('book.html', error="Sorry, that time slot is already taken.", services=services, available_slots=available_slots)

    return render_template('book.html', services=services, available_slots=available_slots)

@app.route('/confirmation')
def confirmation():
    name = request.args.get('name')
    booking_time = request.args.get('booking_time')
    service = request.args.get('service')
    return render_template('confirmation.html', name=name, booking_time=booking_time, service=service)

if __name__ == '__main__':
    app.run(debug=True)
