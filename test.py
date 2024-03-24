import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

APIKEY = os.getenv('OPENAI_API_KEY')


client = OpenAI(
        api_key=APIKEY,
    )

voiceToText = "Okay, so for this problem, you can see that the goal is to find two numbers that add up to a target value. So what we're doing here is first create a hash map, which we will use when we iterate through all the values in array. Every time we see a value, we put it in a hash map, and every time we see a value, we also check if that in a value, plus a previously seen value in a hash map equals to a target value. Then we return the two indices. This way, we can cut down the runtime from old n squared to old n."
code = """
def twoSum(self, nums: List[int], target: int) -> List[int]:
    hashmap = {}
    for index, num in enumerate(nums):
        find = target - num
        if find in hashmap:
            return [hashmap[find], index]
        hashmap[num] = index
"""

#1. First check if there is an error
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a comparer. You compare a decription with the actual code. how accurate is it?"},
        {"role": "user", "content": f"Code: {code}, description: {voiceToText}"},
    ]
)
print(completion.choices[0].message.content)
