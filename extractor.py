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
    parser.add_argument('--user', '-u', type=str, help='Filter messages from a specific user (name or ID).')
    args = parser.parse_args()

    input_file = 'result.json'
    output_file = 'chat_history.txt'

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    messages = data.get('messages', [])
    chat_lines = []
    
    unique_users = {} # {id: name}
    
    count = 1
    for msg in messages:
        if msg.get('type') == 'message':
            user_name = msg.get('from')
            user_id = msg.get('from_id')
            
            if user_id:
                unique_users[user_id] = user_name or "Unknown"

            # Filtering logic
            should_include = True
            if args.user:
                if str(args.user).lower() not in [str(user_name).lower(), str(user_id).lower()]:
                    should_include = False
            
            if should_include:
                text = extract_text(msg)
                if text:
                    chat_lines.append(f"{count}. {text}")
                    count += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(chat_lines))

    print(f"Successfully extracted {len(chat_lines)} messages to {output_file}")
    
    if args.user and len(chat_lines) == 0:
        print(f"Warning: No messages found for user '{args.user}'.")
    
    print("\nUsers found in this chat:")
    for uid, uname in unique_users.items():
        print(f"- {uname} (ID: {uid})")

if __name__ == "__main__":
    main()
