### Contrastive Explanations ###
def get_contrastive_explanation():
    contrastive_explanation = "if the human asks you a Why question, identify the fact (what happened), and it's implicit foil (human expectation). Then, in your explanation, incorporate both fact and foil."
    return contrastive_explanation

def get_non_contrastive_explanation():
    non_contrastive_explanation = "if the human asks you a Why question, identify the fact (what happened). Then, in your explanation, incorporate that fact."
    return non_contrastive_explanation