import streamlit as st
import time
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
import html

# Set page configuration
st.set_page_config(page_title="Vancouver Live Chat", page_icon="💬", layout="centered")

# Define styling for light and dark mode
LIGHT_MODE_CSS = """
    body {
        background-color: #f0f2f6;
    }
    .main {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: #333333;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        background-color: #e8ebf0;
        border-radius: 10px;
        border: 1px solid #ccc;
    }
    .message {
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 10px;
        background-color: #f0f2f6;
        transition: background-color 0.3s ease;
    }
    .own-message {
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 10px;
        background-color: #d1f7c4;
        transition: background-color 0.3s ease;
    }
    .message:hover, .own-message:hover {
        background-color: #dfe3e8;
    }
    .timestamp {
        font-size: 0.8em;
        color: #666;
    }
    .chat-box {
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    input[type=text] {
        border-radius: 10px;
        padding: 10px;
        width: 100%;
        border: 1px solid #ccc;
        transition: all 0.3s ease;
    }
    input[type=text]:focus {
        border-color: #007BFF;
        box-shadow: 0 0 10px rgba(0, 123, 255, 0.2);
    }
    .send-button {
        background-color: #007BFF;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .send-button:hover {
        background-color: #0056b3;
    }
"""

DARK_MODE_CSS = """
    body {
        background-color: #121212;
    }
    .main {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 10px;
    }
    h1, h2, h3, h4, h5, p, label {
        color: #ffffff;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        background-color: #333;
        border-radius: 10px;
        border: 1px solid #555;
    }
    .message {
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 10px;
        background-color: #444;
        transition: background-color 0.3s ease;
    }
    .own-message {
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 10px;
        background-color: #006400;
        transition: background-color 0.3s ease;
    }
    .message:hover, .own-message:hover {
        background-color: #555;
    }
    .timestamp {
        font-size: 0.8em;
        color: #888;
    }
    .chat-box {
        background-color: #222;
        border: 1px solid #555;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    input[type=text] {
        border-radius: 10px;
        padding: 10px;
        width: 100%;
        border: 1px solid #666;
        transition: all 0.3s ease;
    }
    input[type=text]:focus {
        border-color: #00aaff;
        box-shadow: 0 0 10px rgba(0, 170, 255, 0.5);
    }
    .send-button {
        background-color: #00aaff;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .send-button:hover {
        background-color: #0088cc;
    }
"""

# Choose between light and dark mode
mode = st.sidebar.radio("Choose theme:", ["Light Mode", "Dark Mode"])

# Apply CSS based on the selected mode
if mode == "Dark Mode":
    st.markdown(f"<style>{DARK_MODE_CSS}</style>", unsafe_allow_html=True)
else:
    st.markdown(f"<style>{LIGHT_MODE_CSS}</style>", unsafe_allow_html=True)

# Store messages, usernames, and user points in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "points" not in st.session_state:
    st.session_state["points"] = {}

# Ask for username
username = st.sidebar.text_input("Enter your username", "Anonymous")

# Initialize user's points if not already in the system
if username not in st.session_state["points"]:
    st.session_state["points"][username] = 0

# Function to remove messages older than 5 minutes
def remove_old_messages():
    current_time = datetime.now()
    st.session_state["messages"] = [msg for msg in st.session_state["messages"] if msg['timestamp'] > current_time - timedelta(minutes=5)]

# Function to sanitize user input before injecting into HTML
def sanitize_input(user_input):
    return html.escape(user_input)

# Function to display messages and points
def display_chat():
    chat_display = st.empty()  # For dynamically updating chat content
    chat_history = "<div class='chat-container'>"  # Add a scrollable container
    
    for message in st.session_state["messages"]:
        timestamp = message['timestamp'].strftime('%H:%M:%S')
        if message['user'] == username:
            chat_history += f"<div class='own-message'><span class='timestamp'>{timestamp}</span><br><strong>{message['user']}:</strong> {message['message']}</div>"
        else:
            chat_history += f"<div class='message'><span class='timestamp'>{timestamp}</span><br><strong>{message['user']}:</strong> {message['message']}</div>"
    
    chat_history += "</div>"
    chat_display.markdown(chat_history, unsafe_allow_html=True)

# Display Chat Header and Points
st.title("Vancouver Live Chat 💬")
st.write(f"Messages will disappear after 5 minutes for a real-time chatting experience.")

# Display current points
st.sidebar.subheader(f"Your Points: {st.session_state['points'][username]} Points")

# Remove expired messages before displaying chat
remove_old_messages()

# Display chat messages
display_chat()

# Input for new message with a text box and styled button
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
user_input = st.text_input("Type your message here... (Supports emojis 😊)", key="input_box")

# Send message when "Send" button is pressed and clear the input field
if st.button("Send", key="send_button", help="Click to send your message", args=("btn",)):
    if user_input.strip():
        sanitized_message = sanitize_input(user_input)  # Sanitize input
        st.session_state["messages"].append({
            "user": username,
            "message": sanitized_message,
            "timestamp": datetime.now()
        })
        
        # Award points for sending a message
        st.session_state["points"][username] += 10  # Gain 10 points for each message
        
        # Clear the input box after sending the message
        st.session_state["input_box"] = ""

# Footer section
st.sidebar.write("Built with ❤️ using Streamlit")
st.sidebar.markdown("[Learn more about Vancouver](https://vancouver.ca)")

# Auto-refresh every 10 seconds, using a unique key
st_autorefresh(interval=500, key=f"auto_refresh_{username}_{int(time.time())}")
