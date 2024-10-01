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


def CoT_first_call(conversation, model, results_directory, queryname, plan_path):
    with open(plan_path, 'r') as file:
        plan_data = json.load(file)[0]

    conversation.add_message(str(plan_data['role']), str(plan_data['content']))
    
    success, prompt_answer_dir = query_and_save(conversation, 
                   directory=results_directory, 
                   queryname=queryname, 
                   model=model)
    
    return conversation, success, prompt_answer_dir


def CoT_subsequent_calls(conversation, model, results_directory, prompt_answer_dir, queryname, plan_path):

    prompt_answer = load_txt_file(prompt_answer_dir) 
    conversation.add_message("assistant", prompt_answer)

    with open(plan_path, 'r') as file:
        plan_data = json.load(file)[0]

    conversation.add_message(str(plan_data['role']), str(plan_data['content']))
    
    success, prompt_answer_dir = query_and_save(conversation, 
                   directory=results_directory, 
                   queryname=queryname, 
                   model=model)
    
    return conversation, success, prompt_answer_dir


def unstructured_LLM(model, results_directory):
    print("\n*** Unstructured LLM Model ***\n")
    conversation = Conversation()
    
    ### confusion prompt ###
    conversation, success, _ = CoT_first_call(
        conversation, 
        model, 
        results_directory, 
        queryname="test_unstructured_LLM", 
        plan_path='Prompts/unstructured_LLM_prompt.json'
    )

    if not success:
        return False # time limit exceeded 
    else:
        return True


def facts_based_LLM(model, results_directory):
    print("\n*** Facts-based LLM Model ***\n")

    conversation = Conversation()

    ### plan prompt ###
    conversation, success, all_facts_prompt_answer_dir = CoT_first_call(
        conversation, 
        model, 
        results_directory, 
        queryname="test_facts_based_LLM", 
        plan_path='Prompts/facts_based_LLM_prompt.json'
    )

    if not success:
        return False # time limit exceeded 
    else:
        return True


def main():
    gpt_model = 'gpt-4-turbo'
    results_dir = '../Results/'

    unstructured_LLM(model=gpt_model, results_directory=results_dir)
    facts_based_LLM(model=gpt_model, results_directory=results_dir)


if __name__ == '__main__':
    main()

    # TODO could have chain of thought in one json (but need to plug in model's answer)
    # TODO (assistant vs user vs system)