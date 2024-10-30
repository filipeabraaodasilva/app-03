# LIBS
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from crewai import (Agent, Task, Crew)
from crewai_tools import (WebsiteSearchTool)

# INITS
load_dotenv()

# FUNCS
def app() -> None:
    
    llm = ChatGroq(model='llama3-70b-8192',
                   temperature=0.5,
                   api_key=os.getenv('GROQ_API_KEY'))
    
    user_manual = WebsiteSearchTool(website='https://arquivar.gitbook.io/')
    
    agent = Agent(role='',
                  goal='',
                  backstory='',
                  llm='')

# APP
if __name__ == '__main__':
    app()
