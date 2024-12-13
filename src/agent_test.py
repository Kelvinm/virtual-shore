import tempfile
import os 
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor

# import and load .env file
from dotenv import load_dotenv
load_dotenv()

# Define the output directory where the code will write the output files.
output_directory = os.path.abspath(os.getenv("OUTPUT_DIRECTORY"))

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()
print(temp_dir.name)    
# Create a local command line code executor.
executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
    # work_dir='.'
)

# Create an agent with code executor configuration.
code_executor_agent = ConversableAgent(
    "code_executor_agent",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={"executor": executor},  # Use the local command line code executor.
    human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
)

# Define the llm_config dictionary with Ollama API settings
llm_config = {
    "api_type": "ollama",
    "api_base": os.getenv("API_BASE"),
    "api_key": "ollama",
    "model": "qwen2.5-coder:latest",
    "temperature": 0.7,
}


code_writer_system_message = """You are a helpful AI assistant.
Solve tasks using your coding and language skills.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
Reply 'TERMINATE' in the end when everything is done.
"""

code_writer_agent = ConversableAgent(
    "code_writer_agent",
    system_message=code_writer_system_message,
    llm_config=llm_config,
    code_execution_config=False,  # Turn off code execution for this agent.
)


chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message=f"""please complete the following task:
                * create a basic hello world python script and write the python script to location: {output_directory}.  
                  * If the directory is not there create it. if writing to a temporary directory please specify the directory path.
                * please make sure to include a unit test file that will write to them same output location with the prefix of test_.
                  * if there is no pytest, please install it.
                *  once you create the script and test it, please TERMINATE the chat.

                * the output directory should contain 2 python files.
                
                """,
)
temp_dir.cleanup()