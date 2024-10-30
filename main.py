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
    
    llm = ChatGroq(model='groq/llama3-70b-8192',
                   model_kwargs={'provider': 'Huggingface'},
                   temperature=0.5,
                   api_key=os.getenv('GROQ_API_KEY'))
    
    user_manual = WebsiteSearchTool(website='https://arquivar.gitbook.io/')
    
    search_agent = Agent(role='Senior Researcher',
                         goal='Find answers to questions received.',
                         backstory='Specialist in the ArqGED system.',
                         llm=llm,
                         tools=[user_manual],
                         verbose=True,
                         allow_delegation=True)
    
    editor_agent = Agent(role='Senior Editor',
                         goal='Write a clear response based on the question received and the data obtained by other agents.',
                         backstory='You are an experienced, confident writer and know how to express yourself clearly and directly.',
                         llm=llm,
                         tools=[],
                         verbose=True)
    
    task = Task(description='Respond to user questions by consulting the information available in the manual.'
                            'Questionamento: {question}',
                agent=search_agent,
                expected_output='Text aways in PT-BR.')
    
    crew = Crew(agents=[search_agent, editor_agent],
                tasks=[task])
    
    crew.kickoff(inputs={'question': 'O que é workflow?'})

# APP
if __name__ == '__main__':
    app()
