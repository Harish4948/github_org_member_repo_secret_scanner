# GitHub Public Repository Scanner

This tool scans New public repositories of Organization members and Organizations for secrets in almost real time(8 mins)
It retrieves the repos and basically diffs with previous results, these new result are pushed to a secret scanner to scan for secrets and alert the webhooks from notify. The prob with most free/open source solutions is that it takes a long time to scan and hard to scan just the new repos for secrets.

## Usage

1. Set the `GITHUB_PAT` environment variable to a [GitHub Personal Access Token]
2. Modify the `org_names` list in `main` function with the names of the organizations you want to scan.
3. Run the script with `python scanner.py`.

## Requirements

- Python 3.6 or higher
- `requests` library (`pip install requests`)
- `tqdm` library (`pip install tqdm`)
-  Trufflehog
-  Notify from project discovery

# Future Plan
- Implement Monitoring User public repos for new changes and scan them
- Clean up the bash script to better arrange the output and filenames
