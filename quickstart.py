import csv
import json
import os


def calculate_affinity(index, total_cores=80, reserved_cores=2, cores_per_process=1):
    """
    Calculates CPU affinity mask for each process
    Reserved cores: 0-3 (for OS/UI)
    Returns hex string without 0x prefix
    """
    usable_cores = total_cores - reserved_cores
    max_groups = usable_cores // cores_per_process
    group = index % max_groups
    start_core = reserved_cores + (group * cores_per_process)
    mask = ((1 << cores_per_process) - 1) << start_core
    return format(mask, 'x').upper()


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
        "fps": "10",
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
start "" /B /LOW /AFFINITY {affinity} javaw -Xms{allocate_ram} -Xmx{allocate_ram} \
-XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 \
-XX:+UseNUMA -server -Djava.awt.headless=true -jar "%DREAMBOT_JAR%" \
-json "{quick_start_file_path}" >nul 2>&1
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
        "Breaks"
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
    affinity_mask = calculate_affinity(index)
    batch_file_contents = template.format(
        allocate_ram="512M",
        quick_start_file_path=quick_start_file_path,
        affinity=affinity_mask
    )

    with open(quick_start_file_path, "w") as quick_start_file:
        json.dump(quick_start, quick_start_file)

    with open(batch_file_path, "w") as batch_file:
        batch_file.write(batch_file_contents)
