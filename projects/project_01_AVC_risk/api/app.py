from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)
def predict_model(x_data):
    model = pickle.load(open('../data_process/model/modelo.pkl', 'rb'))
    resultado = model.predict_proba(x_data)
    return resultado

@app.route('/',methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        
        sexo = int(request.form['sexo'])

        idade = float(request.form['idade'])
        
        hipertensao = int(request.form['hipertensao'])

        coracao = int(request.form['doenca_coracao'])

        residencia = int(request.form['residencia'])

        glicose = float(request.form['glicose_media'])

        imc = float(request.form['imc'])

        trabalho = request.form['trabalho']

        tabagismo = request.form['tabagismo']
        

        trab_autonomo = 0
        trab_nunca = 0
        trab_privado = 0
        trab_publico = 0
        trab_crianca = 0

        if trabalho == '1':
            trab_autonomo = 1
        elif trabalho == '2':
            trab_privado = 1
        elif trabalho == '3':
            trab_publico = 1
        elif trabalho == '4':
            trab_nunca = 1
        elif trabalho == '5':
            trab_crianca = 1
        else:
            print("Unexpected Error!")
            
        




        novo_paciente = pd.DataFrame(
            {
            'sexo': sexo,
            'idade': idade,
            'hipertensao': hipertensao,
            'doenca_coracao' : coracao,
            'tipo_residencia' : residencia,
            'media_nivel_glicose' : glicose,
            'imc' : imc,
            'trabalho_Autonomo' : 0,
            'trabalho_Never_worked': 0,
            'trabalho_Privado': 0,
            'trabalho_Servidor_Publico': 0,
            'trabalho_crianca': 0,
            'tabagismo_desconhecido': 0,
            'tabagismo_fuma': 0,
            'tabagismo_fuma_eventualmente': 0,
            'tabagismo_nunca_fumou': 0
            },
            index=[0]
        )

        if tabagismo == '1':
            novo_paciente['tabagismo_fuma'][0] = 1
        elif tabagismo == '2':
            novo_paciente['tabagismo_fuma_eventualmente'][0] = 1
        elif tabagismo == '0':
            novo_paciente['tabagismo_nunca_fumou'][0] = 1
        elif tabagismo == 'na':
            novo_paciente['tabagismo_desconhecido'][0] = 1

        risco_avc = predict_model(novo_paciente)

        print(novo_paciente.dtypes)

        resultado = f'O risco de AVC é {risco_avc[0][1] * 100} %'


        #return redirect(url_for('resultado', risco_avc = risco_avc))
        return f'<h1 style="text-align:center;padding:100px"> Resultado da predição</h1><p style="color:blue; font-size:30px;text-align:center;"> O risco de AVC é: { risco_avc[0][1] *100} % </p>'
                
    return render_template('home.html')
    





if __name__ == '__main__':
    app.run(debug=True)
