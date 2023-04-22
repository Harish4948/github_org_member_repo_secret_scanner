import os
import requests

def get_org_public_repos(org_name):
    #GET ORG public repos

def get_org_members(org_name):
    # GET AND STORE ORG MEMBERS

def get_members_repos(org_name, retrieved_members=set()):
    #  GET MEMBERS
    #  GET MEMBER REPOS

def write_to_file(filename, items):

def read_from_file(filename):

def main(org_names):
    # GET ORGS IN A LIST, 
    # iTERATE THROUGH ORGS 
    #   call get_org_public_repos
    #   call get_org_member_repos and members
    #   iterate through the repos and compare against previous results if new append to new_repos list and write
    #   