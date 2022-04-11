from ipyleaflet import Map, Marker, LayersControl, MarkerCluster, LayerGroup, WidgetControl, Polyline, Popup
from ipywidgets import IntSlider, Play, Layout, Output, VBox, HTML, Button, Dropdown, Combobox, HBox, Text, AppLayout, interactive
import requests
import pandas as pd
import numpy as np
import time
import datetime
from datetime import timedelta
import chart_studio.plotly as py
import cufflinks as cf
import plotly.offline
import ast
from IPython.display import clear_output
from io import StringIO
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

'''
Klasse Steuerung übernimmt das Einlesen und Verwalten der Datensätze (per Dropdown Menü)
'''


class Steuerung:
    loadButton = Button(description='Lade die Umweltdaten', disabled=False, button_style='', 
                    layout = Layout(width = '300px'))

    
    ID_input = Text(
        value='5fedf96f576ab7001cc9310a',
        description='BoxID: ', )
    sID_input = Text(
        value='5fedf96f576ab7001cc9310c',
        description='SensorID: ', )

    loadOwnID = Button(description='Zeige Messwerte und Sensor IDs der Box', disabled=False, button_style='', 
                    layout = Layout(width = '300px'))

    loadSensorButton = Button(description='Messwerte des Sensors laden', disabled=False, button_style='', 
                    layout = Layout(width = '300px'))

    def ladeEigeneDatei(self, b):
        clear_output(wait=True)
        display(VBox([self.auswahl, self.loadButton, self.ID_input, self.loadOwnID]))
        boxID = Steuerung.ID_input.value
        #boxID1 = input('BoxID eingeben: ')
        url = 'https://api.opensensemap.org/boxes/' + boxID
        headers = {'Content-type': 'application/json'}
        sensor_box = requests.get(url, headers = headers)
        box_info = sensor_box.content
        dict_str = box_info.decode("UTF-8")
        box_info = ast.literal_eval(dict_str)
        print("------")
        for keys,values in box_info.items():
            if(keys == "sensors"):
                for data in values:
                    for k,v in data.items():
                        #print(k, v)
                        if(k == "title"):
                            print("Messwert: " + v)
                        elif (k == "_id"):
                            print("SensorID: " + v)
                    print("------")
        display(VBox([self.sID_input, self.loadSensorButton]))

    def ladeSensorDaten(self, b):
        boxID = Steuerung.ID_input.value
        sensorID1 = Steuerung.sID_input.value
        headers = {'Content-type': 'application/json'}
        url_meas = 'https://api.opensensemap.org/boxes/' + boxID + '/data/' + sensorID1 + '?&download=true&format=json'
        measurements = requests.get(url_meas, headers = headers)
        measurements.status_code
        values = measurements.content
        s=str(values,'utf-8')
        data = StringIO(s) 
        df=pd.read_json(data)
        self.data = self.datatype_correction(df)


    auswahl = Dropdown(options=['Box1', 'Box2', 'Daten von der openSenseMap'], value='Box1',
                   description='Datei auswählen:', layout = Layout(width = '300px'), disabled=False, 
                   style = {'description_width': 'initial'})
    
    def __init__(self, *args, **kwargs):
        self.data = pd.DataFrame()
        self.output_maske = Output(layout = Layout(width ='auto', max_width = '700px', border = '1px solid gray'))
        pd.set_option('display.max_rows',6)


    def loadData(self, boxID, sensorIDs):
        for ending in sensorIDs:
            url = 'https://api.opensensemap.org/boxes/' + boxID
            headers = {'Content-type': 'application/json'}
            #headers = {'Content-type': 'application/csv'}
            url_meas = 'https://api.opensensemap.org/boxes/' + boxID + '/data/' + sensorID1 + '?&download=true&format=json'
            measurements = requests.get(url_meas, headers = headers)
            values = measurements.content
            s=str(values,'utf-8')
            data = StringIO(s) 
            df=pd.read_json(data)

    def ladeDatei(self, wahl):
        #SensorDaten für OpenSenseMap herunterladen:
            if(wahl == "Daten von der openSenseMap"):
                clear_output(wait=True)
                display(VBox([self.auswahl, self.loadButton, self.ID_input, self.loadOwnID]))
            else:
                if(wahl == 'Box1'):
                    clear_output(wait=True)
                    display(VBox([self.auswahl, self.loadButton]))
                    df = pd.read_csv('res/Sensor1.csv', sep = ';')
                    self.data = self.datatype_correction_csv(df)
                elif(wahl == 'Box2'):
                    clear_output(wait=True)
                    display(VBox([self.auswahl, self.loadButton]))
                    df = pd.read_csv('res/Sensor2.csv', sep = ';')
                    self.data = self.datatype_correction_csv(df)
                else:
                    clear_output(wait=True)
                    print("Fehlerhafte Eingabe")
                #boxID1 = input('BoxID eingeben: ')
                #url = 'https://api.opensensemap.org/boxes/' + boxID
                #headers = {'Content-type': 'application/json'}
                ##headers = {'Content-type': 'application/csv'}
                #url_meas = 'https://api.opensensemap.org/boxes/' + boxID + '/data/' + sensorID1 + '?&download=true&format=json'
                #measurements = requests.get(url_meas, headers = headers)
                #measurements.status_code
                #values = measurements.content
                #s=str(values,'utf-8')
                #data = StringIO(s) 
                #df=pd.read_json(data)
                #self.data = self.datatype_correction(df)
            


#        if(datei == "ggf. später mehr"):
#            print("Später kommen noch andere Datensätze. Wähle bitte einen anderen")
#        else:
#            if (datei == "Temperatur"):
#                self.data = pd.read_csv('Daten/temp.csv', parse_dates=['value'])
#            elif (datei == "Feinstaub"):
#                self.data = pd.read_csv('Daten/pm.csv', parse_dates=['value'])
#            elif (datei == "Luftfeuchtigkeit"):
#                self.data = pd.read_csv('Daten/hum.csv', parse_dates=['value'])
#            else:
#                print("Bitte gültigen Datensatz eingeben.")
#            self.data = self.datatype_correction(self.data)
#            print(datei + "-Daten wurden geladen")


    def buttonLoadData_onclick(self, b):
        Steuerung.ladeDatei(self, wahl = Steuerung.auswahl.value)

    def loadDataFrame(path: str):
        data = pd.read_csv(path)
        data = datatype_correction(data)
        if data.index.name != 'timestamp':
            df = df.set('timestamp')

    def datatype_correction(self, df):
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        if df.index.name != 'createdAt':
            df['createdAt'] = pd.to_datetime(df['createdAt'], dayfirst=True,errors='coerce')
            df['createdAt'] = df['createdAt'] + timedelta(hours=2)
            df = df.drop(['location'], axis = 1)
            df = df.set_index('createdAt')
        return df

    def datatype_correction_csv(self, df):
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        if df.index.name != 'createdAt':
            df['createdAt'] = pd.to_datetime(df['createdAt'], dayfirst=True,errors='coerce')
            df['createdAt'] = df['createdAt'] + timedelta(hours=2)
            df = df.set_index('createdAt')
        return df


