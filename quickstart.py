import csv
import json
import os


def calculate_affinity(index, reserved_cores=2):
    """
    Handles processor groups for >64 cores
    Returns tuple: (group_number, affinity_mask_hex)
    """
    cores_per_group = 64
    group = index // (cores_per_group - reserved_cores)
    group_core = index % (cores_per_group - reserved_cores) + reserved_cores
    mask = 1 << group_core
    return (group, format(mask, 'x').upper())


def input_accounts(columns, delimiter='\t'):
    lines = []

    while True:
        try:
            line = input()
        except EOFError:
            break

        if not line:
            break

        lines.append(line)

    return [dict(zip(columns, line.split('\t'))) for line in lines]


def arguments_to_string(args_dict):
    return ' '.join([f'-{key} {value}' if value is not None else f'-{key}' for key, value in args_dict.items()])


def generate_quickstart(account: dict):
    quick_start = {
        "account": f"{account['Username']}",
        "proxy": f"{account['Proxy'] if account['Proxy'] != '' else None}",
        "world": "f2p",
        "flags": ["-covert", "-fresh"],
        "layout": "resizable_modern",
        "fps": f"{account['FPS'] if account['Proxy'] != '' else None}",
        "script": f"{account['Script']}"
    }

    if account.get("Params", None) is not None:
        quick_start["params"] = [account['Params']]

    if account.get("Breaks", None) is not None:
        quick_start["breaks"] = f"{account['Breaks']}"

    return quick_start


template = """
@echo off
set "DREAMBOT_JAR=%USERPROFILE%\\DreamBot\\BotData\\client.jar"

rem PowerShell command for cross-group affinity
powershell -Command "$p = Start-Process javaw -ArgumentList '-Xms512M -Xmx512M -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -XX:+UseNUMA -server -jar \"%DREAMBOT_JAR%\" -json \"{quick_start_file_path}\"' -PassThru -WindowStyle Hidden; $p.ProcessorAffinity = {affinity}; $p.ProcessorGroup = {group}"
"""

cwd = os.getcwd()
print(f"Current working directory: {cwd}")

print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
accounts = input_accounts(
    [
        "System", "Method", "Status",
        "Banned", "Username", "E-mail",
        "Password", "TOTP secret", "Proxy",
        "Previous Proxy", "Script", "Params",
        "Breaks", "FPS"
    ]
)

for index, account in enumerate(accounts):
    print(account)

    nickname_normalized = account["Username"].replace(" ", "_")
    quick_start_file_path = os.path.join(cwd, "output", "quick_start", f"{nickname_normalized}.json")
    batch_file_path = os.path.join(cwd, "output", f"{index}_{nickname_normalized}.bat")

    os.makedirs(os.path.dirname(quick_start_file_path), exist_ok=True)
    os.makedirs(os.path.dirname(batch_file_path), exist_ok=True)

    quick_start = generate_quickstart(account)
    group_number, affinity_mask = calculate_affinity(index)

    batch_file_contents = template.format(
        quick_start_file_path=quick_start_file_path,
        affinity=affinity_mask,
        group=group_number
    )

    with open(quick_start_file_path, "w") as quick_start_file:
        json.dump(quick_start, quick_start_file)

    with open(batch_file_path, "w") as batch_file:
        batch_file.write(batch_file_contents)
