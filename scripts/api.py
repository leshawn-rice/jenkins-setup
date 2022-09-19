import re
import requests
import sys


class JenkinsAPI():
    def __init__(self, username: str = None, password: str = None, jenkins_url: str = None) -> None:
        self.username = username
        self.password = password
        self.BASE_URL = jenkins_url if jenkins_url else "http://localhost:8080"
        self.create_session()

    def create_session(self):
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)

    def get_jenkins_crumb(self, endpoint):
        url = self.BASE_URL + endpoint
        response = self.session.get(url)

        if not response.ok:
            sys.exit("HTTP error {} while accessing Jenkins at {}. Exiting.".format(
                response.status_code, url))

        re_match = re.search(r'.*data-crumb-value="(.*)".*', response.text)

        if not re_match:
            sys.exit("Couldn't get required Jenkins-Crumb. Exiting.")

        self.jenkins_crumb = re_match.group(1)

    def get(self, endpoint):
        url = self.BASE_URL + endpoint

        data = {"Jenkins-Crumb": self.jenkins_crumb}

        if self.jenkins_crumb:
            response = self.session.get(url, params=data)
        else:
            response = self.session.get(url)

        return response

    def post(self, endpoint: str = '', body: dict = None):
        url = self.BASE_URL + endpoint

        if not self.jenkins_crumb:
            sys.exit("Jenkins-Crumb required. Exiting")

        data = {"Jenkins-Crumb": self.jenkins_crumb}

        if body:
            response = self.session.post(url, params=data, data=body)
        else:
            response = self.session.post(url, params=data)

        return response

    def close_session(self):
        self.session.close()
