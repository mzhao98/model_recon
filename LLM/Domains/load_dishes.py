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

### Functions used by Facts-Based LLM model ###
def get_facts():
    """
    All-possible facts.
    Used for facts-based models.
    """
        
    facts = """
        fact_1|The dirty dishes need to be loaded in the dishwasher.|1|public\n
        fact_2|The dishes that I have used are dirty.|1|human-private\n
        fact_3|Any dish left on the counter is dirty.|1|robot-private\n
        fact_4|Not all dishes that are left on the counter are dirty.|1|human-private\n
    """
    
    return facts
