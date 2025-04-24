def read_accounts(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split(':')
            if len(parts) < 3:
                continue

            username = parts[0]
            email = parts[1]
            password = parts[2]

            yield {
                'username': username,
                'email': email,
                'password': password
            }

print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
emails = []

while True:
    try:
        line = input()
    except EOFError:
        break

    if not line:
        break

    emails.append(line)

file_path = "accounts.txt"
accounts = list(read_accounts(file_path))

print("Accounts:")
for account in accounts:
    print(account['email'])

print("Usernames:")
for email in emails:
    account = next((a for a in accounts if email.strip().lower() in a['email'].strip().lower()), None)
    if account is not None:
        print(account['username'])
    else:
        print("unknown")

