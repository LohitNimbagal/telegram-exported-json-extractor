# Telegram Exported JSON Extractor

A simple Python utility to extract message text from Telegram chat history exported in JSON format.

## Features

- Extracts text from both simple text messages and complex formatted messages.
- Numbers each message in the output.
- Filters messages by user (name or ID).
- Lists all users found in the chat export.

## Prerequisites

- Python 3.x

## Usage

1. **Option A: Real Data**
   - Export your Telegram chat in **JSON** format from Telegram Desktop.
   - Rename the file to `result.json` and place it in this directory.

2. **Option B: Try the Example**
   - If you don't have a `result.json` yet, the provided `run_extractor.bat` will automatically use `example_result.json` to show you how it works.

3. **Run the Extractor**:
   - Double-click **`run_extractor.bat`** (Windows).
   - The script will now guide you through two steps:
     - **Step 1**: It lists all participants found in the chat.
     - **Step 2**: You select a user by number (or `0` for everyone) to extract their messages.

4. **Advanced: Bypass Selection**:
   - run manually via command line to skip the interactive prompt:
     ```bash
     python extractor.py --user "User Name"
     ```

## Output

The extracted text is saved to `chat_history.txt`.
