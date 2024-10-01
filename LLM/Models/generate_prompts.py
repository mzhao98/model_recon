import sys
sys.path.append("..")
import json

import Domains.get_water as water
import Domains.load_dishes as dishes
import Explanation.contrastive_explanations as explanation


# global variables
example_domain = water
target_domain = dishes

contrastive = 1


# get file paths for skeleton code, and where to save the prompt (json and human read-ible txt)
def get_file_paths(model_name):

    skeleton_file_path= f"Prompts/{model_name}_prompt_skeleton.txt"
    json_file_path= f"Prompts/{model_name}_prompt.json"
    txt_file_path= f"Prompts//{model_name}_human_readible_prompt.txt"

    return skeleton_file_path, json_file_path, txt_file_path


# save promt to json
def save_to_json(data, json_file_path, txt_file_path):

    # format prompt with role and content fields
    def role_content_formatting(prompt_content):
        prompt = [{
                "role": "user",
                "content": prompt_content
            }]
        
        return prompt

    json_formatted_data = role_content_formatting(data)

    # json (to pass in prompt)
    with open(json_file_path, 'w') as f:
        json.dump(json_formatted_data, f)

    with open(txt_file_path, 'w') as f:
        f.write(data)


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


# populate dynamic content for Unstructured LLM Model 
def unstructured_LLM_prompt_content(file_path):
    """
    Loads the second prompt in the Chain-of-Thought, to identify the confusion underlying the question.

    Args:
        human_input (str): human input (question indicating confusion).
        target_domain (str): target domain (used to load task description).
        file_path (str): Path to skeleton text for generating a plan.
    """
    with open(file_path, 'r') as file:
        file_content = file.read()

    # explanation design
    contrastive_explanation_design = explanation.get_contrastive_explanation() if contrastive else explanation.get_non_contrastive_explanation()
    file_content = file_content.replace("<insert-explanation-design>", contrastive_explanation_design) 

    # example domain
    file_content = file_content.replace("<insert-example-domain-name>", example_domain.get_name())
    file_content = file_content.replace("<insert-example-task>", example_domain.get_task())

    file_content = file_content.replace("<insert-example-plan>", example_domain.get_plan())
    file_content = file_content.replace("<insert-example-interrupted-action>", example_domain.get_interrupted_action())
    file_content = file_content.replace("<insert-example-human-question>", example_domain.get_question())

    file_content = file_content.replace("<insert-example-confusion-source>", example_domain.get_confusion())
    file_content = file_content.replace("<insert-example-explanation>", example_domain.get_explanation())
    

    # target domain
    file_content = file_content.replace("<insert-target-domain-name>", target_domain.get_name())
    file_content = file_content.replace("<insert-target-task>", target_domain.get_task())

    file_content = file_content.replace("<insert-target-plan>", target_domain.get_plan())
    file_content = file_content.replace("<insert-target-interrupted-action>", target_domain.get_interrupted_action())
    file_content = file_content.replace("<insert-target-human-question>", target_domain.get_question())
    
    return file_content


# populate dynamic content for Facts based LLM Model
def facts_based_LLM_prompt_content(file_path):
    """
    Loads the second prompt in the Chain-of-Thought, to identify the confusion underlying the question.

    Args:
        human_input (str): human input (question indicating confusion).
        target_domain (str): target domain (used to load task description).
        file_path (str): Path to skeleton text for generating a plan.
    """
    with open(file_path, 'r') as file:
        file_content = file.read()

    # explanation design
    contrastive_explanation_design = explanation.get_contrastive_explanation() if contrastive else explanation.get_non_contrastive_explanation()
    file_content = file_content.replace("<insert-explanation-design>", contrastive_explanation_design) 

    # example domain
    file_content = file_content.replace("<insert-example-domain-name>", example_domain.get_name())
    file_content = file_content.replace("<insert-example-task>", example_domain.get_task())

    file_content = file_content.replace("<insert-example-plan>", example_domain.get_plan())
    file_content = file_content.replace("<insert-example-interrupted-action>", example_domain.get_interrupted_action())
    file_content = file_content.replace("<insert-example-human-question>", example_domain.get_question())

    file_content = file_content.replace("<insert-example-facts>", example_domain.get_facts())
    file_content = file_content.replace("<insert-example-facts-to-communicate>", example_domain.get_facts_to_communicate())
    file_content = file_content.replace("<insert-example-explanation>", example_domain.get_explanation())

    # target domain
    file_content = file_content.replace("<insert-target-domain-name>", target_domain.get_name())
    file_content = file_content.replace("<insert-target-task>", target_domain.get_task())
    
    file_content = file_content.replace("<insert-target-plan>", target_domain.get_plan())
    file_content = file_content.replace("<insert-target-interrupted-action>", target_domain.get_interrupted_action())
    file_content = file_content.replace("<insert-target-human-question>", target_domain.get_question())

    return file_content


# Unstructured LLM Model 
def unstructured_LLM(model_name):
    skeleton_file_path, json_file_path, txt_file_path = get_file_paths(model_name)

    # note that right now, the first human question is hard coded (since no human is observing the robot behavior)
    # human_clarification_question = input("Enter the user clarification: ")

    save_to_json(
        unstructured_LLM_prompt_content(file_path=skeleton_file_path), 
        json_file_path,
        txt_file_path)


# Facts based LLM Model
def facts_based_LLM(model_name):
    skeleton_file_path, json_file_path, txt_file_path = get_file_paths(model_name)

    save_to_json(
        facts_based_LLM_prompt_content(file_path=skeleton_file_path), 
        json_file_path,
        txt_file_path)


def main():
    unstructured_LLM("unstructured_LLM")
    facts_based_LLM("facts_based_LLM")


if __name__ == "__main__":
    main()