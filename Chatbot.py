import tkinter as tk          # GUI library
from tkinter import scrolledtext  # Scrollable text widget
from datetime import datetime  # For timestamps, time, and date

#  SECTION 1 : RULE-BASED RESPONSE ENGINE

def get_bot_response(user_input):
    """
    Core rule engine of the chatbot.
    
    Accepts the user's message (string), converts it to
    lowercase for case-insensitive matching, then returns
    the appropriate bot reply using if-elif rules.
    
    Parameters:
        user_input (str): The message typed by the user.
    
    Returns:
        str: The chatbot's response.
    """

    # Convert to lowercase
    message = user_input.lower().strip()

    # ── Greetings ──────────────────────────────────────────
    if message in ["hello", "hi", "hey", "hii", "helo"]:
        return "👋 Hello there! I'm SmartBot. How can I help you today?\nType 'help' to see what I can do!"

    # ── How are you ────────────────────────────────────────
    elif "how are you" in message:
        return "😊 I'm doing great, thanks for asking!\nHow about you? Ready to chat?"

    # ── Bot's name ─────────────────────────────────────────
    elif "your name" in message or "who are you" in message:
        return "🤖 I'm SmartBot — a simple rule-based chatbot\nbuilt with Python & Tkinter. Nice to meet you!"

    # ── Help / Commands list ───────────────────────────────
    elif message == "help":
        return (
            "📋 Here are the commands I understand:\n"
            "  • hello / hi / hey  → Greeting\n"
            "  • how are you       → My status\n"
            "  • what is your name → My introduction\n"
            "  • time              → Current time\n"
            "  • date              → Today's date\n"
            "  • thanks            → You're welcome 😊\n"
            "  • bye               → Exit greeting\n"
            "  • clear             → Clear the chat"
        )

    # ── Current Time ───────────────────────────────────────
    elif message == "time":
        current_time = datetime.now().strftime("%I:%M %p")   # e.g. 03:45 PM
        return f"⏰ The current time is: {current_time}"

    # ── Current Date ───────────────────────────────────────
    elif message == "date":
        current_date = datetime.now().strftime("%A, %d %B %Y")  # e.g. Tuesday, 03 June 2025
        return f"📅 Today's date is: {current_date}"

    # ── Thanks ─────────────────────────────────────────────
    elif message in ["thanks", "thank you", "thankyou", "thx", "ty"]:
        return "😊 You're most welcome! Happy to help anytime."

    # ── Goodbye ────────────────────────────────────────────
    elif message in ["bye", "goodbye", "see you", "exit", "quit"]:
        return "👋 Goodbye! It was nice chatting with you.\nHave a wonderful day! 🌟"

    # ── Clear command (handled in send_message, but respond anyway) ──
    elif message == "clear":
        return "🧹 Chat cleared! Fresh start 😊"

    # ── Unknown input ──────────────────────────────────────
    else:
        return (
            "🤔 Sorry, I don't understand that.\n"
            "Type 'help' to see the list of commands I support."
        )

#  SECTION 2 : GUI HELPER FUNCTIONS

def get_timestamp():
    """Returns the current time as a short string, e.g. [03:45 PM]"""
    return datetime.now().strftime("[%I:%M %p]")


def display_message(sender, message, tag):
    """
    Inserts a formatted message into the chat display area.

    Parameters:
        sender  (str): "You" or "SmartBot"
        message (str): The text to display
        tag     (str): "user" or "bot" — controls text color via tags
    """
    # Allow writing to the text widget temporarily
    chat_area.config(state=tk.NORMAL)

    # Insert the timestamp line in grey
    chat_area.insert(tk.END, f"\n  {get_timestamp()}\n", "timestamp")

    # Insert the sender label + message with color based on tag
    chat_area.insert(tk.END, f"  {sender}:\n  {message}\n", tag)

    # Add a separator line
    chat_area.insert(tk.END, "  " + "─" * 45 + "\n", "separator")

    # Lock the text area again so users can't edit it
    chat_area.config(state=tk.DISABLED)

    # Auto-scroll to the latest message
    chat_area.yview(tk.END)


def send_message(event=None):
    """
    Triggered when the user clicks 'Send' or presses Enter.
    
    Reads the input field, validates it, gets a bot response,
    and displays both messages in the chat area.

    Parameter:
        event: Keyboard event (used when Enter key is pressed).
               Default is None for button click.
    """
    # Get the text from the input field and strip extra spaces
    user_text = input_field.get().strip()

    # Do nothing if the field is empty
    if not user_text:
        return

    # Clear the input field after reading
    input_field.delete(0, tk.END)

    # If user types "clear", wipe the chat
    if user_text.lower() == "clear":
        clear_chat()
        return

    # Display the user's message in the chat
    display_message("You", user_text, "user")

    # Get the bot's response using the rule engine
    bot_reply = get_bot_response(user_text)

    # Display the bot's response in the chat
    display_message("SmartBot 🤖", bot_reply, "bot")


def clear_chat():
    """
    Clears all messages from the chat display area
    and shows a fresh welcome message.
    """
    # Enable editing, clear everything, then disable again
    chat_area.config(state=tk.NORMAL)
    chat_area.delete(1.0, tk.END)
    chat_area.config(state=tk.DISABLED)

    # Show welcome message again after clearing
    show_welcome_message()


def show_welcome_message():
    """
    Displays a welcome banner when the app starts
    (or after the chat is cleared).
    """
    welcome_text = (
        "┌──────────────────────────────────────────┐\n"
        "│        Welcome to SmartBot🤖             │\n"
        "│ A Rule-Based Chatbot built with Python   │\n"
        "│ Type 'help' to see available commands    │\n"
        "└──────────────────────────────────────────┘"
    )
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, welcome_text + "\n", "welcome")
    chat_area.config(state=tk.DISABLED)

#  SECTION 3 : TKINTER GUI SETUP

# ── Create the main window ────────────────────
root = tk.Tk()
root.title("SmartBot — Rule-Based Chatbot")
root.geometry("620x650")          # Width x Height
root.resizable(True, True)        # Allow resizing
root.configure(bg="#1a1a2e")      # Dark navy background

# ── Color palette (dark theme) ────────────────
COLOR_BG          = "#1a1a2e"   # Main background
COLOR_CHAT_BG     = "#16213e"   # Chat area background
COLOR_INPUT_BG    = "#0f3460"   # Input field background
COLOR_BUTTON_SEND = "#e94560"   # Send button (accent red)
COLOR_BUTTON_CLR  = "#533483"   # Clear button (purple)
COLOR_TEXT_USER   = "#00d4ff"   # User message color (cyan)
COLOR_TEXT_BOT    = "#a8ff78"   # Bot message color (green)
COLOR_TIMESTAMP   = "#888888"   # Timestamp color (grey)
COLOR_SEPARATOR   = "#333355"   # Separator line color
COLOR_WELCOME     = "#f5a623"   # Welcome message (orange)
COLOR_WHITE       = "#e0e0e0"   # General white text

# ── Font definitions ──────────────────────────
FONT_CHAT    = ("Consolas", 10)
FONT_INPUT   = ("Segoe UI", 11)
FONT_BUTTON  = ("Segoe UI", 10, "bold")
FONT_TITLE   = ("Segoe UI", 12, "bold")

#  SECTION 4 : LAYOUT WIDGETS

# ── Title label at the top ────────────────────
title_label = tk.Label(
    root,
    text="🤖  SmartBot — Rule-Based Chatbot",
    font=FONT_TITLE,
    bg=COLOR_BG,
    fg=COLOR_WELCOME,
    pady=10
)
title_label.pack(fill=tk.X)

# ── Chat display area (ScrolledText) ─────────
# ScrolledText = Text widget + built-in vertical scrollbar
chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,           # Wrap long lines at word boundaries
    state=tk.DISABLED,      # Read-only; users cannot type here
    font=FONT_CHAT,
    bg=COLOR_CHAT_BG,
    fg=COLOR_WHITE,
    insertbackground=COLOR_WHITE,
    bd=0,                   # No border
    padx=10,
    pady=10,
    height=28
)
chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))

# ── Color tags for different message types ─────
# These tags control the text color per message type
chat_area.tag_config("user",      foreground=COLOR_TEXT_USER)
chat_area.tag_config("bot",       foreground=COLOR_TEXT_BOT)
chat_area.tag_config("timestamp", foreground=COLOR_TIMESTAMP)
chat_area.tag_config("separator", foreground=COLOR_SEPARATOR)
chat_area.tag_config("welcome",   foreground=COLOR_WELCOME)

# ── Bottom frame for input + buttons ──────────
bottom_frame = tk.Frame(root, bg=COLOR_BG, pady=8)
bottom_frame.pack(fill=tk.X, padx=10)

# ── Text input field ──────────────────────────
input_field = tk.Entry(
    bottom_frame,
    font=FONT_INPUT,
    bg=COLOR_INPUT_BG,
    fg=COLOR_WHITE,
    insertbackground=COLOR_WHITE,   # Cursor color
    relief=tk.FLAT,
    bd=5
)
input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
input_field.focus()   # Auto-focus so user can type immediately

# ── Send button ───────────────────────────────
send_button = tk.Button(
    bottom_frame,
    text="Send ➤",
    font=FONT_BUTTON,
    bg=COLOR_BUTTON_SEND,
    fg=COLOR_WHITE,
    activebackground="#c73652",
    activeforeground=COLOR_WHITE,
    relief=tk.FLAT,
    padx=14,
    pady=6,
    cursor="hand2",         # Pointer cursor on hover
    command=send_message    # Call send_message on click
)
send_button.pack(side=tk.LEFT, padx=(8, 4))

# ── Clear Chat button ─────────────────────────
clear_button = tk.Button(
    bottom_frame,
    text="🗑 Clear",
    font=FONT_BUTTON,
    bg=COLOR_BUTTON_CLR,
    fg=COLOR_WHITE,
    activebackground="#3d2466",
    activeforeground=COLOR_WHITE,
    relief=tk.FLAT,
    padx=10,
    pady=6,
    cursor="hand2",
    command=clear_chat      # Call clear_chat on click
)
clear_button.pack(side=tk.LEFT, padx=(0, 4))

# ── Hint label at the bottom ──────────────────
hint_label = tk.Label(
    root,
    text="Press Enter or click Send to chat  •  Type 'help' for commands",
    font=("Segoe UI", 8),
    bg=COLOR_BG,
    fg=COLOR_TIMESTAMP
)
hint_label.pack(pady=(0, 6))

#  SECTION 5 : KEY BINDING & STARTUP

# This way pressing Enter = clicking Send button
root.bind("<Return>", send_message)

# Show the welcome message when the app first opens
show_welcome_message()

# ── Start the Tkinter event loop ──────────────
# This keeps the window open and responsive to user actions
root.mainloop()
#  END OF PROJECT
