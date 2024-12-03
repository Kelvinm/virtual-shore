import autogen
import requests
from dotenv import load_dotenv

load_dotenv()

def test_connections():
    # Test the Ollama API connection
    response = requests.get("http://localhost:11434/api/version")
    print(f"REST API test: {response.json()}")

try:
    test_connections()

    # Define the llm_config dictionary with Ollama API settings
    llm_config = {
        "api_type": "ollama",
        "api_base": "http://localhost:11434/api",
        "api_key": "ollama",  # Adjust if your API requires a different key
        "model": "llama3.1:latest",
        "temperature": 0.7,
    }

    # Initialize the AssistantAgent with the llm_config
    assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config=llm_config
    )

    # Initialize the UserProxyAgent
    user_proxy = autogen.UserProxyAgent(
        name="User",
        human_input_mode="TERMINATE",
        code_execution_config={"use_docker": False}
    )

    # Start the conversation
    user_proxy.initiate_chat(
        assistant,
        message="Say hello"
    )

except Exception as e:
    print(f"Error type: {type(e)}")
    print(f"Full error: {str(e)}")
    print(f"Error args: {e.args}")
