import json
import base64
from pathlib import Path

import os
import PySimpleGUI as sg

def validPath(filepath):
    if filepath and Path(filepath).exists():
        return True
    sg.popup_error("Specified filepath is incorrect :(")
    return False

layout = [
            [sg.Text("Cozy Grove Save Editor (WIP)")],
            [sg.Text("Created by callmepvp (pvp#7272)")],
            [sg.Text("File Location:"), sg.Input(key="-IN-"), sg.FileBrowse(file_types=[("Save Files", "*.sf"), ("Json Files", "*.json")])],
            [sg.Text("Output Location:"), sg.Input(key="-OUT-"), sg.FolderBrowse()],
            [sg.Button("Decode")], [sg.Button("Encode")]
]

#Window Creation
window = sg.Window("Save Editor", layout)

#Event Loop
while True:
    event, values = window.read()
    
    #Handle Events
    if event == "Decode":
        if validPath(values["-IN-"]) and validPath(values["-OUT-"]):

            inputFilePath = values["-IN-"]
            outputFilePath = values["-OUT-"]

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
            with open(f'{outputFilePath}/cg_save.json', 'w') as f:
                json.dump(json_str, f, indent=4)

            print('[DECODING SUCCESSFUL]')

    elif event == "Encode":
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

            print('[ENCODING SUCCESSFUL]')

    elif event == sg.WIN_CLOSED:
        break

window.close()



