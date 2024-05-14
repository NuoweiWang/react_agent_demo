from .chat_zhipuai import ChatZhipuAI

class llm_api:
    _instance = None
    
    @staticmethod
    def getInstance():
        if llm_api._instance is None:
            llm_api()
        return llm_api._instance

    def __init__(self):
        if llm_api._instance is not None:
            raise ValueError("An instantiation already exists!")
        else:
            llm_api._instance = ChatZhipuAI(model_name="glm-4", api_key = "your-key", temperature = 0.55)
