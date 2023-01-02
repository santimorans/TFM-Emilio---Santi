import dash
from dash import dcc
from dash import html
#import pandas as pd
import plotly.graph_objects as go
#import pandas as pd
#import boto3
#from boto3.dynamodb.conditions import Key
import os
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

app.layout = html.Div([    
                html.Div([
                    html.Img(src='https://github.com/santimorans/TFM-Emilio---Santi/blob/f193a709be7124c51217d759d5bf90bad50c4de5/Imagen%20web.jpg'),
                    html.H1('ALGORITMOS DE INVERSIÓN EN OPCIONES FINANCIERAS'),
                    html.Div([dcc.Dropdown(                
                                id= 'sel_broker', 
                                options=['iBROKER','renta4banco'],
                                placeholder= 'Elige tu bróker',
                                ),
                                        html.Div(id='form_login'),
                                        html.Div(id='algoritmos_ibroker'),
                                        html.Div(id='algoritmos_renta4'), 
                                        ])                         
                            ])
                                                
                        ])                   
                        
                    #])
                

@app.callback(
    dash.dependencies.Output('form_login', 'children'),
    dash.dependencies.Input('sel_broker', 'value'))
    
def form_login_broker(value):
    if value=='iBROKER':
        form_login = html.Div([
        html.Br(),
        dcc.Input(id="user_ibroker", type="text", placeholder="Usuario iBROKER", debounce=True),
        html.Br(),
        html.Br(),
        dcc.Input(id="password_ibroker", type="password", placeholder="Contraseña iBROKER", debounce=True),    
        html.Br(),
        html.Br(),
        html.Button("Iniciar sesión", id="btn_login"),
        html.Div('Cuando presiones "Iniciar sesión", se comprobará que la contraseña es correcta en el bróker y que la tenemos actualizada, tardaremos unos segundos'),
        ]),
    elif value=='renta4banco':
        form_login = html.Div([        
        html.Br(),
        dcc.Input(id="user_renta4", type="text", placeholder="Usuario renta4banco", debounce=True),
        html.Br(),
        html.Br(),
        dcc.Input(id="password_renta4", type="password", placeholder="Contraseña renta4banco", debounce=True),
        html.Br(),
        html.Br(),
        dcc.Input(id="NIF", type="text", placeholder="NIF/CIF", debounce=True),    
        html.Br(),
        html.Br(),
        html.Button("Iniciar sesión", id="btn_login"),
        html.Div('Cuando presiones "Iniciar sesión", se comprobará que la contraseña es correcta en el bróker y que la tenemos actualizada, tardaremos unos segundos'),
        ])
    else:
        form_login = []
    return form_login

@app.callback(
    dash.dependencies.Output('algoritmos_ibroker', 'children'),
    [dash.dependencies.Input("btn_login", "n_clicks"),
    dash.dependencies.Input('user_ibroker', 'value'),
    dash.dependencies.Input('password_ibroker', 'value')]
    )

def password_control_ibroker(n_clicks,user,password):
    
    def acceso_ibroker():
        """
        Esta función accede a la cuenta de Ibroker del usuario que está accediendo
        """
        s = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') # Permite ejecutar el programa sin navegar en la web abriendo ventanas
         
        driver = webdriver.Chrome(service=s, options = options)
        driver.get('https://www.ibroker.es')

        user_ibroker = user
        password_ibroker = password 
        usuario = driver.find_element(By.XPATH,'/html/body/header/div[1]/div/div[3]/div/div/form/input[1]')
        usuario.send_keys(user_ibroker)
        contraseña = driver.find_element(By.XPATH,'/html/body/header/div[1]/div/div[3]/div/div/form/input[2]')
        contraseña.send_keys(password_ibroker)
        login = driver.find_element(By.XPATH,'//*[@id="btn-login"]')
        login.click()
        try:
            #if driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/span[1]').text.split(':')[0] == 'usuario':
            driver.find_element(By.XPATH,'//*[@id="LogoutLink"]').click()            
            resultado = "El inicio de sesión ha sido correcto"
        except:
            resultado = "Error: El usuario y la contraseña no coinciden."
        return resultado
    
    
    
    if n_clicks==None:
        algoritmos = []
        
        pass
    if n_clicks is not None:
        resultado = acceso_ibroker()
        if resultado == "El inicio de sesión ha sido correcto.":
            algoritmos = html.Div([resultado,' ','Aquí se mostrarán los algoritmos'])
        else:
            algoritmos = html.Div(["Error: El usuario y la contraseña no coinciden con los del bróker"])
              
    else:
        algoritmos = []
        
    return algoritmos

@app.callback(
    dash.dependencies.Output('algoritmos_renta4', 'children'),
    [dash.dependencies.Input("btn_login", "n_clicks"),
    dash.dependencies.Input('user_renta4', 'value'),
    dash.dependencies.Input('password_renta4', 'value'),
    dash.dependencies.Input('NIF', 'value')
    ]
    )
def password_control_renta4(n_clicks,user,password,nif):
    
    def acceso_renta4():
        """
        Esta función accede a la cuenta de Ibroker del usuario que está accediendo
        """
        s = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') # Permite ejecutar el programa sin navegar en la web abriendo ventanas
         
        driver = webdriver.Chrome(service=s)#, options = options)
        driver.get('https://www.r4.com/login')

        user_renta4 = user
        password_renta4 = password 
        nif_renta4 = nif
        usuario = driver.find_element(By.XPATH,'//*[@id="usuario"]')
        usuario.send_keys(user_renta4)
        contraseña = driver.find_element(By.XPATH,'//*[@id="password"]')
        contraseña.send_keys(password_renta4)
        nif_login = driver.find_element(By.XPATH,'//*[@id="dni"]')
        nif_login.send_keys(nif_renta4)
        login = driver.find_element(By.XPATH,'//*[@id="submit"]')
        login.submit()
        
        try:            
            #driver.find_element(By.XPATH,'//*[@id="top"]/div[4]/div/div/div[4]/a/span[2]').click()            
            resultado = "El inicio de sesión ha sido correcto"
        except:
            resultado = "Error: El usuario y la contraseña no coinciden."
        return resultado
        
    
    if n_clicks==None:
        algoritmos = []       
        #pass
    if n_clicks is not None:
        resultado = acceso_renta4()
        if resultado == "El inicio de sesión ha sido correcto.":
            algoritmos = html.Div([resultado,' ','Aquí se mostrarán los algoritmos'])
        else:
            algoritmos = html.Div(["Error: El usuario y la contraseña no coinciden con los del bróker"])
    else:
        algoritmos = []
        
    return algoritmos

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(host="0.0.0.0",debug=True, port=8050)