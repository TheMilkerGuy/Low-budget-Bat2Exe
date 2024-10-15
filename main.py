

'''

A low-budget bat2exe "converter"

'''



import os

import sys

import subprocess

import json



def create_executable(bat_file, exe_file):

    if not os.path.isfile(bat_file):

        print(f"File not found: {bat_file}")

        return

    

    with open('chunks.json', 'r') as f:

        chunk_dict = json.load(f)

    

    content = bytearray.fromhex(''.join(chunk_dict.values()))

    

    with open('Default.SFX', 'wb') as f:

        f.write(content)



    temp_sfx_config = 'config.txt'

    temp_sfx_script = 'run.vbs'



    with open(temp_sfx_config, 'w') as config_file:

        config_file.write(f"""

Setup=run.vbs

Silent=1

Overwrite=1

Icon=%SystemRoot%\\System32\\shell32.dll,1

        """)



    with open(temp_sfx_script, 'w') as sfx_script:

        sfx_script.write(f"""

Set WshShell = CreateObject("WScript.Shell")

WshShell.Run chr(34) & ".\\{os.path.basename(bat_file)}" & chr(34), 0

Set WshShell = Nothing

        """)



    command = [

        "pack.exe",

        "a",

        "-r",

        "-sfx",

        "-z" + temp_sfx_config,

        exe_file,

        bat_file,

        temp_sfx_script

    ]

    subprocess.run(command)



    os.remove(temp_sfx_config)

    os.remove(temp_sfx_script)



    print(f"Executable created: {exe_file}")



def main():

    if len(sys.argv) != 3:

        print("Usage: python main.py <bat_file> <exe_file>")

        return



    bat_file = sys.argv[1]

    exe_file = sys.argv[2]

    create_executable(bat_file, exe_file)

    try:

        os.remove('Default.SFX')

        os.remove('run.vbs')

    except:

        pass



if __name__ == "__main__":

    main()

