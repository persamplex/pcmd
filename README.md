# README for Doskey Alias Manager

## Overview
The **Doskey Alias Manager** is a Python script designed to simplify the management of command aliases in the Windows Command Prompt (CMD). This tool allows users to create, update, and remove doskey aliases easily, as well as automatically configure their system to run a batch file on CMD startup.

## Features
- **Add new aliases**: Create new doskey commands with ease.
- **List existing commands**: View all current doskey aliases and their corresponding commands.
- **Remove commands**: Delete specific doskey aliases by their index.
- **Automatic setup**: Automatically sets up a batch file to run doskey commands when CMD is opened.
- **Registry integration**: Updates the Windows Registry to ensure that specified batch files run on startup.

## Requirements
- Python 3.x
- Windows operating system

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/doskey-alias-manager.git
   cd doskey-alias-manager
   ```

2. Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

3. Run the script:
   ```bash
   python doskey_alias_manager.py
   ```

## Usage
You can manage your doskey aliases using command-line arguments:

### Commands
- **Set a new alias**:
  ```bash
  python doskey_alias_manager.py --set "alias=command"
  ```
  Example:
  ```bash
  python doskey_alias_manager.py --set "myip=curl https://api.ipify.org"
  ```

- **Show version**:
  ```bash
  python doskey_alias_manager.py --version
  ```

- **Print all aliases**:
  ```bash
  python doskey_alias_manager.py --print
  ```

- **Remove an alias by index**:
  ```bash
  python doskey_alias_manager.py --remove <index>
  ```
  Example:
  ```bash
  python doskey_alias_manager.py --remove 1
  ```

- **Install the pcmd alias** (copies the script to the doskey folder):
  ```bash
  python doskey_alias_manager.py --install
  ```

### Example Output
When you print all commands, you will see output similar to this:
```
num | doskey         | command
----------------------------------------
1   | myip          | curl https://api.ipify.org
```

## Notes
- This script only works on Windows systems.
- Ensure that you run the script with appropriate permissions to modify the registry.

## Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
