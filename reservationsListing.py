from flask import Flask, jsonify, request
import json

app = Flask(__name__)

reservations = []

@app.route('/reservations', methods=['GET', 'POST'])
def manage_reservations():
    if request.method == 'GET':
        return jsonify(reservations)
    elif request.method == 'POST':
        reservation_data = request.json
        reservations.append(reservation_data)
        save_reservations_to_file()
        return jsonify({'message': 'Reservation added successfully'}), 201

@app.route('/reservations/<string:flight_number>', methods=['DELETE'])
def delete_reservations_by_flight_number(flight_number):
    deleted_count = 0
    global reservations
    
    reservations_to_keep = []
    for reservation in reservations:
        if reservation.get('flight_number') != flight_number:
            reservations_to_keep.append(reservation)
        else:
            deleted_count += 1
    
    reservations = reservations_to_keep
    save_reservations_to_file()
    
    if deleted_count > 0:
        return jsonify({'message': f'{deleted_count} reservations with flight_number {flight_number} deleted'}), 200
    else:
        return jsonify({'message': 'No reservations with the specified flight_number'}), 404

def save_reservations_to_file():
    with open('reservations.json', 'w') as f:
        json.dump(reservations, f)

if __name__ == '__main__':
    try:
        with open('reservations.json', 'r') as f:
            reservations = json.load(f)
    except FileNotFoundError:
        reservations = []
    
    app.run()