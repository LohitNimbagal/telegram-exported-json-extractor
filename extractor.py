import json
import os
import argparse

def extract_text(message):
    text_data = message.get('text', '')
    if isinstance(text_data, str):
        return text_data.strip()
    elif isinstance(text_data, list):
        parts = []
        for part in text_data:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict) and 'text' in part:
                parts.append(part['text'])
        return "".join(parts).strip()
    return ""

def main():
    parser = argparse.ArgumentParser(description='Extract text from Telegram JSON export.')
    parser.add_argument('--user', '-u', type=str, help='Filter messages from a specific user (name or ID). Bypass interactive selection.')
    args = parser.parse_args()

    input_file = 'result.json'
    output_file = 'chat_history.txt'

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print("Loading data...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    messages = data.get('messages', [])
    
    # Step 1: Get unique users
    unique_users = {} # {id: name}
    for msg in messages:
        if msg.get('type') == 'message':
            user_name = msg.get('from')
            user_id = msg.get('from_id')
            if user_id:
                unique_users[user_id] = user_name or "Unknown"

    target_user_id = None
    target_user_name = None

    # Step 2: Selection
    if args.user:
        # Search for ID or Name in our unique_users map
        found = False
        for uid, uname in unique_users.items():
            if str(args.user).lower() in [str(uname).lower(), str(uid).lower()]:
                target_user_id = uid
                target_user_name = uname
                found = True
                break
        if not found:
            print(f"Warning: User '{args.user}' not found in chat. Extracting nothing.")
            return
    else:
        print("\nParticipants found in this chat:")
        print("0. [Extract All Messages]")
        user_list = list(unique_users.items())
        for i, (uid, uname) in enumerate(user_list, 1):
            print(f"{i}. {uname} (ID: {uid})")
        
        try:
            choice = input(f"\nSelect a user number (0-{len(user_list)}): ").strip()
            if choice == '0' or choice == '':
                target_user_id = None
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(user_list):
                    target_user_id, target_user_name = user_list[idx]
                else:
                    print("Invalid selection. Extracting all.")
                    target_user_id = None
        except ValueError:
            print("Invalid input. Extracting all.")
            target_user_id = None

    # Step 3: Extract
    chat_lines = []
    count = 1
    for msg in messages:
        if msg.get('type') == 'message':
            user_id = msg.get('from_id')
            
            should_include = True
            if target_user_id and user_id != target_user_id:
                should_include = False
            
            if should_include:
                text = extract_text(msg)
                if text:
                    chat_lines.append(f"{count}. {text}")
                    count += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(chat_lines))

    print(f"\n--- SUCCESS ---")
    if target_user_id:
        print(f"Extracted {len(chat_lines)} messages from: {target_user_name}")
    else:
        print(f"Extracted {len(chat_lines)} messages from: Everyone")
    print(f"File saved to: {output_file}")

if __name__ == "__main__":
    main()
