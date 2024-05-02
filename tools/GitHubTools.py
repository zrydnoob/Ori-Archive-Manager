import requests
import requests.packages


def getRepoCommits(repo):
    url = f"https://api.github.com/repos/{repo}/commits"
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, verify=False)
    release_info = response.json()
    return release_info


def getLastCommit(repo):
    return getRepoCommits(repo)[0]
