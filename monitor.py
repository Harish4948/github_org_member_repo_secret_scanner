import os
import requests
import time
from tqdm import tqdm
import subprocess

def get_org_public_repos(org_name):
    #GET ORG public repos
    api_url = f"https://api.github.com/orgs/{org_name}/repos"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_PAT')}",}
    repos = []
    page_num = 1
    while True:
        response = requests.get(api_url + f"?per_page=100&page={page_num}&type=public", headers=headers)
        if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers and int(response.headers['X-RateLimit-Remaining']) == 0:
            raise Exception("GitHub rate limit exceeded")
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve public repos for {org_name}. Status code: {response.status_code}")
        org_data = response.json()
        repos.extend([repo["html_url"] for repo in org_data])
        if len(org_data) < 100:
            break
        page_num += 1
    return repos

def get_org_members(org_name):
    api_url = f"https://api.github.com/orgs/{org_name}/members"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_PAT')}",
    }
    members = []
    page_num = 1
    while True:
        response = requests.get(api_url + f"?per_page=100&page={page_num}", headers=headers)
        if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers and int(response.headers['X-RateLimit-Remaining']) == 0:
            raise Exception("GitHub rate limit exceeded")
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve members for {org_name}. Status code: {response.status_code}")
        members_data = response.json()
        members.extend([member["login"] for member in members_data])
        if len(members_data) < 100:
            break
        page_num += 1
    return members

def get_members_repos(org_name, retrieved_members=set()):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_PAT')}",
    }
    members = get_org_members(org_name)
    repositories = []
    for member in members:
        if member in retrieved_members:
            print("Skipping member since already scanned"+member)
            continue
        api_url = f"https://api.github.com/users/{member}/repos?type=owner"
        page_number = 1
        print("Scanning User: "+member)
        while True:
            params = {"type": "owner", "per_page": 100, "page": page_number}
            response = requests.get(api_url, headers=headers, params=params)
            repos = response.json()
            if not repos:
                break
            repositories.extend([repo["html_url"] for repo in repos])
            page_number += 1
        retrieved_members.add(member)
    return repositories, retrieved_members

def write_to_file(filename, items):
    with open(filename, "w") as f:
        f.write("\n".join(items))
def read_from_file(filename):
    with open(filename, "r") as f:
        items = f.read().splitlines()
    return items

def main(org_names):
    scan_number = 0
    while True:
        retrieved_members = set()
        scan_number += 1
        print(f"Scan Number: {scan_number}")
        new_repos = []
        start_time = time.time()
        for org_name in org_names:
            print("Scanning Org: "+org_name)
            org_repos = get_org_public_repos(org_name)
            member_repos, retrieved_members = get_members_repos(org_name, retrieved_members)
            all_repos = org_repos + member_repos
            repositories = read_from_file(os.getcwd()+"/repositories.txt")
            for repo in all_repos:
                if repo not in repositories:
                    new_repos.append(repo)
                    repositories.append(repo)
            write_to_file(os.getcwd()+"/repositories.txt", repositories)
        if new_repos:
            print(f"New Repositories Found: {len(new_repos)}")
            # Save new results to new_repos.txt
            print(new_repos)
            write_to_file(os.getcwd()+"/new_repos.txt", new_repos)
            # Invoke the secret scanning script asynchronously.
            scan_command = ["/bin/bash", "scanner.sh"]
            process = subprocess.Popen(scan_command)
        else:
            print("No New Repositories found")
        elapsed_time = time.time() - start_time
        print(f"Time taken for scan: {elapsed_time:.2f} seconds")
        # Display progress bar
        print("scan_completed")
        for i in tqdm(range(500), desc="Next scan in "):
            time.sleep(1)

if __name__ == "__main__":
    org_names = ["regentmarkets","binary-com"]
    main(org_names)
