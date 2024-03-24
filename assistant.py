import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

APIKEY = os.getenv('OPENAI_API_KEY')


checkupID = 0

#Both syntax and logic suggestion
def normalCheckup(problem: str, snapshot: str):
    global checkupID


    #Starts at 1 and clears the page
    if checkupID == 0:
        file_path = "./assistantLog.json"
        with open(file_path, 'w') as file:
            json.dump([], file)
    

    client = OpenAI(
        api_key=APIKEY,
    )
    
    #print(snapshot)

    #1. First check if there is an error
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a problem determiner for partly finished code. You either say there is a major problem in the code, or there isn't a problem. Note that incomplete code is ok. Code with glaring technical problem is not"},
            {"role": "user", "content": "Here is the problem: " + problem + ". Now this is the current status of the code:" + snapshot + "  If there is an error in the code say Yes. Pay specific attention to braces mismatches. Otherwise, say No."},
        ]
    )
    isError = completion.choices[0].message.content
    print(completion.choices[0].message.content)
    # Technically don't even need this line?
    if "No" in isError or "No" in isError :
        syntaxSuggestion = ""
        print("No issues")
    else:

        #Each of these api calls does exactly one thing; keeps it consistant and controllable
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Real Time Assistant is coding assistant specifically designed to provide hints and help for learners on algorithm problems. The main goal is to hint, not directly address any issues the user might have"},
                {"role": "user", "content": "Here is the problem: " + problem + ". Now this is the current status of the code:" + snapshot + " Do you see any errors? If so, give a light hint including the line number. If not, return True. Omit the first sentence you generate"},
            ]
        )

        # Print the assistant's response
        #print(completion)
        #print(completion.choices[0].message.content)
        raw1 = completion.choices[0].message.content


        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Vaguer is an assistant which makes the given hint more vague."},
                {"role": "user", "content": raw1},
            ]
        )

        #print(completion.choices[0].message.content)
        raw2 = completion.choices[0].message.content


        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Mentor is an assistant which rephrases the input to match that of a mentor. Make sure it remains curt and short"},
                {"role": "user", "content": raw2},
            ]
        )

        print(completion.choices[0].message.content)
        syntaxSuggestion = completion.choices[0].message.content


    #Now onto logic errors
    #1. First check if there is an error
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a problem determiner for partly finished code. You spot any mistakes in logic or confused code, like when the wrong variable is used. Make sure to rigorously compare the user inputted code with the problem statement, and identify mistakes "},
            {"role": "user", "content": "Here is the problem: " + problem + ". Now this is the current status of user code:" + snapshot + " Do you see any logic issues? This could be using the wrong variable which would cause the program to fail. Pay special attention to target "},
        ]
    )
    theMistake = completion.choices[0].message.content
    print(theMistake)

    #2. Now make this mistake into a hint
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a hint maker. you take in a mistake, and you find the best way to rephrase the provided mistake and solution into a hint. Think of your audience as being a student who is learning to code. "},
            {"role": "user", "content": "Give a hint which encapsulates this problem and hints towards the solution: " + theMistake},
        ]
    )

    rawHint = completion.choices[0].message.content
    print(rawHint)


    #2. Now make this hint vaguer
    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a hint editor. You are given hints that reveal the solution "},
    #         {"role": "user", "content": "Edit this hint to make sure not to reveal the solution " + rawHint + " If it does not reveal the solution then leave it as it is."},
    #     ]
    # )

    logicSuggestion = completion.choices[0].message.content
    print(logicSuggestion)

    if logicSuggestion:
        suggestion = logicSuggestion

    else:
        suggestion = syntaxSuggestion

    if isError == "No Issues":
        return "No Issues"





    print("Logging now")
    print(checkupID)
    # LOGGING 
    file_path = "./assistantLog.json"

    # If this is the first issue reported (also, this clears the file)


    data = []
    # Read from the file, if it isn't empty (note the two brackets)
    if os.path.exists(file_path) and os.path.getsize(file_path) > 3:
        print("non empty json")
        #If we should add a new entry
        addNew = True
        mostRecentEntry = {}
        with open(file_path, 'r') as file:
            data = json.load(file)
            mostRecentEntry = data[-1]
            #The user has been stuck on the same code
            if snapshot == mostRecentEntry["snapshot"]:
                mostRecentEntry["counter"] += 1
                addNew = False

        
        #If the user has been stuck for more than 1 iteration. CAN MODIFY num iterations
        if mostRecentEntry["counter"] > 1:
            # Skip the hint since you don't wnat ot spam the same hint
            print("Skip")
            return "No Issues"

        #New element to add:
        new_entry = {
            "id": checkupID,
            "problem": problem,
            "snapshot": snapshot,
            "advice": suggestion,
            "counter": mostRecentEntry["counter"] + 1
        }

        # This is a unique entry we should add
        if addNew:
            new_entry["counter"] = 0
            data.append(new_entry)
            # Only count as feedback if there are issues AND it is unique
            checkupID += 1
            print("Adding new")
        #Otherwise we just overwrite it
        else:
            data[-1] = new_entry
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            
    # nothing here yet, so will just put this first value
    else:
        print("adding first entry")
        new_entry = {
            "id": checkupID,
            "problem": problem,
            "snapshot": snapshot,
            "advice": suggestion,
            "counter": 1
        }
        data.append(new_entry)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        # Only count as feedback if there are issues AND it is unique
        checkupID += 1

    print("Logging finished")
    
    #Now that it is logged, we return the suggestion
    return str(suggestion)

        





#  Should be able to ask GPT for help if stuck
def giveHint():
    #Suggest an 
    pass


#This should have access to all the questions asked
def summary():
    pass


if __name__ == '__main__':
    problem = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\nYou may assume that each input would have exactly one solution, and you may not use the same element twice."
    snapshot = """
def twoSum(nums: list[int], target: int) -> list[int]:
  hashmap = []
  for index, num in enumerate(nums):
      find = target - num

"""

    normalCheckup(problem, snapshot)