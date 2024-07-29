import numpy as np

import pickle
import kinpy as kp

from pathlib import Path

# import torch
# import torch.nn as nn

from openai import OpenAI
import os

def generate_plan(prompt):
    key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(
        api_key = key,
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": prompt},
            {"role": "user",
             "content": """The desired output is\"Robot plan: [fetch and bring water to human]\" """}
        ]
    )

    response = completion.choices[0].message

    formatted_response = response.content

    return formatted_response


def generate_baseline_explanation(prompt):
    key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(
        api_key = key,
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": prompt},
            {"role": "user",
             "content": """Provide the most likely source for the human's confusion (only one):<source> """}
        ]
    )

    response = completion.choices[0].message
    return response


def obtain_initial_plan():
    initial_prompt = '''Setting: A robot is assisting a person in day-to-day tasks in the home. Task Representation: The robot must perform the following task: assist the human in doing the dishes. 

        The robot has the following actions available to it: [identify dishes on counter, load the dishwasher, unload the 
        dishwasher, put soap in the dishwasher, open dishwasher, close dishwasher, start dishwasher]. Only use those actions. 
        If they are not sufficient, be clear about which actions need to be added.  
        Generate a plan only using the actions available for how the robot should accomplish this task.  

         An example prompt is: \"Setting: A robot is assisting a person in getting water. 
         Task Representation: The robot must perform the following task: help the person get water. 
         The robot has the following actions available to it: [remind the human to take vitamin, remind human to eat, 
         fetch and bring water to human, fetch and bring coffee to human].\"    


        '''

    robot_initial_plan = generate_plan(initial_prompt)

    # Formatting output
    robot_initial_plan_formatted = robot_initial_plan.split("Task Plan:")[-1]
    robot_initial_plan_formatted = robot_initial_plan_formatted.replace("Robot Plan: ", "My plan is to: ")
    robot_initial_plan_formatted = robot_initial_plan_formatted.replace("Robot plan: ", "My plan is to: ")

    return robot_initial_plan_formatted


def obtain_model_explanation(message):
    human_clarification_prompt = f'''
    The robot carried out this plan. As the robot was loading the dishwasher, 
    the human asked the following question: \"{message}\"
    '''

    source_of_confusion = generate_baseline_explanation(human_clarification_prompt)

    # Formatting result
    source_of_confusion_formatted = source_of_confusion.content

    return source_of_confusion_formatted


# if __name__ == '__main__':
#     initial_prompt = '''Setting: A robot is assisting a person in day-to-day tasks in the home. Task Representation: The robot must perform the following task: assist the human in doing the dishes. 

#         The robot has the following actions available to it: [identify dishes on counter, load the dishwasher, unload the 
#         dishwasher, put soap in the dishwasher, open dishwasher, close dishwasher, start dishwasher]. Only use those actions. 
#         If they are not sufficient, be clear about which actions need to be added.  
#         Generate a plan only using the actions available for how the robot should accomplish this task.  

#          An example prompt is: \"Setting: A robot is assisting a person in getting water. 
#          Task Representation: The robot must perform the following task: help the person get water. 
#          The robot has the following actions available to it: [remind the human to take vitamin, remind human to eat, 
#          fetch and bring water to human, fetch and bring coffee to human].\"    


#         '''

#     robot_initial_plan = generate_plan(initial_prompt)

#     print("Robot initial plan: ", robot_initial_plan)
#     human_clarification_question = input("Enter the user clarification: ")

#     human_clarification_prompt = f'''
#     The robot carried out this plan. As the robot was loading the dishwasher, 
#     the human asked the following question: \"{human_clarification_question}\"
#     '''

#     source_of_confusion = generate_baseline_explanation(human_clarification_prompt)
#     print("Source of confusion: ", source_of_confusion)

#     print("Done.")