import os
import openai
import json
import argparse
import time

# Credit: This is a modified version of a script obtained from ​Xijia (Polina) Zhang. 

api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = api_key


class Conversation:
    def __init__(self):
        self.messages = []

    def add_message(self, role: str, content: str):
        """
        Adds a new message to the conversation.
        
        Args:
            role (str): The role of the sender ('system', 'user' or 'assistant').
            content (str): The content of the message.
        """
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        """
        Returns the list of messages.
        """
        return self.messages

    def clear_messages(self):
        """
        Clears all messages in the conversation.
        """
        self.messages = []

    def load_from_json(self, file_path: str):
        """
        Loads messages from a JSON file and adds them to the conversation.
        
        Args:
            file_path (str): The path to the JSON file containing the conversation messages.
        """
        self.clear_messages()
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            for message in data:
                self.add_message(str(message['role']), str(message['content']))
        except:
            raise ValueError("Invalid JSON format: Expected json file in Conversation format.")


def save_conversation_to_file(conversation: Conversation, filename: str):
    """
    Saves the conversation to a JSON file.

    Args:
        conversation (Conversation): The conversation object containing the messages.
        filename (str): The name of the file to save the conversation to.
    """
    with open(filename, 'w') as file:
        json.dump(conversation.get_messages(), file, indent=4)


def save_answer_to_file(answer: str, filename: str):
    """
    Saves the answer to a TXT file.

    Args:
        answer (str): The response generated by the language model (LLM).
        filename (str): The name of the file to save the answer to.
    """
    with open(filename, "w") as file:
        file.write(answer)


def load_conversation_from_file(filename: str) -> Conversation:
    """
    Loads a conversation from a JSON file and returns a Conversation object.

    Args:
        filename (str): The name of the file to load the conversation from.

    Returns:
        Conversation: A Conversation object containing the loaded messages.
    """
    conversation = Conversation()
    try:
        with open(filename, 'r') as file:
            messages = json.load(file)
            for message in messages:
                conversation.add_message(message["role"], message["content"])
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file '{filename}'.")
    
    return conversation


def save_query_to_files(conversation: Conversation, answer: str, directory: str, queryname: str, model: str, write_prompt_only = False):
    """
    Saves the prompt to a JSON file and the answer to a txt file with assoaciated filenames

    Args:
        conversation (Conversation): The conversation object containing the input messages.
        answer (str): The response generated by the language model (LLM).
        directory (str): The path to the folder where the query will be saved.
        queryname (str): The name assigned to this query for identification purposes.
        model (str): The language model used to generate the response.
    """
    save_path = os.path.join(directory, f"{queryname}-{model}.json")
    save_conversation_to_file(conversation, save_path)
    save_answer_to_file(answer, os.path.join(directory, f"{queryname}-{model}.txt")) if not write_prompt_only else None


def callAPI(conversation, model, temperature, max_tokens):
    completion = openai.chat.completions.create(
        model=model,
        temperature = temperature,
        messages=conversation.get_messages(),
        max_tokens=max_tokens
    )
    print(f"{completion.choices[0].message.content}")
    return completion.choices[0].message.content


def is_string_empty(s):
    return not s.strip()


def query_and_save(conversation, directory, queryname, model, temperature=0.2, max_tokens=256, write_prompt_only = False):
    """
    Queries the API with the provided prompt and saves the result.

    Args:
        conversation (Conversation): The conversation object containing the current messages.
        directory (str): The path to the folder where the query will be saved.
        queryname (str): The name assigned to this query for identification purposes.
        model (str): The language model used to generate the response.
        temperature (float): The temperature parameter for controlling randomness in API output (default is 0.2).
        max_tokens (int): The maximum number of tokens for the API response (default is 256).

    Returns:
        bool: Returns True if the process was successful, otherwise False.
        str: The path to the answer (useful in CoT prompting)
    """
    success = True

    def attempt_api_call(conversation, temperature, max_tokens):
        try:
            return callAPI(conversation, model=model, temperature=temperature, max_tokens=max_tokens)
        except Exception as e:
            print(f"Error querying the API: {str(e)}")
            return None
        
    if write_prompt_only:
        save_query_to_files(conversation, "", directory, queryname, model, write_prompt_only=True)
        return True, ""

    answer = attempt_api_call(conversation, temperature, max_tokens)
    
    # Retry loop for empty responses
    while is_string_empty(answer):
        answer = attempt_api_call(conversation, temperature, max_tokens)
    
    if answer is None:
        # Retry after waiting if API call failed
        print("Error while querying the API | Cooling down for 10 seconds...")
        time.sleep(10)
        answer = attempt_api_call(conversation, temperature, max_tokens)

        if answer is None:
            print(f"Prompt with directory {directory}; queryname {queryname} exceeds token limit!")
            success = False

    if success:
        save_query_to_files(conversation, answer, directory, queryname, model)
    
    return success, os.path.join(directory, f"{queryname}-{model}.txt") if success else None