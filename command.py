import os
from openai import OpenAI
from config import OPENAI_API_KEY

FILES_DIR = "./files"
client = OpenAI(api_key=OPENAI_API_KEY)

# Runtime state
pending_filename = None
pending_action = None
awaiting_followup = False

# ========== GPT Interface ==========

def gpt_to_command(user_input):
    system_prompt = """You are an assistant that maps natural language to structured system commands.
Valid formats:
- read file <filename>
- write file <filename> <content>
- create file <filename>
- add file <filename> <content>
- append file <filename> <content>
- delete file <filename>
- list files
- gpt <prompt>

If the user hasn’t provided content yet, use <content> as a placeholder.
Only return a command — no extra words, formatting, or punctuation.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

def gpt_parse_content(raw_input):
    system_prompt = "You are a helpful assistant. Clean up and return the user’s spoken message as clean content. Respond only with the content — no explanation, no formatting."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_input}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

# ========== Public Entry ==========

def process_command_flow(input_text):
    global pending_filename, pending_action, awaiting_followup

    input_text = input_text.strip()

    if awaiting_followup:
        awaiting_followup = False
        cleaned_content = gpt_parse_content(input_text)
        full_command = f"{pending_action} file {pending_filename} {cleaned_content}"
        reset_state()
        return handle_command(full_command)

    # Initial GPT parse
    parsed = gpt_to_command(input_text)
    parts = parsed.split()

    if len(parts) >= 3 and parts[0] in ["write", "add", "append"] and "<content>" in parsed:
        pending_action = parts[0]
        pending_filename = parts[2]
        awaiting_followup = True
        return f"📝 {pending_action.capitalize()} to {pending_filename}. What should I add?"

    return handle_command(parsed)

def reset_state():
    global pending_filename, pending_action, awaiting_followup
    pending_filename = None
    pending_action = None
    awaiting_followup = False

# ========== Core Command Execution ==========

def handle_command(text):
    parts = text.strip().split()
    cmd = parts[0].lower()

    if cmd == "read" and parts[1] == "file":
        return read_file(parts[2])
    elif cmd == "write" and parts[1] == "file":
        return write_file(parts[2], " ".join(parts[3:]))
    elif cmd == "create" and parts[1] == "file":
        return create_file(parts[2])
    elif cmd == "add" and parts[1] == "file":
        return add_file(parts[2], " ".join(parts[3:]))
    elif cmd == "append" and parts[1] == "file":
        return append_file(parts[2], " ".join(parts[3:]))
    elif cmd == "delete" and parts[1] == "file":
        return delete_file(parts[2])
    elif cmd == "list" and parts[1] == "files":
        return list_files()
    elif cmd == "gpt":
        return f"🧠 GPT: {' '.join(parts[1:])}"
    else:
        return f"❌ Unknown command: {text}"

# ========== File System Commands ==========

def read_file(filename):
    path = os.path.join(FILES_DIR, auto_txt(filename))
    try:
        with open(path, "r") as f:
            return f"📄 {filename}:\n" + f.read()
    except FileNotFoundError:
        return f"❌ File '{filename}' not found."

def write_file(filename, content):
    path = os.path.join(FILES_DIR, auto_txt(filename))
    with open(path, "w") as f:
        f.write(content)
    return f"✅ Wrote to '{filename}'"

def create_file(filename):
    path = os.path.join(FILES_DIR, auto_txt(filename))
    if os.path.exists(path):
        return f"⚠️ File '{filename}' already exists."
    with open(path, "w") as f:
        pass
    return f"✅ Created file '{filename}'"

def add_file(filename, content):
    path = os.path.join(FILES_DIR, auto_txt(filename))
    with open(path, "w") as f:
        f.write(content)
    return f"✅ Created and added content to '{filename}'"

def append_file(filename, content):
    path = os.path.join(FILES_DIR, auto_txt(filename))
    with open(path, "a") as f:
        f.write(content + "\n")
    return f"➕ Appended to '{filename}'"

def delete_file(filename):
    path = os.path.join(FILES_DIR, auto_txt(filename))
    if os.path.exists(path):
        os.remove(path)
        return f"🗑️ Deleted file '{filename}'"
    return f"❌ File '{filename}' not found."

def list_files():
    try:
        files = os.listdir(FILES_DIR)
        if not files:
            return "📂 No files found."
        return "📂 Files:\n" + "\n".join(files)
    except Exception as e:
        return f"⚠️ Error listing files: {e}"

def auto_txt(filename):
    path = os.path.join(FILES_DIR, filename)
    
    # Case 1: Exact file exists
    if os.path.exists(path):
        return filename

    # Case 2: Add .txt if missing and try again
    if not filename.endswith(".txt"):
        path_with_txt = os.path.join(FILES_DIR, filename + ".txt")
        if os.path.exists(path_with_txt):
            return filename + ".txt"
    
    # Default fallback: use .txt if not present
    return filename if filename.endswith(".txt") else filename + ".txt"
def is_awaiting_followup():
    return awaiting_followup