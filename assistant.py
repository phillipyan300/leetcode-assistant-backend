import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

APIKEY = os.getenv('OPENAI_API_KEY')


#TODO: Double check this gets reset when I want it to
checkupID = 0

def normalCheckup(problem: str, snapshot: str):
    global checkupID
    checkupID += 1

    client = OpenAI(
        api_key=APIKEY,
    )
    
    print(snapshot)

    #1. First check if there is an error
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a problem determiner for partly finished code. You either say there is a major problem in the code, or there isn't a problem. Note that incomplete code is ok. Code with glaring technical problem is not"},
            {"role": "user", "content": "Here is the problem: " + problem + ". Now this is the current status of the code:" + snapshot + "  If there is an error in the code that has already been written, say Yes. Otherwise, say No"},
        ]
    )
    isError = completion.choices[0].message.content
    print(completion.choices[0].message.content)

    if "No" in isError or "No" in isError :
        return "No Issues"

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
    print(completion.choices[0].message.content)
    raw1 = completion.choices[0].message.content


    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Vaguer is an assistant which makes the given hint more vague."},
            {"role": "user", "content": raw1},
        ]
    )

    print(completion.choices[0].message.content)
    raw2 = completion.choices[0].message.content


    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Mentor is an assistant which rephrases the input to match that of a mentor. Make sure it remains curt and short"},
            {"role": "user", "content": raw2},
        ]
    )

    print(completion.choices[0].message.content)
    raw3 = completion.choices[0].message.content

    return str(raw3)







# Need to be able to store previous question For now skip
def followup():
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