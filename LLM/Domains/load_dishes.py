### Functions used by all models, returning information about the domain, task, and interaction ###
def get_name():
    """
    Domain name.
    Used for all models.
    """
        
    name = "load_dishes"
    return name

def get_task():
    """
    Task discription.
    Used for all models.
    """

    task = "The robot must assist the human in doing the dishes. "
    return task

def get_plan():
    """
    Plan of actions, along with explanation of the actions in the plan.
    Used for all models.
    """

    plan = f"Suggested Plan: [open dishwasher, identify dishes on counter, load the dishwasher, put soap in the dishwasher, close dishwasher, start dishwasher]."
    return plan

def get_interrupted_action():
    """
    Action that was being taken when the human asked the question.
    Used for all models.
    """
        
    action = "loading the dishwasher"
    return action

def get_question():
    """
    Return human question.
    Used for all models.
    """

    question = "Why did you load a clean plate into the dishwasher?"
    return question

### Functions used by Unstructured LLM model ###
def get_actions():
    """
    Action that was being taken when the human asked the question.
    Used for all models.
    """

    actions = "[identify dishes on counter, load the dishwasher, unload the dishwasher, put soap in the dishwasher, open dishwasher, close dishwasher, start dishwasher]"
    return actions