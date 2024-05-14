from .outside_tools import Tools 
import json
import json5
from langchain.prompts import (
    ChatPromptTemplate
)
from .model_api import llm_api
from .build_prompt import *
from langchain.chains import LLMChain
from .outside_tools import Tools
from .prompt_template import ANSWER_PROMPT

class Agent:
    system_prompt = SystemMessagePromptTemplate.from_template(
            build_system_prompt(Tools())
        )
    tool = Tools()


    def __init__(self, model) -> None:
        self.model = model
        self.memory = ConversationBufferWindowMemory(k=2,memory_key="chat_history", return_messages=True)
        self.message_setting = MessagesPlaceholder(variable_name="chat_history")
        self.human_prompt = build_human_prompt()

    
    def parse_latest_plugin_call(self, text):
        plugin_name, plugin_args = '', ''
        i = text.rfind('\nAction:')
        j = text.rfind('\nAction Input:')
        k = text.rfind('\nObservation:')
        if 0 <= i < j:  
            if k < j:  
                text = text.rstrip() + '\nObservation:'  
            k = text.rfind('\nObservation:')
            plugin_name = text[i + len('\nAction:') : j].strip()
            plugin_args = text[j + len('\nAction Input:') : k].strip()
            text = text[:k]
        return plugin_name, plugin_args, text
    
    def call_plugin(self, plugin_name, plugin_args):
        if plugin_name == 'Search':
            return Agent.tool.google_search(plugin_args)

    def chat(self, text):
        prompt = ChatPromptTemplate(
            messages= [
            Agent.system_prompt,
            self.message_setting,
            self.human_prompt
                ])        
        conversation = LLMChain(
            llm=self.model,
            prompt=prompt,
            verbose=False,
            memory=self.memory
        )

        response = conversation({"question": text})
        plugin_name, plugin_args, response = self.parse_latest_plugin_call(response["text"])

        if plugin_name:
            if type(plugin_args) == dict:
                plugin_args = list(plugin_args.values())[0]  
            fact = self.call_plugin(plugin_name, plugin_args)
            response = ANSWER_PROMPT.format(query=text, fact=fact)
            response = conversation({"question": response})
            response = response['text']

        if '\nFinal Answer:' in response:
            response = response[(response.rfind('\nFinal Answer:')+ len("\nFinal Answer:"))::].strip()
            response = response.replace("\n", "")
            response = response.replace("Final Answer:", " ")

        response = response.replace("```", " ")
            

        return response.strip()

# if __name__ == '__main__':
#     agent = Agent(llm_api)
#     prompt = agent.build_planning_prompt()
#     print(prompt)