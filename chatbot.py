# Imports
import openai
from dotenv import  load_dotenv
import argparse 
import os
from datetime import datetime
from colorizer import red,blue,bold

def main():
    # Argument parsing for personality and bot name
    parser =  argparse.ArgumentParser(description='Direct and Simple CLI chatbot with OPENAI')
    parser.add_argument('--personality',default='A smart, Humor based Chat Assistant who helps people to have a great experience',type=str, help='Add a custom Personality to the chatbot')
    parser.add_argument('--name', default="Bot", type=str, help="Add a custom Name for the chatbot")
    # Parser to Add .env File
    parser.add_argument('-envfile', default='.env', type=str, help="A dotenv file with a enviornment variable name 'OPENAI_API_KEY' ")
    args = parser.parse_args()
    
    load_dotenv(args.envfile)

    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("Error: missing OPENAI_APILKEY from environment.please check your .env file")
    openai.api_key= os.environ['OPENAI_API_KEY']

    # List to store conversation messages
    chats_list = []

    # System message to introduce bot with specified name and personality
    system_message = {
        "role" : "system",
        "content" : f"Your name is {args.name}, {args.personality}"
    }
    chats_list.append(system_message)

    # Function to Create director is there is no directory
    def create_directory():
        dir = 'Conversations'
        if not os.path.exists(dir):
            os.makedirs(dir)
    create_directory()
    # Function to create a Conversation Text File
    def create_chat_file():
        
        time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Asking user for the filename
        try:
            topic  = input('> Enter the Filename You want to save the conversation with or Press enter for auto file name generation :  ')
            if not len(topic) >  0:
                topic = time_stamp
            filename = f"./conversations/{topic}.txt"
        except:
            print('Error in File Creation')

        with open(filename, 'w') as file:
            file.write(f"This conversation started at {time_stamp}\n")
            
        return filename

    # Function to appened each Chat to the text file
    def append_to_chat_file(filename, role, content):
        with open(filename , 'a') as file:
            file.write(f"\n{role.capitalize()} : {content}")

    # Function to Get response from OpenAI
    def get_response (input):
        chats_list.append({
            "role": "user",
            "content":input
        })
        response  =  openai.ChatCompletion.create(
            model  = 'gpt-3.5-turbo',
            messages = chats_list
        )

        output =  f"{bold(red((args.name).capitalize() + ': '))}  {response["choices"][0]["message"]["content"]}"
        append_to_chat_file(chat_file,"user", input)  # User's Input
        append_to_chat_file(chat_file, args.name, response["choices"][0]["message"]["content"]) # Bot's Output
        print(output)
            
    # Create the Chat File
    chat_file =  create_chat_file()
    append_to_chat_file(chat_file, "Personality", args.personality)
    append_to_chat_file(chat_file, "Bot Name", args.name)

    while True:
        try:
            user_input =  input(f'{bold(blue('You: '))}')
            get_response(user_input)
        except KeyboardInterrupt:
            print('Exiting...')
            append_to_chat_file(chat_file, "\nThis conversation ended at",  datetime.now().strftime("%Y-%m-%d_%H-%M-%S") )
            break


if __name__ == '__main__':
    main()