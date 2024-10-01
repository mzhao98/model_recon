# model_recon

Run `LLM/Models/unstructured_LLM.py` to generate the seperate CoT prompts for that model. 

Those prompts are structured using the txt skeleton files in `LLM/Models/Prompts` and finalized (with info filled in from `LLM/Domains`) in the json files  in `LLM/Models/Prompts`.

Then, run `LLM/Models/evaluate_model.py` to prompt the model (specified in main) the these CoT prompts.