def get_name():
    name = "load_dishes"
    return name

def get_task():
    task = "The robot must assist the human in doing the dishes. "
    return task

# actions the robot has to begin with
def get_actions():
    actions = "[identify dishes on counter, load the dishwasher, unload the dishwasher, put soap in the dishwasher, open dishwasher, close dishwasher, start dishwasher]"
    return actions

def get_explanation():
    explanation = "The actions provided are sufficient to accomplish the task."
    return explanation

def get_plan():
    plan = f"Suggested Plan: [open dishwasher, identify dishes on counter, load the dishwasher, put soap in the dishwasher,close dishwasher, start dishwasher].\n Explanation: f{get_explanation()}"
    return plan

def get_interrupted_action():
    action = "loading the dishwasher"
    return action