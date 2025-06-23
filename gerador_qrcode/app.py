from flask import Flask, render_template, request, send_from_directory
import qrcode
import os
from io import BytesIO

app = Flask(__name__)

# Caminho para armazenar os QR codes gerados
QR_CODES_DIR = os.path.join('static', 'qr_codes')
if not os.path.exists(QR_CODES_DIR):
    os.makedirs(QR_CODES_DIR)

# Rota principal (index)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Pegar o valor inserido pelo usuário (exemplo: URL)
        data = request.form.get('data')
        
        # Gerar QR Code
        if data:
            img = qrcode.make(data)

            # Salvar como PNG
            img_path = os.path.join(QR_CODES_DIR, 'qr_code.png')
            img.save(img_path)

            # Enviar a imagem gerada para o cliente
            return render_template('index.html', qr_code_path=img_path)
    
    # Caso não tenha POST, apenas renderiza a página
    return render_template('index.html')

# Rota para servir o QR code gerado
@app.route('/static/qr_codes/<filename>')
def send_qr_code(filename):
    return send_from_directory(QR_CODES_DIR, filename)
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)    
