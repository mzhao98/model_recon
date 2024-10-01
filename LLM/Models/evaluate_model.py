from query import Conversation, query_and_save
import json


def load_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def evaluate_model(model, results_directory='../Results/'):
    conversation = Conversation()

    ### plan prompt ###
    queryname = "plan_test"

    plan_path = 'Prompts/plan_prompt.json'
    with open(plan_path, 'r') as file:
        plan_data = json.load(file)[0]

    conversation.add_message(str(plan_data['role']), str(plan_data['content']))
    
    success, prompt_answer_dir = query_and_save(conversation, 
                   directory=results_directory, 
                   queryname=queryname, 
                   model=model)
    if not success:
        return False # time limit exceeded 
    
    ### confusion prompt ###
    prompt_answer = load_txt_file(prompt_answer_dir) 
    conversation.add_message("assistant", prompt_answer)

    queryname = "confusion_test"

    confusion_path = 'Prompts/confusion_prompt.json'
    with open(confusion_path, 'r') as file:
        confusion_data = json.load(file)[0]

    conversation.add_message(str(confusion_data['role']), str(confusion_data['content']))

    success, confusion_answer_dir = query_and_save(conversation, 
                   directory=results_directory, 
                   queryname=queryname, 
                   model=model)
    if not success:
        return False # time limit exceeded 
    
    ### explanation prompt ###
    confusion_answer = load_txt_file(confusion_answer_dir) 
    conversation.add_message("assistant", confusion_answer)

    queryname = "explanation_test"

    explanation_path = 'Prompts/explanation_prompt.json'
    with open(explanation_path, 'r') as file:
        explanation_data = json.load(file)[0]

    conversation.add_message(str(explanation_data['role']), str(explanation_data['content']))

    success, _ = query_and_save(conversation, 
                   directory=results_directory, 
                   queryname=queryname, 
                   model=model)
    if not success:
        return False # time limit exceeded 
    else:
        return True


def main():
    evaluate_model(model='gpt-4-turbo')


if __name__ == '__main__':
    main()