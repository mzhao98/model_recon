### Functions used by all models, returning information about the domain, task, and interaction ###
def get_name():
    """
    Domain name.
    Used for all models.
    """
        
    name = "get_water"
    return name

def get_task():
    """
    Task discription.
    Used for all models.
    """
        
    task = "The robot must must assist the human in getting them a glass of water."
    return task

def get_plan():
    """
    Plan of actions, along with explanation of the actions in the plan.
    Used for all models.
    """
    
    plan = f"Suggested Plan: [get glass of water, fill glass of water, bring water to human]."
    return plan

def get_interrupted_action():
    """
    Action that was being taken when the human asked the question.
    Used for all models.
    """
        
    action = "fill glass of water"
    return action

def get_question():
    """
    Return human question.
    Used for all models.
    """

    question = "Why did you get me water from the sink?"
    return question

### Functions used by Unstructured LLM model ###
def get_actions():
    """
    Actions the robot the ability to do, to begin with
    Used for Unstructured LLM model.
    """
        
    actions = "[remind the human to take vitamin, remind human to eat, bring water to human, bring coffee to human]"
    return actions

def get_confusion():
    """
    Identify human confusion.
    Used for unstructured LLM model.
    """
    confusion = "The human is confused about why the water was obtained from the sink when it could have been obtained elsewhere, such as the fridge. This is confusing, as obtaining water from the fridge is prefferable, as it has the attribute of being filtered."
    return confusion

def get_confusion_explanation(): 
    """
    Explanation to address human confusion (for now, same explanation as facts-based explanation).
    Used for unstructured LLM model.
    """
    confusion = get_facts_explanation()
    return confusion

### Functions used by Facts-based LLM model ###

def get_facts():
    """
    Set of all relevant facts, labeled.
    Used for facts-based LLM model.
    """
        
    facts = """
            Water needs to be poured into a glass (public).\n
            Unfiltered water can be found in sink (public).\n
            Filtered water can be found in fridge (private-human).\n
            Filtered water is preffered (private-human).\n
            Task is to bring human a glass of water (public).\n
            Glass must be held without too much force, in order not to break it (private-robot).
        """
    return facts

def get_facts_to_communicate():
    """
    Subset of facts that need to be communicated, given the question.
    Used for facts-based LLM model.
    """

    facts_to_communicate = """
        Filtered water is preffered (private-human).\n
        Filtered water can be found in fridge (private-human).\n
    """
    return facts_to_communicate

def get_facts_explanation():
    """
    Explanation created from facts to be communicated.
    Used for facts-based LLM model.
    """
    facts_explanation = "I provided water from the sink, but from your question I now understand that you would like water from the fridge. I believe that this is because water from the fridge is filtered and you preffer filtered water."
    return facts_explanation