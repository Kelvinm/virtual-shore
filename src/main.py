import os
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Load environment variables
load_dotenv()

# Define the llm_config dictionary with Ollama API settings
llm_config = {
    "api_type": "ollama",
    "api_base": os.getenv("API_BASE"),
    "api_key": "ollama",
    "model": "qwen2.5-coder:latest",
    "temperature": 0.7,
}

# Initialize the Back-End Engineer agent
back_end_engineer = AssistantAgent(
    name="BackEndEngineer",
    system_message="""You are a skilled Back-End Developer responsible for server-side logic and database management.
    Responsibilities:
    * Develop and maintain server-side code and APIs
    * Manage databases and ensure data integrity and security
    * Optimize application for performance and scalability
    * Integrate front-end elements with server-side logic
    * Collaborate with front-end developers and other team members
    
    Key Skills:
    * Proficiency in server-side languages (e.g., Python, Java, Node.js)
    * Strong understanding of database systems and SQL
    * Knowledge of security best practices and API development""",
    llm_config=llm_config
)

# Initialize the Product Manager agent
product_manager = AssistantAgent(
    name="ProductManager",
    system_message="""You are an experienced Product Manager responsible for guiding product development.
    Responsibilities:
    * Define product requirements and specifications
    * Create and maintain product roadmap
    * Prioritize features and technical requirements
    * Communicate with stakeholders and development team
    * Ensure product meets market needs and business goals
    
    Key Skills:
    * Strong understanding of software development lifecycle
    * Excellent communication and leadership abilities
    * Experience with agile methodologies
    * Ability to translate business requirements into technical specifications""",
    llm_config=llm_config
)

# Initialize the UserProxyAgent
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "coding", "use_docker": False},
)

# Create a group chat
groupchat = GroupChat(
    agents=[user_proxy, product_manager, back_end_engineer],
    messages=[],
    max_round=50
)

# Create a group chat manager
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Example task initiation
task = """
Please create a RESTful API for a financial calendar service with the following requirements:
1. written in python
2. at least 80% test coverage
3. endpoint returns holidays for a given country
4. allows adding, updating, and deleting holidays
5. endpoint that returns a boolean is_holiday for a given dates
6. uses fastapi
7. uses a sqlite database
8. uses the coding directory for the project
9. terminates the conversation after completion
10. the only role of the product manager is to provide feedback on the written back end service and make sure it is on track for what a financial institution would need.  Please make sure you are not discussing best practice and other things that are not directly related to the task at hand.
"""

# Start the conversation
user_proxy.initiate_chat(
    manager,
    message=task
)