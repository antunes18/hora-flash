from flask import Flask, render_template_string, request, jsonify
import pywhatkit
import threading
from datetime import datetime

app = Flask(__name__)

# Professional WhatsApp number (with country code, e.g. Brazil +55)
# PROFESSIONAL_WHATSAPP = "+5563991171042"  # CHANGE to actual number before use

# Available time slots as strings (hour:minute)
# 8:00 to 12:00 (8,9,10,11) and 14:00 to 18:00 (14,15,16,17)
# Using one hour slots starting at these times
available_slots = [f"{h:02d}:00" for h in range(8, 12)] + [f"{h:02d}:00" for h in range(14, 18)]

# Dictionary to store booked appointments: slot_time -> {name, phone}
appointments = {}

# Lock to synchronize access to appointments
lock = threading.Lock()


@app.route("/")
def index():
    # Single-page HTML with Tailwind CSS and JS for frontend
    html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Agendamento Serviço Estético</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-b from-pink-200 via-purple-200 to-indigo-200 min-h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-lg p-6 max-w-md w-full">
        <h1 class="text-2xl font-bold mb-4 text-center text-purple-700">Agende seu Horário</h1>
        <form id="bookingForm" class="space-y-4">
            <div>
                <label for="name" class="block text-purple-800 font-semibold mb-1">Nome:</label>
                <input type="text" id="name" name="name" required placeholder="Seu nome"
                       class="w-full px-3 py-2 border border-purple-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500" />
            </div>
            <div>
                <label for="phone" class="block text-purple-800 font-semibold mb-1">Celular (com DDD):</label>
                <input type="tel" id="phone" name="phone" required placeholder="Ex: 11999999999"
                       pattern="\\d{10,13}" title="Digite o número de celular com DDD, só números"
                       class="w-full px-3 py-2 border border-purple-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500" />
            </div>
            <div>
                <label for="timeSlot" class="block text-purple-800 font-semibold mb-1">Escolha o horário:</label>
                <select id="timeSlot" name="timeSlot" required
                        class="w-full px-3 py-2 border border-purple-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500">
                    <option value="">Carregando horários disponíveis...</option>
                </select>
            </div>
            <button type="submit"
                    class="w-full bg-purple-600 text-white font-semibold py-2 rounded hover:bg-purple-700 transition-colors">
                Agendar
            </button>
        </form>

        <div id="message" class="mt-4 text-center font-semibold"></div>
    </div>

    <script>
        async function fetchAvailableSlots() {
            const select = document.getElementById('timeSlot');
            select.innerHTML = '<option value="">Carregando horários disponíveis...</option>';
            try {
                const response = await fetch('/api/available_slots');
                if (!response.ok) throw new Error('Erro ao buscar horários');
                const data = await response.json();
                select.innerHTML = '';
                if(data.slots.length === 0) {
                    select.innerHTML = '<option value="">Nenhum horário disponível</option>';
                } else {
                    data.slots.forEach(slot => {
                        const option = document.createElement('option');
                        option.value = slot;
                        option.textContent = slot;
                        select.appendChild(option);
                    });
                }
            } catch (error) {
                select.innerHTML = '<option value="">Erro ao carregar horários</option>';
            }
        }

        document.getElementById('bookingForm').addEventListener('submit', async function(event){
            event.preventDefault();
            const messageDiv = document.getElementById('message');
            messageDiv.textContent = '';
            const name = document.getElementById('name').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const timeSlot = document.getElementById('timeSlot').value;

            if(!name || !phone || !timeSlot) {
                messageDiv.textContent = 'Por favor, preencha todos os campos.';
                messageDiv.className = 'mt-4 text-center font-semibold text-red-600';
                return;
            }

            messageDiv.textContent = 'Enviando agendamento...';
            messageDiv.className = 'mt-4 text-center font-semibold text-purple-600';

            try {
                const response = await fetch('/api/book', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, phone, timeSlot})
                });
                const data = await response.json();
                if(response.ok) {
                    messageDiv.textContent = data.message;
                    messageDiv.className = 'mt-4 text-center font-semibold text-green-600';
                    // Refresh available slots after booking 
                    fetchAvailableSlots();
                    // Clear the form inputs
                    document.getElementById('bookingForm').reset();
                } else {
                    messageDiv.textContent = data.error;
                    messageDiv.className = 'mt-4 text-center font-semibold text-red-600';
                    // Refresh available slots in case of concurrency issues
                    fetchAvailableSlots();
                }
            } catch(err) {
                messageDiv.textContent = 'Erro ao enviar o agendamento.';
                messageDiv.className = 'mt-4 text-center font-semibold text-red-600';
            }
        });

        // Load available slots on page load
        fetchAvailableSlots();
    </script>
</body>
</html>
    """
    return render_template_string(html)


@app.route("/api/available_slots")
def available_slots_api():
    # Return list of slots NOT booked yet
    with lock:
        free_slots = [slot for slot in available_slots if slot not in appointments]
    return jsonify({"slots": free_slots})

def send_whatsapp_message(name, phone, timeSlot):
    # Compose message to professional
    message = f"Novo agendamento:\nCliente: {name}\nCelular: {phone}\nHorário: {timeSlot}"
    # pywhatkit requires scheduled time: schedule 1 min later than current time
    now = datetime.now()
    hour = now.hour
    minute = now.minute + 1
    # Adjust time if minute over 59
    if minute > 59:
        minute = 0
        hour = (hour + 1) % 24
    try:
       # pywhatkit.sendwhatmsg(PROFESSIONAL_WHATSAPP, message, hour, minute, wait_time=30, close_time=5, tab_close=True)
        pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=10)
    except Exception as e:
        print(f"Erro ao enviar WhatsApp: {e}")

@app.route("/api/book", methods=["POST"])
def book_slot():
    data = request.get_json()
    name = data.get("name", "").strip()
    phone = data.get("phone",    "").strip()
    phone = '+55' + phone
    timeSlot = data.get("timeSlot", "").strip()

    if not name or not phone or not timeSlot:
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400

    with lock:
        if timeSlot not in available_slots:
            return jsonify({"error": "Horário inválido."}), 400
        if timeSlot in appointments:
            return jsonify({"error": "Horário já reservado."}), 409
        # Reserve slot
        appointments[timeSlot] = {"name": name, "phone": phone}

    # Send WhatsApp notification in a separate thread (so we do not block)
    threading.Thread(target=send_whatsapp_message, args=(name, phone, timeSlot), daemon=True).start()

    return jsonify({"message": f"Agendamento confirmado para {timeSlot}. A profissional será notificada para confirmar."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
   