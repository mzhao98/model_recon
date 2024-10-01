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


def CoT_first_call(conversation, model, results_directory, queryname, prompt_path):

    # add next conversational input
    with open(prompt_path, 'r') as file:
        plan_data = json.load(file)[0]
    conversation.add_message(str(plan_data['role']), str(plan_data['content']))
    
    # query llm
    success, prompt_answer_dir = query_and_save(conversation, 
                   directory=results_directory, 
                   queryname=queryname, 
                   model=model)
    
    return conversation, success, prompt_answer_dir


def CoT_subsequent_calls(conversation, model, results_directory, prompt_answer_dir, queryname, prompt_path):
    """
    Subsequent calls to model, made without feedback from human.
    Currently unused.
    """

    # add previous conversation content 
    prompt_answer = load_txt_file(prompt_answer_dir) 
    conversation.add_message("assistant", prompt_answer)

    # add next conversational input
    with open(prompt_path, 'r') as file:
        plan_data = json.load(file)[0]
    conversation.add_message(str(plan_data['role']), str(plan_data['content']))
    
    # query llm
    success, prompt_answer_dir = query_and_save(conversation, 
                   directory=results_directory, 
                   queryname=queryname, 
                   model=model)
    
    return conversation, success, prompt_answer_dir


def query_model_with_human_response(conversation, model, results_directory, prompt_answer_dir, queryname, human_response):

    # add previous conversation content 
    prompt_answer = load_txt_file(prompt_answer_dir) 
    conversation.add_message("assistant", prompt_answer)

    # add next conversational input (from human response)
    conversation.add_message("user", human_response)
    
    # query llm
    success, prompt_answer_dir = query_and_save(conversation, 
                   directory=results_directory, 
                   queryname=queryname, 
                   model=model)
    
    return conversation, success, prompt_answer_dir


def query_model(model, results_directory, model_name, bidirectional=0):
    print(f"\n*** {model_name} ***\n")
    conversation = Conversation()
    
    ### confusion prompt ###
    conversation, success, prompt_answer_dir = CoT_first_call(
        conversation, 
        model, 
        results_directory, 
        queryname=f"test_{model_name}", 
        prompt_path=f"Prompts/{model_name}_prompt.json"
    )

    if not success:
        return False # time limit exceeded 
    else:

        if bidirectional:

            print('\n')
            input_message = "\nIf you are satisfied, enter \"approved\", else enter your response.  "

            human_input = input(input_message)

            while "approve" not in human_input:

                human_input_prompt = ""

                with open(f"Prompts/{model_name}_followup_prompt_skeleton.txt", 'r') as file:
                    human_input_prompt = file.read()
                human_input_prompt = human_input_prompt.replace("<insert-human-response>", human_input)

                conversation, success, prompt_answer_dir = query_model_with_human_response(
                    conversation, 
                    model, 
                    results_directory, 
                    prompt_answer_dir,
                    queryname=f"test_{model_name}", # "test_{model_name}_with_human_response_{i}"
                    human_response=human_input
                )
                if not success:
                    return False # time limit exceeded 

                print('\n')
                human_input = input(input_message)
        else:
            return True
    return True


def main():
    gpt_model = 'gpt-4-turbo'
    results_dir = '../Results/'

    for model_name_i in ["unstructured_LLM", "facts_based_LLM"]:
        query_model(model=gpt_model, results_directory=results_dir, model_name=model_name_i, bidirectional=1)


if __name__ == '__main__':
    main()