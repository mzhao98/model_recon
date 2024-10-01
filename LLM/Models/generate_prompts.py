import sys
sys.path.append("..")
import json

import Domains.get_water as water
import Domains.load_dishes as dishes


# save promt to json
def save_to_json(data, file_path):

    # format prompt with role and content fields
    def role_content_formatting(prompt_content):
        prompt = [{
                "role": "user",
                "content": prompt_content
            }]
        
        return prompt

    json_formatted_data = role_content_formatting(data)

    with open(file_path, 'w') as f:
        json.dump(json_formatted_data, f)


# read prompt txt files
def load_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# populate dynamic content for confusion prompt
def unstructured_LLM_prompt_content(example_domain, target_domain, file_path):
    """
    Loads the second prompt in the Chain-of-Thought, to identify the confusion underlying the question.

    Args:
        human_input (str): human input (question indicating confusion).
        target_domain (str): target domain (used to load task description).
        file_path (str): Path to skeleton text for generating a plan.
    """
    with open(file_path, 'r') as file:
        file_content = file.read()

    # human input
    file_content = file_content.replace("<insert-target-human-question>", target_domain.get_question())

    # example domain
    file_content = file_content.replace("<insert-example-domain-name>", example_domain.get_name())
    file_content = file_content.replace("<insert-example-task>", example_domain.get_task())
    file_content = file_content.replace("<insert-example-plan>", example_domain.get_plan())
    file_content = file_content.replace("<insert-example-interrupted-action>", example_domain.get_interrupted_action())
    file_content = file_content.replace("<insert-example-human-question>", example_domain.get_question())
    file_content = file_content.replace("<insert-example-confusion-source>", example_domain.get_confusion())
    file_content = file_content.replace("<insert-example-explanation>", example_domain.get_confusion_explanation())
    

    # target domain
    file_content = file_content.replace("<insert-target-domain-name>", target_domain.get_name())
    file_content = file_content.replace("<insert-target-task>", target_domain.get_task())
    file_content = file_content.replace("<insert-target-plan>", target_domain.get_plan())
    file_content = file_content.replace("<insert-target-interrupted-action>", target_domain.get_interrupted_action())
    file_content = file_content.replace("<insert-target-human-question>", target_domain.get_question())
    
    return file_content


# populate dynamic content for all facts prompt
def facts_based_LLM_prompt_content(example_domain, target_domain, file_path):
    """
    Loads the second prompt in the Chain-of-Thought, to identify the confusion underlying the question.

    Args:
        human_input (str): human input (question indicating confusion).
        target_domain (str): target domain (used to load task description).
        file_path (str): Path to skeleton text for generating a plan.
    """
    with open(file_path, 'r') as file:
        file_content = file.read()

    # example domain
    file_content = file_content.replace("<insert-example-domain-name>", example_domain.get_name())
    file_content = file_content.replace("<insert-example-task>", example_domain.get_task())
    file_content = file_content.replace("<insert-example-question>", example_domain.get_question())
    file_content = file_content.replace("<insert-example-facts>", example_domain.get_facts())
    file_content = file_content.replace("<insert-example-facts-to-communicate>", example_domain.get_facts_to_communicate())
    file_content = file_content.replace("<insert-example-facts-explanation>", example_domain.get_facts_explanation())

    # target domain
    file_content = file_content.replace("<insert-target-domain-name>", target_domain.get_name())
    file_content = file_content.replace("<insert-target-task>", target_domain.get_task())
    file_content = file_content.replace("<insert-target-question>", target_domain.get_question())

    return file_content


# Unstructured LLM Model 
def unstructured_LLM(example_domain, target_domain):

    file_path='Prompts/unstructured_LLM_prompt_skeleton.txt'

    # human_clarification_question = input("Enter the user clarification: ")

    save_to_json(
        unstructured_LLM_prompt_content(example_domain=example_domain, target_domain=target_domain, file_path=file_path), 
        'Prompts/unstructured_LLM_prompt.json')


# Facts based LLM Model
def facts_based_LLM(example_domain, target_domain):

    file_path='Prompts/facts_based_LLM_prompt_skeleton.txt'

    save_to_json(
        facts_based_LLM_prompt_content(example_domain=example_domain, target_domain=target_domain, file_path=file_path), 
        'Prompts/facts_based_LLM_prompt.json')


def main():

    example_domain = water
    target_domain = dishes

    unstructured_LLM(example_domain, target_domain)
    facts_based_LLM(example_domain, target_domain)

if __name__ == "__main__":
    main()