from api import JenkinsAPI
import json
import sys

if len(sys.argv) < 2:
    sys.exit("Need admin password!")

user_info = sys.argv[1]

username, password = user_info.split(":")

jenkins = JenkinsAPI(username=username, password=password)
jenkins.get_jenkins_crumb("/me/configure")
body = {"newTokenName": "ld-admin-token"}
response = jenkins.post(
    endpoint="/me/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken", body=body)
token = json.loads(response.text).get("data", {}).get("tokenValue", "")
jenkins.close_session()

print(token)
