def get_name():
    name = "get_water"
    return name

def get_task():
    task = "The robot must must assist the human in getting them a glass of water."
    return task

# actions the robot has to begin with
def get_actions():
    actions = "[remind the human to take vitamin, remind human to eat, bring water to human, bring coffee to human]"
    return actions

def get_explanation():
    explanation = "The robot is missing the action `get glass of water` and the action `fill glass of water`. Without these actions, the robot cannot bring a glass of water to the human."
    return explanation

def get_plan():
    plan = f"Suggested Plan: [get glass of water, fill glass of water, bring water to human].\n Explanation: f{get_explanation()}"
    return plan