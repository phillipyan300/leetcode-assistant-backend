from flask import Flask, request, jsonify
import subprocess
from flask_cors import CORS
import json
from assistant import normalCheckup
import os
from werkzeug.utils import secure_filename


# ”
import ast
# Notes: 
# Just check to make sure that multiline strings actually work

app = Flask(__name__)

#CORS stuff
CORS(app, resources={r"/*": {"origins": "*"}}, methods=['POST','GET'])

PROBLEMMAP= {
        "Contains_Duplicate": "Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.",
        "Valid_Anagram": "Given two strings s and t, return true if t is an anagram of s, and false otherwise.\nAn Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "Two_Sum": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "Group_Anagrams": "Given an array of strings strs, group the anagrams together. You can return the answer in any order.\nAn Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "Top_K_Frequent_Elements": "Given an integer array nums and an integer k, return the k most frequent elements."
        }

@app.route("/get_question_<string:question>", methods=["GET", "POST"])
def get_question(question):
    #rudimentary database
    if question in PROBLEMMAP:
        print(jsonify(PROBLEMMAP[question]))
        return jsonify(PROBLEMMAP[question])


# NEED TWO_SUM
# Expects json with fields: code: "code ", language:"language" problem:"problem"
@app.route("/test_code", methods=["POST"])
def test_code():
    print("Testing submitted code: ")

    data = request.get_json()
    raw_code = data.get("code")
    language = data.get("language")
    problem = data.get("problem")

    #Skeleton framework for response data, will add more later
    # Tests has a list of parameters
    response_data = {
        "Overall Success": False,
        "Test Results": [], 
    }
    # No submission = return nothing inputed
    if not raw_code:
        return jsonify(response_data)
    if raw_code:

        #Basic safety check, but only for python
        if "os" in raw_code:
            response_data["Warnings"]["Unsafe"] = "Potentially Dangerous and Unsafe Code Detected."
            return jsonify(response_data)

        #Get tests
        file_path = "tests.json"
        with open(file_path, 'r') as file:
            testsFile = json.load(file)
        testList = testsFile["programs"][problem]["tests"]

        #Add this line at the end of user code to actually run it
        templateAddToRun =  testsFile["programs"][problem]["toTest"]

        #This is to check to make sure that nothing fails. 
        noFails = True
        for test in testList:
            if test["visible"] != 1:
                continue
            # Add an entry for this test in the return package
            response_data["Test Results"].append({})
            testDict = response_data["Test Results"][-1]

            #Use template to create the running line
            # If you need it exactly without the *, but as individual arguments in the function call:
            params_str = ", ".join(map(str, test['parameters']))
            addToRun = f"\nprint({templateAddToRun}({params_str}))"
            codeToRun = raw_code + addToRun
            print(codeToRun)
            
            # Now run it with subprocess. For now just for python
            result = subprocess.run([language, '-c', codeToRun], capture_output=True, text=True)

            #Strip std out of new lines of tabs and turn it into a list
            result.stdout = result.stdout.strip()

            # Check for errors
            if result.stderr:
                noFails = False
                testDict["Success"] = False
            
            #Wrong answer
            # First stringify each of the possible output so it is standardized with result.stdout output
            # tempList = []
            # for potentialAnswer in test["output"]:
            #     # print("stringify")
            #     # print(str(potentialAnswer))
            #     tempList.append(str(potentialAnswer))
            # stringifiedOutput = tempList

            if result.stdout != str(test["output"]):
                # print("wrong answer")
                # print(type(test["output"]))
                # print(test["output"])
                # print(result.stdout)
                # print(type(result.stdout))
                # print("end")
                noFails = False
                testDict["Success"] = False
            else:
                testDict["Success"] = True
            testDict["Output"] = result.stdout
            testDict["Expected Output"] = str(test["output"])
            testDict["Error"] = result.stderr
            testDict["Test Case"] = str(test['parameters'])
                
            print(result.stdout)
            
        if noFails:
            response_data["Overall Success"] = True
        print(response_data)
        return jsonify(response_data)
        
@app.route("/cycle_help", methods=["POST"])
def cycle_help():
    data = request.get_json()
    problem = data.get("problem")
    #The actual problem
    problemStatement = PROBLEMMAP[problem]
    raw_code = data.get("code")

    print(raw_code)

    clue = normalCheckup(problemStatement, raw_code)

    if clue == "No Issues":
        retDict = {"response": "No Issues"}
        return jsonify(retDict)
    print(f"The clue is: {clue}")
    retDict = {"response": clue}
    return jsonify(retDict)


CORS(app, resources={r"/*": {"origins": "*"}}, methods=['POST','GET'])


# Takes in audio recording and submitted answer
# Returns report card for this problem (include a graph with char count?)
@app.route("/submit", methods=["POST"])
def submit():
    print(request)
    print(request.files)
    print(request.form)
    print(request.data)
    # if 'file' not in request.files:
    #     print("no audio")
    #     return jsonify({"error": "No audio part"}), 400

    print("received")
    audio_file = request.files['file']
    filename = secure_filename(audio_file.filename)

    file_size = audio_file.content_length
    print(file_size)

    audio_file_path = os.path.join("./audioTests", filename)
    audio_file.save(audio_file_path)
    return jsonify("test")













if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
