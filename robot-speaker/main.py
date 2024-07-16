import customtkinter as ctk
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to handle speaking the entered text
def speak_text():
    text = entry_text.get()
    if text.lower() == 'q':
        root.quit()
    else:
        engine.say(text)
        engine.runAndWait()

# Function to handle exiting the application
def quit_app():
    root.quit()

# Create the main window
root = ctk.CTk()
root.title("RobotSpeaker")
root.geometry("400x300")

# Create widgets
label_title = ctk.CTkLabel(root, text="Welcome to RobotSpeaker", font=("Helvetica", 16), text_color="white")
entry_text = ctk.CTkEntry(root, placeholder_text="Enter what you want me to say", width=300)
button_speak = ctk.CTkButton(root, text="Speak", command=speak_text)
button_quit = ctk.CTkButton(root, text="Quit", command=quit_app)
label_note = ctk.CTkLabel(root, text="Press 'quit' to exit", text_color="grey")

# Layout widgets
label_title.pack(pady=20)
entry_text.pack(pady=10)
button_speak.pack(pady=10)
button_quit.pack(pady=10)
label_note.pack(pady=10)

# Run the main loop
root.mainloop()



