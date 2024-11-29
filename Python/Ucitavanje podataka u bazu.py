# Imports
import pymysql
import pandas as pd
import numpy as np
import json
import requests
import random
from sqlalchemy import create_engine, text

data = {
    r'..\CSV\InicijalnoPunjenje.csv': '2024-10-31 01:29:58',
    r'..\CSV\InkrementalnoPunjenje1.csv': '2024-11-01 01:30:58',
    r'..\CSV\InkrementalnoPunjenje2.csv': '2024-11-02 01:31:26',
    r'..\CSV\InkrementalnoPunjenje3.csv': '2024-11-03 01:31:15',
    r'..\CSV\InkrementalnoPunjenje4.csv': '2024-11-04 01:31:28',
    r'..\CSV\InkrementalnoPunjenje5.csv': '2024-11-05 01:31:26',
    r'..\CSV\InkrementalnoPunjenje6.csv': '2024-11-06 01:31:29',
    r'..\CSV\InkrementalnoPunjenje7.csv': '2024-11-07 01:31:22',
    r'..\CSV\InkrementalnoPunjenje8.csv': '2024-11-08 01:31:26',
    r'..\CSV\InkrementalnoPunjenje9.csv': '2024-11-09 01:31:27',
    r'..\CSV\InkrementalnoPunjenje10.csv': '2024-11-10 01:31:24',
    
}


for path, datetime in data.items():
    # Database connection
    user = 'root'
    passw = 'root'
    host =  'localhost' 
    port = 3306 
    database = 'crimes_in_chicago'
    mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database , echo=False)
    print(mydb)
    connection = mydb.connect()
    
    print(f"Početak punjenja podataka u MySQL iz datoteke : {path.split('\\')[-1]}")
    # Import CSV Sales_Products file
    CSV_FILE_PATH = path
    df = pd.read_csv(CSV_FILE_PATH, delimiter=',')
    print("CSV size: ", df.shape)

    # Print leading rows of dataframe
    print(df.head(20))

    #Lokacija
    location_data = pd.DataFrame({
        'adresa': df['Block'].str.upper(),  
        'strana_grada': df['Strana_svijeta'],
        'last_modified':datetime  
    })
    print(location_data)
    existing_addresses = pd.read_sql("SELECT adresa FROM lokacija", con=mydb)
    lokacija = location_data.drop_duplicates(subset=['adresa'])
    print(lokacija)
    lokacija = lokacija[~lokacija['adresa'].isin(existing_addresses['adresa'])]
    print(lokacija)

    #print(lokacija[lokacija['adresa'] == '003XX E Randolph St'])
    lokacija.to_sql(con=mydb, name='lokacija', if_exists='append', index=False)
    print("Podaci su uspješno uneseni u tablicu 'lokacija'.")


    #TipZlocina
    primary_data = pd.DataFrame({
        'tip_zlocina': df['Primary Type'],  
        'cijena_zlocina': df['price'],
        'last_modified':datetime  
    })
    print(primary_data)
    existing_primary_data = pd.read_sql("SELECT tip_zlocina FROM tip_zlocina", con=mydb)
    tip_zlocina = primary_data.drop_duplicates(subset=['tip_zlocina'])
    print(tip_zlocina)
    tip_zlocina = tip_zlocina[~tip_zlocina['tip_zlocina'].isin(existing_primary_data['tip_zlocina'])]
    tip_zlocina.to_sql(con=mydb, name='tip_zlocina', if_exists='append', index=False)
    print("Podaci su uspješno uneseni u tablicu 'tip_zlocina'.")

    #Pocinitelj
    offender_data= pd.DataFrame({
          'spol': df['spol'],
          'prijasnje_kaznjavnanje': df['prijasnje_kaznjavanje'].astype(str),
          'id_dobna_skupina': df['id_dobna_skupina'],
          'last_modified':datetime
      })

      
    print(offender_data)
    offender_data.to_sql(con=mydb, name='pocinitelj', if_exists='append', index=False)
    print("Podaci su uspješno uneseni u tablicu 'pocinitelj'.")


    #PocinjeniZlocini
    tip_zlocina_fk, lokacija_fk =[], []

    for i, row in df.iterrows():
        lokacija_query = text(f"SELECT id FROM lokacija WHERE adresa = :adresa;")
        lokacija_result = connection.execute(lokacija_query, {'adresa': row['Block']}).fetchone()
        if lokacija_result:
            lokacija_fk.append(lokacija_result[0])

            
        tip_zlocina_query = text(f"SELECT id FROM tip_zlocina WHERE tip_zlocina = :tip_zlocina;")
        tip_zlocina_result = connection.execute(tip_zlocina_query, {'tip_zlocina': row['Primary Type']}).fetchone()
        if tip_zlocina_result:
            tip_zlocina_fk.append(tip_zlocina_result[0]) 

    zlocini_data=pd.DataFrame({
      'datum': df['Date'],
      'vrijeme':df['Time'],
      'opis_zlocina':df['Description'],
      'uhicenje':df['Arrest'].astype(str),
      'obiteljsko_zlostavljanje':df['Domestic'].astype(str),
      'mjesto_i_okruzenje':df['Location Description'],
      'kolicina_svjedoka':df['Witnesses'],
      'id_pocinitelj':df['id_pocinitelja'],
      'id_tip_zlocina':tip_zlocina_fk,
      'id_lokacija':lokacija_fk,
      'last_modified':datetime    
                    })
    print(zlocini_data)
    zlocini_data.to_sql(con=mydb, name='pocinjeni_zlocini', if_exists='append', index=False)
    print("Podaci su uspješno uneseni u tablicu 'pocinjeni_zlocini'.")
    print(f"Završetak punjenja podataka u MySQL iz datoteke : {path.split('\\')[-1]}")

print("Inicijano punjenje + svih 10 inkrementalnih punjenja su izvršeni.")
