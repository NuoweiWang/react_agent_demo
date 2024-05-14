from .prompt_template import TOOL_DESC, REACT_PROMPT,SYSTEM_PROMPT
from .outside_tools import Tools
import json
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.memory import ConversationBufferWindowMemory


def build_system_prompt(TOOLS):
    tool_descs = []
    tool_names = []
    for info in TOOLS.toolConfig:
        tool_descs.append(
            TOOL_DESC.format(
                name_for_model=info['name_for_model'],
                name_for_human=info['name_for_human'],
                description_for_model=info['description_for_model'],
                parameters=json.dumps(
                    info['parameters'], ensure_ascii=False),
            )
        )
        tool_names.append(info['name_for_model'])
    tool_descs = '\n\n'.join(tool_descs)
    tool_names = ','.join(tool_names)


    system_message_prompt = SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT)
    prompt_template = ChatPromptTemplate.from_messages([system_message_prompt])  
    prompt = prompt_template.format_prompt(tool_descs=tool_descs, tool_names=tool_names).to_messages()
    return str(prompt[0].content).replace("{", "{{").replace("}", "}}")


def build_human_prompt():

    human_template = """Question: {question}"""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    
    return human_message_prompt

def build_history(history_name,recent_k):

    memory = ConversationBufferWindowMemory(k=recent_k,memory_key=history_name, return_messages=True)

    message_setting = MessagesPlaceholder(variable_name=history_name)

    return memory,message_setting


