# LIBS
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from crewai import (Agent, Task, Crew)
from crewai_tools import (ScrapeWebsiteTool)

# INITS
load_dotenv()

# FUNCS
def app(question) -> None:
    
    llm = ChatGroq(model='groq/llama3-70b-8192',
                   model_kwargs={'provider': 'Huggingface'},
                   temperature=0.5,
                   api_key=os.getenv('GROQ_API_KEY'))
    
    user_manual = ScrapeWebsiteTool(website_url='https://arquivar.gitbook.io/manual-arqged-or-colaboradores-e-franqueados/caixa-ou-pasta/configurar')
    
    search_agent = Agent(role='Senior Researcher',
                         goal='Find answers to questions received based on user manual.',
                         backstory='Specialist in the ArqGED system.',
                         llm=llm,
                         tools=[user_manual],
                         #verbose=True,
                         allow_delegation=True)
    
    editor_agent = Agent(role='Senior Editor',
                         goal='Write a clear response based on the question received and the data obtained by other agents.',
                         backstory='You are an experienced, confident writer and know how to express yourself clearly and directly.',
                         llm=llm,
                        #  verbose=True,
                         tools=[])
    
    task = Task(description='Respond to user questions by consulting the information available in the manual, use the editor_agent to write the final text.'
                            'Question: {question}',
                agent=search_agent,
                expected_output='Text aways in PT-BR.')
    
    crew = Crew(agents=[search_agent, editor_agent],
                tasks=[task])
    
    crew.kickoff(inputs={'question': question})
    
    print(crew)

# APP
if __name__ == '__main__':
    q = input('Pergunte a respeito da configuração de caixa: ')
    app(question=q)
    