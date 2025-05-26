import os
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from services.whatsapp_service import WhatsAppService

app = Flask(__name__)

# Configuration
AVAILABLE_SLOTS = [f"{h:02d}:00" for h in range(8, 12)] + [f"{h:02d}:00" for h in range(14, 18)]
appointments = {}
lock = threading.Lock()

# Initialize WhatsApp service (uses Twilio if configured, else pywhatkit)
whatsapp_service = WhatsAppService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/available_slots')
def available_slots_api():
    with lock:
        free_slots = [slot for slot in AVAILABLE_SLOTS if slot not in appointments]
    return jsonify({'slots': free_slots})

@app.route('/api/book', methods=['POST'])
def book_slot():
    data = request.get_json()
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    time_slot = data.get('timeSlot', '').strip()

    if not name or not phone or not time_slot:
        return jsonify({'error': 'Todos os campos são obrigatórios.'}), 400

    if time_slot not in AVAILABLE_SLOTS:
        return jsonify({'error': 'Horário inválido.'}), 400

    with lock:
        if time_slot in appointments:
            return jsonify({'error': 'Horário já reservado.'}), 409
        appointments[time_slot] = {'name': name, 'phone': phone}

    # Compose message
    message = f"Novo agendamento:\nCliente: {name}\nCelular: {phone}\nHorário: {time_slot}"
    # Send message asynchronously
    threading.Thread(target=whatsapp_service.send_message, args=(phone, message), daemon=True).start()

    return jsonify({'message': f"Agendamento confirmado para {time_slot}. A profissional será notificada para confirmar."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)