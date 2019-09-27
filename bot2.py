import json
import html2text
import html
from html.parser import HTMLParser
import requests  
import os
with open('data.txt') as json_file:
    data = json.load(json_file)
with open('conteudo06.txt', encoding="utf-8") as json_file:
    datab = json.load(json_file)
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

def bulaTodos(txtobula):
    txtobula = txtobula
    for p in datab['people']:
        nome = p['name'].lower()
        slug = p['slug'].lower()
        titulo2 = p['substance'].lower()
        indicacoes = p['indications']
        ret = ret+p
    return(ret)
def bula(txtobula):
    txtobula = txtobula.lower()
    dqz = 1
    for p in datab['people']:
        nome = p['titulo']
        tags = p['tags'].lower()
        texto1 = p['texto']
        tags = tags.split(", ")

        for i in tags:

            if i == "onfalocele":
                texto = html2text.html2text(texto1)
                texto = texto.replace('*  ',' - ') 
                texto = texto.replace('**','*')
                if dqz == 1:
                    dqz = dqz+1
            
            
            
          

def addbula(nome,apresentacao,indicacao,tg1,tg2,tg3):
    name = nome
    website = indicacao
    veio = apresentacao
    cod = tg1.lower()
    codb = tg2.lower()
    codc = tg3.lower()
    data['people'].append({
        'tag1': cod,
        'tag2': codb,
        'tag3': codc,
        'name': name,
        'website': website,
        'from': veio
    })


def rocefin(peso):
    peso = peso
    doseamoxx = peso * 80 / 2
    doseamox = round(doseamoxx, 1)
    laudo = 'Dose de Ceftriaxona para ' + str(peso) + 'kg \n' + str(doseamox) + ' mg a cada 12 horas'
    if peso < 40:
        return(laudo)
    else:
        return('Erro funcao Rocefin')

def ibuprofenoxarope(peso):
    peso = peso
    doseamoxx = peso / 2
    doseamox = round(doseamoxx, 1)
    laudo = 'Dose de Ibuprofeno Xarope para *' + str(peso) + '* kg \n' + str(doseamox) + ' mL a cada 6 horas\nAPRESENTAÇÃO: Suspensão oral gotas 100 mg/ml\n*Crianças*\nNos quadros febris, a dose usual recomendada para crianças a partir dos 6 meses de idade é de 5 a 10 mg/kg de peso corpóreo, a cada 6 a 8 horas.'
    if peso < 40:
        return(laudo)
    else:
        return('Erro funcao ibuprofenoxarope')


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

    elif action == 'rocefin':
        peso = parametros.get('pesoceft')
        calculo = crockoft(peso)
        return {'fulfillmentText': calculo}

    elif action == 'ibuprofenoxarope': ##IBU XAROPE##
        peso = parametros.get('pesoibux')
        calculo = crockoft(peso)
        return {'fulfillmentText': calculo}

    elif action == 'bulaTodos': ##IBU XAROPE##
        peso = "Diogo"
        calculo = bulaTodos(peso)
        return {'fulfillmentText': calculo}

    elif action == 'FALLBACK':
        num1 = parametros.get('doseamoxicilina')
        calculo = bula(msg)
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
