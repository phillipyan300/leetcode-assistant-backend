from flask import Flask, request, jsonify
import subprocess
from flask_cors import CORS
import json
# Notes: 
# Just check to make sure that multiline strings actually work

app = Flask(__name__)

#CORS stuff
CORS(app, resources={r"/*": {"origins": "*"}}, methods=['POST','GET'])


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
        testList = testsFile["programs"]["Two Sum"]["tests"]

        #Add this line at the end of user code to actually run it
        templateAddToRun =  testsFile["programs"]["Two Sum"]["toTest"]

        #This is to check to make sure that nothing fails. 
        noFails = True
        for test in testList:
            # Add an entry for this test in the return package
            response_data["Test Results"].append({})
            testDict = response_data["Test Results"][-1]

            #Use template to create the running line
            addToRun = f"\n {templateAddToRun}({test['parameters']})"
            codeToRun = raw_code + addToRun
            print(codeToRun)
            
            # Now run it with subprocess. For now just for python
            result = subprocess.run([language, '-c', codeToRun], capture_output=True, text=True)

            # Check for errors
            if result.stderr:
                noFails = False
                testDict["Success"] = False
            testDict["Success"] = True
            testDict["Output"] = result.stdout
            testDict["Error"] = result.stderr
                
            print(result.stdout)
            
        if noFails:
            response_data["Overall Success"] = True
        print(response_data)
        return jsonify(response_data)
        
@app.route("/cycle_help", methods=["POST"])
def cycle_help():
    data = request.get_json()
    problem = 2
    raw_code = data.get("code")




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
