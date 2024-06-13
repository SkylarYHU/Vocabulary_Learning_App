import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

# *-------------------------------------------------------------*
# A system extension only for Windows 10 to look much more crisp
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
# *-------------------------------------------------------------*

# Initial list of words and their synonyms
initial_words = [
  {"word": "person", "synonym": "individual, human, being"},
  {"word": "code", "synonym": "program, script, command, snippet"},
  {"word": "work", "synonym": "job, task, employment"},
  {"word": "way", "synonym": "method, manner, approach"},
  {"word": "thing", "synonym": "object, item, stuff"},
  {"word": "serendipity", "synonym": "providence, fluke, fortuity, happenstance"},
  {"word": "world", "synonym": "globe, planet"},
  {"word": "state", "synonym": "condition, situation"},
  {"word": "conundrum", "synonym": "enigma, puzzle, mystery, riddle"},
  {"word": "place", "synonym": "location, spot"},
  {"word": "night", "synonym": "evening, darkness"},
  {"word": "area", "synonym": "region, zone"},
  {"word": "car", "synonym": "vehicle, automobile"},
  {"word": "bug", "synonym": "glitch, error, defect, fault, issue"},
  {"word": "team", "synonym": "group, squad"},
  {"word": "high", "synonym": "tall, above"},
]

class VocabularyApp:
  def __init__(self, root):
    self.root = root
    # Copy the initial words
    self.original_words = initial_words.copy()
    # Initialize the words list
    self.words = self.original_words.copy()
    self.current_word = None
    self.score = 0
    self.total_words = len(self.words)
    
    self.initial(root)
    self.create_widgets(root)

  def initial(self, root):
    # Set the window size and title
    root.geometry("1400x800")
    root.configure(bg='#1F1F1F')
    root.title("Vocabulary Learning")

  def create_widgets(self, root):
    s = ttk.Style()
    s.theme_use('clam')

    # Configure styles for various widgets
    s.configure('Custom.TFrame', background="#1F1F1F")
    s.configure('Greet.TLabel', background="#1F1F1F", foreground='#FFFFFF', font=("Times New Roman", 50))

    s.configure('Custom.TButton', background='#0056b3', foreground='#f2f2f2', font=("Arial", 18))
    s.map('Custom.TButton', background=[('active', '#1F6AA4')])
    
    s.configure('Question.TLabel', background="#1F1F1F", foreground='#FFFFFF', font=("Arial Bold", 22))
    s.configure('Answer.TLabel', background="#1F1F1F", foreground='#FFFFFF', font=("Arial", 18))
    s.configure('Answer.TEntry', fieldbackground="#FFFFFF", foreground='#1F1F1F', font=("Arial", 20), padding=6)
    s.configure('Feedback.TLabel', background="#1F1F1F", foreground='#8D8D8D', font=("Arial", 18))
    s.configure('Score.TLabel', background="#1F1F1F", foreground='#8D8D8D', font=("Arial", 18))
    
    # Greeting frame
    greet_frame = ttk.Frame(root, padding=(0, 40, 0, 20), style="Custom.TFrame")
    greet_frame.pack(fill="both")

    greet_label = ttk.Label(greet_frame, text="Vocabulary Learning", style='Greet.TLabel')
    greet_label.pack()
    
    # Buttons frame
    buttons_frame = ttk.Frame(root, padding=(0, 20, 0, 20), style="Custom.TFrame")
    buttons_frame.columnconfigure((0, 1, 2, 3), weight=1)
    buttons_frame.pack(fill="both")

    # Start/Reset button
    start_button = ttk.Button(buttons_frame, text="Start / Reset", command=self.start_game, style="Custom.TButton", width=15)
    start_button.grid(row=1,column=0, padx=10, pady=5, sticky="ew")

    # Submit button
    self.submit_button = ttk.Button(buttons_frame, text="Submit", command=self.check_answer, style="Custom.TButton", width=15)
    self.submit_button.grid(row=1,column=1, padx=10, pady=5, sticky="ew")

    # End button
    quit_button = ttk.Button(buttons_frame, text="End", command=root.destroy, style="Custom.TButton", width=15)
    quit_button.grid(row=1,column=2, padx=10, pady=5, sticky="ew")

    # Add new word button
    add_word_button = ttk.Button(buttons_frame, text="Add New Word", command=self.add_new_word, style="Custom.TButton", width=15)
    add_word_button.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

    # Question label
    self.question_label = ttk.Label(root, text="== Click Start / Reset to begin the game ==", padding=(0, 30, 0, 20), style="Question.TLabel")
    self.question_label.pack()

    # Answer prompt label
    answer_label = ttk.Label(root, text="\U0001F447 Please input your answer below: \U0001F447  ", padding=(0, 20, 0, 0), style="Answer.TLabel")
    answer_label.pack()

    # Answer entry box
    self.answer_entry = ttk.Entry(root, width=35, style="Answer.TEntry")
    self.answer_entry.bind('<Return>', lambda event: self.check_answer())
    self.answer_entry.pack(pady=15)
    
    # Feedback display label
    self.feedback_display = ttk.Label(root, text="(Feedback will be shown here)", padding=(0, 5, 0, 15), style='Feedback.TLabel')
    self.feedback_display.pack()

    # Score display label
    self.score_label = ttk.Label(root, text=f"Your Score: 0/{self.total_words}", padding=(0, 20, 0), style="Score.TLabel")
    self.score_label.pack()
  
  def add_new_word(self):
    # Create a dialog to add new word and its synonym
    add_word_window = tk.Toplevel(self.root)
    add_word_window.title("Add New Word")
    add_word_window.configure(bg='#1F1F1F')

    # New word label and entry
    new_word_label = ttk.Label(add_word_window, text="New Word:", style="Question.TLabel")
    new_word_label.config(font=("Arial",18))
    new_word_label.grid(row=0, column=0, padx=10, pady=10)

    new_word_entry = ttk.Entry(add_word_window)
    new_word_entry.grid(row=0, column=1, padx=10, pady=10)

    # Synonym label and entry
    synonym_label = ttk.Label(add_word_window, text="Synonym (Please use commas to separate):", style="Question.TLabel")
    synonym_label.config(font=("Arial",18))
    synonym_label.grid(row=1, column=0, padx=10, pady=10)

    synonym_entry = ttk.Entry(add_word_window)
    synonym_entry.grid(row=1, column=1, padx=10, pady=10)

    # Submit button for the new word
    submit_button = ttk.Button(add_word_window, text="Submit", command=lambda: self.submit_new_word(add_word_window, new_word_entry, synonym_entry), style="Custom.TButton")
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)

  def submit_new_word(self, add_word_window, new_word_entry, synonym_entry):
    # Get the new word and synonym, trim whitespace
    new_word = new_word_entry.get().strip()
    synonym = synonym_entry.get().strip()

    # Check if either field is empty
    if not new_word or not synonym:
        messagebox.showerror("Error", "Please enter both the word and its synonym.")
        return

    # Check if the word already exists
    for word in self.original_words:
        if word['word'] == new_word:
            messagebox.showerror("Error", "The word already exists.")
            return

    # Add the new word and synonym to the list
    self.original_words.append({"word": new_word, "synonym": synonym})
    messagebox.showinfo("Successful", "New word added successfully!")
    add_word_window.destroy()

    # Update the total number of words
    self.total_words += 1
    self.update_score()

    # Restart the game to include the new word
    self.start_game()

  def start_game(self):
    # Reset the words to include the original and newly added words
    self.words = self.original_words.copy()
    # Shuffle the words
    random.shuffle(self.words)
    # Reset score
    self.score = 0
    # Update the score display
    self.update_score()
    # Ask the first question
    self.ask_next_question()
    self.feedback_display.config(text="(Feedback will be shown here)", foreground="#8D8D8D")
    # Enable submit button
    self.submit_button.config(state=tk.NORMAL)

  def ask_next_question(self):
    # Check if there are any words left
    if len(self.words) == 0:
        # If no more words, end the game
        messagebox.showinfo("", f"Your final score is {self.score}!")
        # Disable submit button
        self.submit_button.config(state=tk.DISABLED)
        # Show game over message
        self.feedback_display.config(text="Game over! Click 'Start / Reset' to play again.", foreground="#8D8D8D")
        return
    
    # Pop the next word and update the question label
    self.current_word = self.words.pop()
    self.question_label.config(text=f"What is the synonym of {self.current_word['word']}?")
    self.answer_entry.delete(0, tk.END)
      

  def check_answer(self):
    # Ensure the game has started
    # If there's no current word, display error
    if not self.current_word:
        messagebox.showerror("Error", "Please start the game first.")
        return
    
    # Get the user's answer and check it against the correct synonyms
    user_answer = self.answer_entry.get().strip().lower()
    correct_answer = self.current_word['synonym'].strip().lower()

    # Check if the answer is correct
    if user_answer in [syn.strip().lower() for syn in correct_answer.split(',')]:
        self.score += 1
        # Show correct feedback
        self.feedback_display.config(text=f"\U0001F38A Correct! \U0001F44F", foreground="#8AC44B")
    else:
        # Show incorrect feedback
        self.feedback_display.config(text=f"\U0001F4A5 Incorrect! {self.current_word['word']} means {self.current_word['synonym']}...", foreground="#F8981C")

    # Update the score and ask the next question
    self.update_score()
    self.ask_next_question()

  def update_score(self):
    # Update the score display
    self.score_label.config(text=f"Your Score: {self.score}/{self.total_words}")

if __name__ == "__main__":
  root = tk.Tk()
  app = VocabularyApp(root)
  root.mainloop()
