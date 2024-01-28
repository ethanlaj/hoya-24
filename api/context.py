import os
import dotenv
import getpass
dotenv.load_dotenv()


OPENAI_API_KEY  = os.getenv["OPENAI_API_KEY"] 
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("wagwan, bruv?")
memory.chat_memory.add_ai_message("Alright, guv'nor? Just been 'round the old manor, innit?")