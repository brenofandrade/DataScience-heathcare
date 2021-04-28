from flask import Flask, request, render_template, redirect, url_for
import numpy as np



app = Flask(__name__)
@app.route('/success/<idade>')
def success(idade):
    return 'Sua idade é: %s' % idade

@app.route('/',methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        idade = request.form['IDADE']
        sexo = request.form['SEXO']
        imc = request.form['IMC']

        x_input = np.array([idade, sexo, imc])

        print(x_input)
        return f'Sua idade é: {x_input}'
    return render_template('home.html')
    



if __name__ == '__main__':
    app.run(debug=True)

