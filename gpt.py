from openai import OpenAI
import httpx as httpx

class ChatGptService:
    client: OpenAI = None
    message_list: list = None

    def __init__(self, token):
        token = "sk-proj-" + token[:3:-1] if token.startswith('gpt:') else token
        self.client = OpenAI(
            http_client=httpx.Client(proxies="http://18.199.183.77:49232"),
            api_key=token
        )
        self.message_list = []

