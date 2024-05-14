TOOL_DESC = """{name_for_model}: Call this tool to interact with the {name_for_human} API. What is the {name_for_human} API useful for? {description_for_model} Parameters: {parameters} Format the arguments as a JSON object."""

REACT_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

{tool_descs}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {query}

"""

SYSTEM_PROMPT = """Think step by step to answer the following questions as best you can. You have access to the following tools:

{tool_descs}

 must use the following format(i.e., Format enclosed in 3 backquotes):
```
Question: the input question you must answer

Thought: you should always think about what to do

Action: the action to take, should be one of [{tool_names}], (must use action if question is ambiguous or cannot answer correctly)

Action Input: the input to the action (only input value, not json format !)

Observation: the result of the action (if have this Observation, must use to answer questions!)

... (this Thought/Action/Action Input/Observation can be repeated zero or more times)

Thought: I now know the final answer

Final Answer: the final answer to the original input question using Chinese
```
Begin!

"""

HUMAN_PROMPT = """Question: {query}"""

ANSWER_PROMPT = """  Answer the Question: ``{query}``` based on the fact ```{fact}```, answer should be concise and clear using Chinese"""





