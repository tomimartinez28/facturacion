import re
import pdfplumber
import mysql.connector
import datetime
import os

def date_converter(date):
    x = date.split('/')
    return f'{x[0]}-{x[1]}-{x[2]}'


connection = mysql.connector.connect(
    user = 'root', 
    password = 'abcdefgh',
    host = '127.0.0.1',
    database = 'ailaacc',
    port = '3306'
)

cursor = connection.cursor() 

directory = '/Users/tomasmartinez/Documents/FACTURAS1' 



for file in os.listdir(directory):
    archivo = os.path.join (directory, file)
    with pdfplumber.open(archivo) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
    tipo_comprobante = text.split('\n')[2]
    print(text)
    for row in text.split('\n'):
        if row.startswith('Importe Total'):
            x = row.split()[-1]
            total_facturado = float(x.replace(',','.'))
        elif row.startswith('Punto de Venta'):
            punto_de_venta = row.split()[3]
            numero_comprobante = row.split()[-1]
        elif row.startswith('Razón Social'):
            fecha_emision = date_converter((row.split()[-1]))
        elif row.startswith('Período Facturado'):
            periodo_desde = (row.split()[3])
            periodo_hasta = (row.split()[4].split(sep=':')[1])
        elif row.startswith('CUIT'):
            cuit_os = row.split()[1]
    sql = f"INSERT INTO comprobantes(fecha_emision, fecha_desde, fecha_hasta, cuit_os, tipo_comprobante, punto_de_venta, numero_comprobante, importe) VALUES (STR_TO_DATE('{fecha_emision}','%d-%m-%Y'),STR_TO_DATE('{periodo_desde}','%d/%m/%Y'),STR_TO_DATE('{periodo_hasta}','%d/%m/%Y'),{cuit_os},'{tipo_comprobante}',{punto_de_venta},{numero_comprobante}, {total_facturado})"
    
    cursor.execute(sql)
    connection.commit()


