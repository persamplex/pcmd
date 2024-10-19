import os
import json
import sys
import argparse
import shutil
import winreg as reg
import shlex

def check_windows():
    if os.name != 'nt':
        print("This script only works on Windows.")
        sys.exit(1)

def set_registry(bat_file_path):
    registry_key = r"Software\Microsoft\Command Processor"
    value_name = "AutoRun"

    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, registry_key, 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, value_name, 0, reg.REG_SZ, bat_file_path)
            print("Registry updated to run the batch file on CMD open.")
    except Exception as e:
        print(f"Failed to update registry: {e}")

def setup_doskey():
    user_docs_path = os.path.expanduser(r"~\Documents")
    doskey_folder = os.path.join(user_docs_path, 'doskey')
    doskey_file = os.path.join(doskey_folder, 'doskey.json')

    if not os.path.exists(doskey_folder):
        os.makedirs(doskey_folder)

    if not os.path.exists(doskey_file):
        with open(doskey_file, 'w') as f:
            json.dump([], f)

    return doskey_file

def add_alias_to_registry(command, script_path):
    reg_key_path = r'Software\Microsoft\Command Processor'
    try:
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, reg_key_path, 0, reg.KEY_SET_VALUE)
        command_value = f'DOSKEY {command}="{script_path}" $*'
        reg.SetValueEx(reg_key, 'AutoRun', 0, reg.REG_SZ, command_value)
        print(f"Alias '{command}' added to CMD.")
        reg.CloseKey(reg_key)
    except Exception as e:
        print(f"Error adding alias to registry: {e}")

def update_doskey_file(doskey_file, data):
    with open(doskey_file, 'r+') as f:
        current_data = json.load(f)

        for entry in current_data:
            if entry['alias'] == data['alias'] and entry['command'] == data['command']:
                print(f"Duplicate entry found: {data}. Not adding.")
                return

        current_data.append(data)
        f.seek(0)
        f.truncate()
        json.dump(current_data, f, indent=4)

def read_doskey_file(doskey_file):
    with open(doskey_file, 'r') as f:
        return json.load(f)

def remove_command(doskey_file, index):
    with open(doskey_file, 'r+') as f:
        current_data = json.load(f)
        if 0 <= index < len(current_data):
            current_data.pop(index)
            f.seek(0)
            f.truncate()
            json.dump(current_data, f, indent=4)
        else:
            print("Index out of range.")

def create_batch_file(doskey_file):
    batch_file_path = os.path.join(os.path.expanduser(r"~\Documents\doskey"), 'doskey_commands.bat')
    commands = read_doskey_file(doskey_file)

    with open(batch_file_path, 'w') as batch_file:
        for i, command in enumerate(commands):
            batch_file.write(f'doskey {command["alias"]}={command["command"]}\n')
        batch_file.write(f'cls\n')
    return batch_file_path


def main():
    check_windows()
    doskey_file = setup_doskey()

    parser = argparse.ArgumentParser(description='Manage doskey aliases.')
    parser.add_argument('--set','-s', type=str, help='Set a new doskey command (e.g., "myip=curl https://api.ipify.org")')
    parser.add_argument('--version', '-v', action='store_true', help='Show the version of the script.')
    parser.add_argument('--print','-pr','-ls', action='store_true', help='Print all doskey commands')
    parser.add_argument('--remove','-rm', type=int, help='Remove a doskey command by its number')
    parser.add_argument('--install','-i', action='store_true', help='Install the pcmd alias')

    args = parser.parse_args()

    if args.set:
        print(args.set)
        try:
            alias_part, command_part = args.set.split('=', 1)
            alias = alias_part.strip()
            command = shlex.split(command_part.strip(), posix=False)
            data = {"alias": alias, "command": ' '.join(command)}
            update_doskey_file(doskey_file, data)
            print(f'Added: {data}')
        except ValueError:
            print("Error: Please provide a valid input in the format 'alias=command'.")
    
    elif args.version:
        print("Script version: 1.0.1")
    
    elif args.print:
        commands = read_doskey_file(doskey_file)
        print(f'{"num":<5} | {"doskey":<15} | {"command"}')
        print('-' * 40)
        for i, cmd in enumerate(commands):
            print(f'{i+1:<5} | {cmd["alias"]:<15} | {cmd["command"]}')

    elif args.remove is not None:
        remove_command(doskey_file, args.remove - 1)
        print(f'Removed command at index {args.remove}')

    elif args.install:
        user_docs_path = os.path.expanduser(r"~\Documents")
        doskey_folder = os.path.join(user_docs_path, 'doskey')
        script_path = os.path.abspath(__file__)
        shutil.copy(script_path, doskey_folder) 

        pcmd_command = {"alias": "pcmd", "command": f'{sys.executable} "{os.path.join(doskey_folder, os.path.basename(script_path))}" $*'}
        update_doskey_file(doskey_file, pcmd_command)
        pc_command = {"alias": "pc", "command": f'{sys.executable} "{os.path.join(doskey_folder, os.path.basename(script_path))}" $*'}
        update_doskey_file(doskey_file, pc_command)
        
        set_registry(create_batch_file(doskey_file))
        print('Installed the pcmd alias.')
    else:
        print('pcmd is running')
    
    update = create_batch_file(doskey_file)
    sys.exit()

if __name__ == '__main__':
    main()


