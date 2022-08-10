from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from main import getPrediction
import os

#Salve as imagens na pasta 'static', pois o Flask fornece imagens deste diretório
UPLOAD_FOLDER = 'static/images/'

#Crie um objeto de aplicativo usando a classe Flask.
app = Flask(__name__, static_folder="static")

#Adicione impressão digital de referência.
#Cookies viajam com uma assinatura que eles afirmam ser legítima.
#Legitimidade aqui significa que a assinatura foi emitida pelo proprietário do cookie.
#Outros não podem alterar este cookie, pois ele precisa da chave secreta.
#É usado como chave para criptografar a sessão - que pode ser armazenada em um cookie.
#Cookies devem ser criptografados se contiverem informações potencialmente confidenciais.
app.secret_key = "secret key"

#Define a pasta de upload para salvar as imagens enviadas pelo usuário.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Defina a rota para estar em casa.
#O decorador abaixo vincula a rota relativa da URL à função que está decorando.
#Aqui, a função index é com '/', nosso diretório raiz.
#Executar o aplicativo nos envia para index.html.
#Note que render_template significa que ele procura o arquivo na pasta de templates.
@app.route('/')
def index():
    return render_template('index.html')

#Adicione o método Post ao decorador para permitir o envio do formulário. 
@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)  #Use este método werkzeug para proteger o nome do arquivo.
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            #getPrediction(filename)
            label = getPrediction(filename)
            flash(label)
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            flash(full_filename)
            return redirect('/')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000)) #Define port para que possamos mapear a porta do container para localhost
    app.run(debug=True, host='0.0.0.0', port=port)  #Define 0.0.0.0 para Docker