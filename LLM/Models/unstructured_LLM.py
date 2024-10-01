import sys
sys.path.append("..")
import json

import Domains.get_water as water
import Domains.load_dishes as dishes


def save_to_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)

def load_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def plan_prompt_content(example_domain=water, target_domain=dishes, file_path='Prompts/plan_prompt_skeleton.txt'):
    """
    Loads the first prompt in the Chain-of-Thought, to make initial robot plan

    Args:
        target_domain (str): target domain (used to load task description).
        example_domain (str): example task (used to load task description).
        file_path (str): Path to skeleton text for generating a plan.
    """
    with open(file_path, 'r') as file:
        file_content = file.read()

    # example domain
    file_content = file_content.replace("<insert-example-domain-name>", example_domain.get_name())
    file_content = file_content.replace("<insert-example-task>", example_domain.get_task())
    file_content = file_content.replace("<insert-example-actions>", example_domain.get_actions())
    
    file_content = file_content.replace("<insert-example-breakdown>", example_domain.get_plan())

    # target domain
    file_content = file_content.replace("<insert-target-domain-name>", target_domain.get_name())
    file_content = file_content.replace("<insert-target-task>", target_domain.get_task())
    file_content = file_content.replace("<insert-target-actions>", target_domain.get_actions())

    return file_content


def confusion_prompt_content(human_question, target_domain=dishes, file_path='Prompts/confusion_prompt_skeleton.txt'):
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
    file_content = file_content.replace("<insert-target-human-question>", human_question)

    # target domain
    file_content = file_content.replace("<insert-target-interrupted-action>", target_domain.get_interrupted_action())

    return file_content


def explanation_prompt_content(target_domain=dishes, file_path='Prompts/explanation_prompt_skeleton.txt'):
    """
    Loads the third prompt in the Chain-of-Thought, to provide an explanation to address the confusion underlying the question.

    Args:
        file_path (str): Path to skeleton text for generating a plan.
    """
    with open(file_path, 'r') as file:
        file_content = file.read()

    return file_content


def get_plan():
    prompt = [{
        "role": "user",
        "content": plan_prompt_content()
    }]

    return prompt


def get_confusion():
    human_clarification_question = input("Enter the user clarification: ")

    prompt = [{
        "role": "user",
        "content": confusion_prompt_content(human_clarification_question)
    }]

    return prompt


def get_explanation():
    prompt = [{
        "role": "user",
        "content": explanation_prompt_content()
    }]

    return prompt


def main():

    save_to_json(get_plan(), 'Prompts/plan_prompt.json')
    save_to_json(get_confusion(), 'Prompts/confusion_prompt.json')
    save_to_json(get_explanation(), 'Prompts/explanation_prompt.json')

if __name__ == "__main__":
    main()