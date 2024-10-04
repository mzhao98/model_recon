import sys
sys.path.append("..")

class FactModel:
    def __init__(self, name, LLM_path):
        """
        Initializes the FactManager with paths to files for facts, 
        and the mutually inclusive/exclusive relational sets. 
        """
        self.name = name
        self.facts = {}
        # self.facts_path = f'{domain_path}facts.txt'
        # self.must_agree_path = f'{domain_path}must_agree.txt'
        # self.must_disagree_path = f'{domain_path}must_disagree.txt'
        self.LLM_fact_relations_path = f'{LLM_path}test_fact_relationship-gpt-4-turbo.txt'
        self.check_consistency = 1

        # self.load_facts_from_file()
        self.load_facts_from_domain_function()

    def populate_fact(self, fact_name, statement, confidence, visibility_status):
        """
        Populates a fact by adding it to the `facts` dictionary, with 
        details including its statement, confidence, and visibility.
        """

        fact_content = {
            'statement': statement,
            'confidence': confidence,
            'visibility': visibility_status
        }


        if self.check_consistency:
            valid_addition, inconsistent_facts = self.check_fact_consistency(fact_name, fact_content)
            self.inconsistent_facts = inconsistent_facts
            
            if not valid_addition:
                self.resolve_inconsistency(fact_name, fact_content)

            self.facts[fact_name] = fact_content
        else:
            self.facts[fact_name] = fact_content

    def resolve_inconsistency(self, new_fact_name, new_fact_content):
        """
        Prompts the human to decide how to resolve inconsistencies when adding a new fact.
        Options are: 
        1) The new fact is right, so update existing inconsistent facts.
        2) The new fact is wrong and should be updated.
        3) Allow the inconsistency to exist.
        """
        print(f"\nInconsistency detected when adding new fact, '{new_fact_name}'.")
        print(f"  Name: {new_fact_name}")
        print(f"    Statement: {new_fact_content['statement']}")
        print(f"    Confidence: {new_fact_content['confidence']}")
        print(f"    Visibility: {new_fact_content['visibility']}")
        
        print("\nInconsistent, pre-existing facts:", self.inconsistent_facts)
        for fact in self.inconsistent_facts:
            if fact in self.facts:
                fact_details = self.facts[fact]
                print(f"  Name: {fact}")
                print(f"    Statement: {fact_details['statement']}")
                print(f"    Confidence: {fact_details['confidence']}")
                print(f"    Visibility: {fact_details['visibility']}")
            else:
                print(f"  Name: {fact} (not found in existing facts)")
        
        print("\nPlease choose an option:")
        print("1: The new fact is correct. Update inconsistent facts.")
        print("2: The new fact is incorrect. Update it accordingly.")
        print("3: These facts are not inconsistent.")

        choice = input("\nEnter your choice (1, 2, or 3): ")

        if choice == '1':
            # Update existing inconsistent facts with the new fact content
            for fact in self.inconsistent_facts:
                updated_confidence = int(input("Enter new confidence level for the existing, conflicting fact: "))
                self.modify_fact(fact,confidence=updated_confidence)
            print(f"Updated '{fact}' with new confidence level.")

        elif choice == '2':
            updated_confidence = int(input("Enter new confidence level for the new fact: "))
            new_fact_content['confidence'] = updated_confidence
            print(f"Updated '{new_fact_name}' with new confidence level.")

        elif choice == '3':
            print("inconsistent facts: ", self.inconsistent_facts)
            for fact in self.inconsistent_facts:
                self.remove_fact_from_relational_sets(fact)  # Remove from relational sets
            self.remove_fact_from_relational_sets(new_fact_name)  # Remove from relational sets
            print("inconsistent facts: ", self.inconsistent_facts)
            
            print(f"Removed this pair of facts from the inconsistent_facts set (they are allowed to co-exist).")

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    def add_fact(self, fact_string):
        """
        Adds a fact to the facts dictionary from a string formatted as:
        "fact_name|statement|confidence|visibility"
        """
        fact_name, statement, confidence, visibility = fact_string.split('|')
        confidence = int(confidence)  # Ensure confidence is an integer
        visibility_status = {visibility.strip()}  # Convert visibility to a set

        visibility_check = sum([self.name in visibility_status_i for visibility_status_i in visibility_status])

        if ('public' in visibility_status) or visibility_check:
            self.populate_fact(fact_name, statement, confidence, visibility_status)

    def load_facts_from_file(self):
        """
        Loads the initial set of facts from a text file and populates the facts dictionary.
        Each line in the file should be formatted as: name|statement|confidence|visibility.
        """
        with open(self.facts_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    self.add_fact(line)

    def load_facts_from_domain_function(self):
        """
        Loads the initial set of facts from a text file and populates the facts dictionary.
        Each line in the file should be formatted as: name|statement|confidence|visibility.
        """
        lines = import_facts().split('\n')
        for line in lines:
            line = line.strip()
            if line:
                self.add_fact(line)
                        
    def check_fact_consistency(self, new_fact_name, new_fact_content):
        """
        Checks if a new fact is consistent with existing facts by verifying 
        the mutually inclusive and exclusive relationships.
        """
        new_confidence = new_fact_content['confidence']
        inconsistent_facts = []

        must_agree_set, must_disagree_set = self.get_facts_relational_sets(new_fact_name)

        # Check mutually exclusive facts
        for ex_fact_name in must_disagree_set:
            if ex_fact_name in self.facts:
                ex_fact_confidence = self.facts[ex_fact_name]['confidence']
                if ex_fact_confidence == new_confidence:
                    print(f"Conflict: {new_fact_name} and {ex_fact_name} are mutually exclusive but share the same confidence.")
                    inconsistent_facts.append(ex_fact_name)

        # Check mutually inclusive facts
        for in_fact_name in must_agree_set:
            if in_fact_name in self.facts:
                in_fact_confidence = self.facts[in_fact_name]['confidence']
                if in_fact_confidence != new_confidence:
                    print(f"Conflict: {new_fact_name} and {in_fact_name} are mutually inclusive but have different confidences.")
                    inconsistent_facts.append(in_fact_name)
        
        # if inconsistencies exist for this new fact, this new fact is now inconsistent with them, so add it 
        if len(inconsistent_facts) > 0:
            inconsistent_facts.append(new_fact_name)

        return len(inconsistent_facts) == 0, inconsistent_facts

    def modify_fact(self, name, statement=None, confidence=None, visibility_status=None):
        """
        Updates the statement, confidence, or visibility of an existing fact, 
        identified by its name.
        """
        if name in self.facts:
            if statement is not None:
                self.facts[name]['statement'] = statement
            if confidence is not None:
                self.facts[name]['confidence'] = confidence
            if visibility_status is not None:
                self.facts[name]['visibility'] = visibility_status
            return True
        else:
            print(f"Fact {name} does not exist.")
            return False

    def delete_fact(self, name):
        """
        Deletes a fact from the facts dictionary and removes it from any relational sets.
        """
        if name in self.facts:
            self.remove_fact_from_relational_sets(name)
            del self.facts[name]
            return True
        else:
            print(f"Fact {name} does not exist.")
            return False

    def remove_fact_from_relational_sets(self, removed_fact_name):
        """
        Removes a fact from any relational sets that it is part of.
        (Currently unimplemented.)
        """
        self.inconsistent_facts.remove(removed_fact_name)

    def get_facts_relational_sets(self, fact_name):
        """
        Retrieves the mutually inclusive and exclusive sets relevant to a given fact.
        """
        must_agree_sets, must_disagree_sets = self.get_relational_sets()

        relevant_must_agree_set = []
        relevant_must_disagree_set = []

        for must_agree_set in must_agree_sets:
            if fact_name in must_agree_set:
                must_agree_set.remove(fact_name)
                relevant_must_agree_set = must_agree_set

        for must_disagree_set in must_disagree_sets:
            if fact_name in must_disagree_set:
                must_disagree_set.remove(fact_name)
                relevant_must_disagree_set = must_disagree_set

        return relevant_must_agree_set, relevant_must_disagree_set

    def get_relational_sets(self):
        """
        Loads the LLM generated must agree and must disagree set of acts.
        Assuming each line has exactly two facts.
        """
        ### this was to laod from hardcoded must_agree.txt and must_disagree.txt
        # def load_relational_sets(file_path):
        #     relational_sets = []
        #     with open(file_path, 'r') as file:
        #         for line in file:
        #             relational_facts = line.strip().split(',')
        #             relational_facts.sort()  # Optional
        #             relational_sets.append(relational_facts)
        #     return relational_sets

        # must_agree_sets = load_relational_sets(self.must_agree_path)
        # must_disagree_sets = load_relational_sets(self.must_disagree_path)

        ### this is to load from LLM output
        def load_relational_sets(file_path, relationship_type):
            relational_sets = []
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith(relationship_type):
                        facts = line[len(relationship_type):].strip().split(',')
                        if facts:  
                            relational_sets.append(facts)

            if relational_sets == [['']]:
                return []
            return relational_sets

        must_agree_sets = load_relational_sets(self.LLM_fact_relations_path, 'mutually inclusive:')
        must_disagree_sets = load_relational_sets(self.LLM_fact_relations_path, 'mutually exclusive:')

        return must_agree_sets, must_disagree_sets

    def print_model(self):
        """
        Visualize self.facts model
        """
                
        print(f'\n*** {self.name} model ***\n')
        for fact_name in self.facts:
            fact_content = self.facts[fact_name]

            print(fact_name)
            print("    Statement: ", fact_content['statement'])
            print("    Confidence: ", fact_content['confidence'])
            print("    Visibility: ", fact_content['visibility'])


### Load Dishes Fact Logic ###

from Domains.load_dishes import get_facts as import_facts
robot_model = FactModel(name='robot', LLM_path='../Results/')
robot_model.print_model()

# robot_model.delete_fact('fact_2') # delete a fact
# robot_model.modify_fact('fact_3', confidence=0) # change confidence from 0 to 1
# robot_model.add_fact('fact_5|The dishwasher should be filled after the meal.|1|robot-private') # add a new fact
# to change fact relations, please alter load_dishes/must_agree.txt or must_disagree.txt
# robot_model.print_model()

# human_model = FactModel(name='human', domain_path='load_dishes/')
# human_model.print_model()

# TODO have LLM populate facts.txt?
# TODO have LLM populate must_agree and must_disagree.