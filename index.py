import json
import base64
from json import loads
from pathlib import Path


import os
import PySimpleGUI as sg

sg.theme('DarkGrey4')
layout_frame2 = []
layout = [
    [sg.Text("Cozy Grove Save Editor (WIP)")],
    [sg.Text("Created by callmepvp (pvp#7272)")],
    [sg.FileBrowse(file_types=[("Save Files", "*.sf")]), sg.Input(key="-IN-")], [sg.Button("Open Save")]]

def validPath(filepath):
    if filepath and Path(filepath).exists():
        return True
    sg.popup_error("Specified filepath is incorrect :(")
    return False

#Window Creation
window = sg.Window("Save Editor", layout, margins=(2, 2), resizable = True)

#Event Loop
while True:
    event, values = window.read()
    
    #Handle Events
    if event == "Open Save":
        if validPath(values["-IN-"]):
            Data = [
                [sg.Frame("Edit Your Save File Data:", layout_frame2, visible = False, key="-FRAME-", size=(500, 500), expand_x=True, expand_y=True, title_location=sg.TITLE_LOCATION_TOP, border_width = 0)]
            ]
            window.extend_layout(window, Data)
            window["-FRAME-"].update('')

            inputFilePath = values["-IN-"]
            #outputFilePath = values["-OUT-"]

            #Convert the .sf into a .txt for easier manipulation
            with open(inputFilePath, "r") as dataFile:
                dataList = dataFile.readlines()

            Text = ""
            for items in dataList:
                Text = Text + items +"\n"

            Text = Text[4:] #Remove the decryption block

            #Format File
            decodedBytes = base64.b64decode(Text)
            decodedStr = decodedBytes.decode("ascii") 
            json_str=json.loads(decodedStr)

            #Output Formatted File
            with open('data/cg_save.json', 'w') as f:
                json.dump(json_str, f, indent=4)

            print('[DECODING SUCCESSFUL]')

            #Open The Data Manipulation Window
            data = loads(Path("data/cg_save.json").read_text())

            #Add All Changeable Data
            window.refresh()
            window['-FRAME-'].update(visible = True)

            Texts = [
                [sg.Text("Inventory:")]
            ]

            for i in data["Player"]["Inventory"]["SlotDisplayOrder"]:
                if i != None:
                    Texts.append([sg.Text(f'{i["item"]["configID"]}')])

            window.extend_layout(window['-FRAME-'], Texts)

        """elif event == "Encode":
        if validPath(values["-IN-"]) and validPath(values["-OUT-"]):

            inputFilePath = values["-IN-"]
            outputFilePath = values["-OUT-"]

            with open(inputFilePath, "r") as dataFile:
                data = json.load(dataFile)
                Text = json.dumps(data)

                #Format File
                encodedBytes = base64.b64encode(Text.encode('utf-8'))

            #Output Formatted File
            with open(f'{outputFilePath}/cg_save.sf', 'wb') as f:
                f.write(b'60z,') #Adds the decryption block
                f.write(encodedBytes)

            print('[ENCODING SUCCESSFUL]')"""

    elif event == sg.WIN_CLOSED:
        break

window.close()



