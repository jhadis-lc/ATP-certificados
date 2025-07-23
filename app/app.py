from flask import Flask, render_template, request, send_file, jsonify
import qrcode
import io
import os
from datetime import datetime

app = Flask(__name__)

# Variable para mantener el contador
counter = 1

def generate_certificate_id():
    global counter
    certificate_id = f"2025-{counter:05d}"
    counter += 1
    return certificate_id

def generate_qr_code(data, size=(300, 300)):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize(size)
    
    # Guardar en memoria
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return img_buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_certificate():
    # Generar ID único
    certificate_id = generate_certificate_id()
    
    # URL base (debes cambiar esto por tu dominio de GitHub Pages)
    base_url = "https://tu-usuario.github.io/tu-repositorio/verificar"
    verification_url = f"{base_url}?id={certificate_id}"
    
    # Generar QR
    qr_buffer = generate_qr_code(verification_url)
    
    # Guardar QR en archivo
    qr_filename = f"qr_{certificate_id}.png"
    with open(f"static/qr_codes/{qr_filename}", "wb") as f:
        f.write(qr_buffer.getvalue())
    
    return jsonify({
        'certificate_id': certificate_id,
        'verification_url': verification_url,
        'qr_url': f"/static/qr_codes/{qr_filename}"
    })

@app.route('/verify')
def verify_certificate():
    certificate_id = request.args.get('id', '')
    return render_template('verify.html', certificate_id=certificate_id)

if __name__ == '__main__':
    # Crear directorio para QR codes
    os.makedirs('static/qr_codes', exist_ok=True)
    app.run(debug=True)