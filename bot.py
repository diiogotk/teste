import json
import requests  
import os
with open('data.txt') as json_file:
    data = json.load(json_file)
with open('data2.txt') as json_file:
    dataB = json.load(json_file)
from flask import Flask, request, make_response, jsonify
app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello World!'
           
        
# function for responses
def calculadora(num1, num2, sinal):
    operador = sinal
    if operador == '+':
        calculo = int(num1) + int(num2)
        return(calculo)
    elif operador == '-':
        calculo = int(num1) - int(num2)
        return(calculo)
    elif operador == '*':
        calculo = int(num1) * int(num2)
        return(calculo)
    elif operador == '/':
        calculo = int(num1) / int(num2)
        return(calculo)
    else:
        return('erro')

#DOSE AMOXICILINA
def amox(num1):
    peso = num1
    doseAdulto = 'Acima de 40kg já é considerada a dose adulta:\n *1 Comprimido 500mg* de 8/8h por 7 a 10 dias'
    doseamoxx = peso * 50 / 3 * 5 / 250
    doseamox = round(doseamoxx, 1)
    laudo = 'Dose de Amoxicilina para ' + str(peso) + 'kg \n' + str(doseamox) + ' mL a cada 8 horas por 5 a 7 dias \n Apresentação 250mg/5mL'
    if peso < 40:
        return(laudo)
    else:
        return(doseAdulto)

#IMC CALCULO#
def imc(peso, altura):
    do = peso/(altura**2)*10000
    dose = round(do, 2)
    abc = dose
    if dose >= 40:
        
        laudo = 'Obesidade grau III - Mórbida =>' + str(abc)
        laudoimc = laudo
        return(laudoimc)
    elif dose < 40 and dose > 35:
        laudoimc = 'IMC ' + str(abc) +' Obesidade grau II'
        return(laudoimc)
    elif dose < 35 and dose >= 30:
        laudoimc = 'IMC ' + str(abc) +' Obesidade grau I'
        return(laudoimc)
    elif dose < 30 and dose >= 25:
        laudoimc = 'IMC ' + str(abc) +' Acima do peso'
        return(laudoimc)
    else:
        laudoimc = 'indefinido'
        return(laudoimc)

#IMC CALCULO#
def bula(txtobula):
    for p in data['people']:
        tag01 = p['tag1']
        tag02 = p['tag2']
        tag03 = p['tag3']
        if txtobula == tag01 or txtobula == tag02 or txtobula == tag03:
            vr1 = p['website']
            vr2 = p['from']
            vr3 = p['name']
            bulaR = 'Bula de ' +vr3+ '\n' ': Indicação: \n' + vr1 + '\n Posologia: ' + vr2
            return(bulaR)

def addbula(nome,apresentacao,indicacao,tg1,tg2,tg3):
    name = nome
    website = indicacao
    veio = apresentacao
    cod = tg1.lower()
    codb = tg2.lower()
    codc = tg3.lower()
    data['doenca'].append({
        'tag1': cod,
        'tag2': codb,
        'tag3': codc,
        'nome': name,
        'tratamentoa': website,
        'tratamentob': website,
        'tratamentoc': website
        
    })







def results():
    # build a request object
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    parametros = req.get('queryResult').get('parameters')
    msg = req.get('queryResult').get('queryText')
    
    # fetch action from json

    if action == 'imc':
        peso = parametros.get('imcpeso')
        altura = parametros.get('imcaltura')
        dose = imc(peso, altura)
        return {'fulfillmentText': dose}

    elif action == 'bula':
        txtobula = parametros.get('txtbula')
        txt2 = txtobula.lower()
        doseb = bula(txt2)
        return {'fulfillmentText': doseb}

    elif action == 'addbula':
        txtobula = parametros.get('nome')
        txtobula2 = parametros.get('indicacao')
        txtobula3 = parametros.get('apresentacao')
        tg1 = parametros.get('tg1').lower()
        tg2 = parametros.get('tg2').lower()
        tg3 = parametros.get('tg3').lower()
        dosez = addbula(txtobula, txtobula3, txtobula2, tg1, tg2, tg3)
        return {'fulfillmentText': dosez}

    elif action == 'calculadora':
        num1 = parametros.get('num1')
        num2 = parametros.get('num2')
        sinal = parametros.get('operador')
        calculo = calculadora(num1, num2, sinal)
        return {'fulfillmentText': calculo}

    elif action == 'calcamox':
        num1 = parametros.get('doseamoxicilina')
        calculo = amox(num1)
        return {'fulfillmentText': calculo}

    elif action == 'FALLBACK':
        num1 = parametros.get('doseamoxicilina')
        calculo = amox(num1)
        return {'fulfillmentText': calculo}
        
        
    else:
        return {'fulfillmentText': 'Não encontrei nada sobre esse assunto.'}

    # return a fulfillment response
    #return {'fulfillmentText': 'This is a response from webhook.'}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))
if __name__ == '__main__':  
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
