from flask import Flask, request
import time
import basicFunctions




app = Flask(__name__)


studyId = 0

studies_DATA_Requested = {}
studies_DATA_Received = {}
studies_hashes = []

@app.route("/")
def hello():
	return "<h1>Home Page</h1>"

@app.route("/researchRequest", methods=['POST'])
def processResearchJson():
	global studyId

	data = request.get_json()

	timeStamp = time.time()	# Record the timestamp of the request

	attributeValues = []	# X values
	attributeKeys = []	# X keys
	datapointValues = [] # Y values
	datapointKeys = [] # Y keys

	for k in data["X"]:
		attributeValues.append(data["X"][k])
		attributeKeys.append(k)

	for k in data["Y"]:
		datapointValues.append(data["Y"][k])
		datapointKeys.append(k)

	remoteHash = basicFunctions.getSha256(attributeValues)
	studies_hashes.append(remoteHash)

	studies_DATA_Requested[studyId] = {}

	# studies_DATA_Requested[studyId]["ID"] = studyId
	studies_DATA_Requested[studyId]["University"] = data["University"]
	studies_DATA_Requested[studyId]["Timestamp"] = timeStamp
	studies_DATA_Requested[studyId]["Hash"] = remoteHash
	studies_DATA_Requested[studyId]["X"] = []
	studies_DATA_Requested[studyId]["Y"] = []

	for k in attributeKeys:
		studies_DATA_Requested[studyId]['X'].append(k)
	for k in datapointKeys:
		studies_DATA_Requested[studyId]['Y'].append(k)

	studyId += 1

	return "DONE"

@app.route("/mobileRequest", methods = ['POST'])
def processMobileJson():
	data = request.get_json()


	attributeValues = []	# X values
	attributeKeys = []	# X keys
	datapointValues = []	# Y values
	datapointKeys = [] # Y keys


	for k in data["X"]:
		attributeValues.append(data["X"][k])
		attributeKeys.append(k)

	for k in data["Y"]:
		datapointValues.append(data["Y"][k])
		datapointKeys.append(k)

	localHash = basicFunctions.getSha256(attributeValues)

	currentID = data["ID"]
	if (len(studies_hashes) > currentID and localHash == studies_hashes[currentID]):
		studies_DATA_Received[currentID] = data["Y"]

	return "DONE"


@app.route("/studiesRequest", methods = ['POST'])
def sendStudies():
	return studies_DATA_Requested

if __name__ == '__main__':
	app.run(debug=True)

