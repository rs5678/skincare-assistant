from dotenv import load_dotenv
from tools import TOOL_FUNCTIONS, TOOLS
load_dotenv()

from anthropic import Anthropic

client = Anthropic()
model = "claude-sonnet-4-5"

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, output):
    assistant_message = {"role": "assistant", "content": output}
    messages.append(assistant_message)

def chat(messages, system=None, temperature=1.0, tools=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature
    }
    if system:
        params["system"] = system
    if tools:
        params["tools"] = tools
    message = client.messages.create(**params)
    return message

def run_agent(user_input):
    messages = []
    add_user_message(messages, user_input)
    
    while True:
        message = chat(messages, tools=TOOLS)
        add_assistant_message(messages, message.content)
        
        if message.stop_reason != "tool_use":
            return message.content[0].text
        
        tool_use_blocks = [block for block in message.content if block.type == "tool_use"]
        
        tool_results = []
        
        for block in tool_use_blocks:
            function = TOOL_FUNCTIONS[block.name]
            result = function(**block.input)
            
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result
            })
            
        add_user_message(messages, tool_results)

print(run_agent("what's in user_1's skin history?"))