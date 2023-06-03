import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import wikipediaapi
import requests
import io



class ChatBot:
    def __init__(self, master):
        self.master = master
        master.title("ChatBot")

        # Create chat display
        self.chat_display = tk.Text(master, state=tk.DISABLED, bg="pale turquoise", fg="cyan4", font=("times new roman", 16))
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Create user input field
        self.user_input = tk.Entry(master, bg="darkolivegreen3", fg="#333333", font=("times new roman", 16))
        self.user_input.pack(fill=tk.X)

        # Bind Enter key to send message
        self.user_input.bind("<Return>", self.send_message)

        # Wikipedia API
        self.wiki_wiki = wikipediaapi.Wikipedia('en')

        # Predefined responses
        self.responses = {
            'hi': 'Hey!',
            'hello': 'Hello!',
            'how are you': "I'm good, thank you!",
            'what is your name': 'My name is ChatBot.',
            'what can you do': 'I can provide information and have conversations.',
            'how does wikipedia work': 'Wikipedia is a collaboratively edited online encyclopedia.',
            'tell me a joke': 'Why dont scientists trust atoms? Because they make up everything!',
            'which languages can you speak': 'I only converse in English as of now.',
            'do you like people': 'They can certainly be annoying at times, but they are fun.',
            'what is the largest ocean': 'The largest ocean is the Pacific Ocean.',
            'what is the meaning of life': 'The meaning of life is subjective and varies for each individual.',
            'tell me about Python programming language': 'Python is a high-level programming language.',
            'how can I learn to code': 'You can start learning to code through online tutorials and resources.',
            'thank you': 'You\'re welcome!',
            'goodbye': 'Goodbye! Have a great day!',
            'okay': 'Do you want to ask anything else?',
            'no': 'Alright',
            'yes': 'Sure',
        }

    def send_message(self, event=None):
        user_message = self.user_input.get()
        self.user_input.delete(0, tk.END)

        self.display_message(user_message, "User")
        self.respond(user_message)

    def display_message(self, message, sender):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def display_image(self, image_url):
        response = requests.get(image_url)
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((200, 200))  # Adjust the size of the image as needed
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(self.master, image=photo)
        image_label.image = photo
        image_label.pack()


    def respond(self, message):
        message = message.lower()

        if message in self.responses:
            self.display_message(self.responses[message], "ChatBot")
        elif 'wikipedia' in message:
            search_query = message.replace('wikipedia', '')
            page = self.wiki_wiki.page(search_query)
            if page.exists():
                summary = page.summary[0:600] + "..." if len(page.summary) > 600 else page.summary
                self.display_message(summary, "ChatBot")
            else:
                self.display_message("I'm sorry, I couldn't find any information on that.", "ChatBot")
        else:
            self.display_message("I'm sorry, I don't understand.", "ChatBot")

def main():
    root = tk.Tk()
    chatbot = ChatBot(root)
    root.mainloop()

if __name__ == "__main__":
    main()
