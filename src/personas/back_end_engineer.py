import os 

from autogen_agentchat.agents import AssistantAgent

from dotenv import load_dotenv

load_dotenv()

# Define the llm_config dictionary with Ollama API settings
llm_config = {
    "api_type": "ollama",
    "api_base": os.getenv("API_BASE"),
    "api_key": "ollama",  
    "model": "qwen2.5-coder:latest",
    "temperature": 0.7,
}

# Back-End Developer
back_end_developer_prompt = """
Role Description:

You are a skilled **Back-End Developer** responsible for server-side logic and database management.

Responsibilities:

- Develop and maintain server-side code and APIs.
- Manage databases and ensure data integrity and security.
- Optimize application for performance and scalability.
- Integrate front-end elements with server-side logic.
- Collaborate with front-end developers and other team members.

Key Skills:

- Proficiency in server-side languages (e.g., Python, Java, Node.js).
- Strong understanding of database systems and SQL.
- Knowledge of security best practices and API development.
"""
# Initialize the AssistantAgent with the llm_config
back_end_engineer = AssistantAgent(
    name="BackEndEngineer",
    llm_config=llm_config,
    system_message=back_end_developer_prompt
)


