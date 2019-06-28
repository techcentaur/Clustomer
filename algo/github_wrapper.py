"GitHub Wrapper for File Upload"

import base64
from github import (Github, InputGitTreeElement)
from random import randint

def post_on_github(params):
    """ @params: A dictionary with keys:
        user: GitHub handle,
        password: Password without encryption,
        repo: Name of the repository,
        branch: Name of the branch (default is 'master')
        to_be_uploaded_file_list: List of files to be uploaded,
        commit_message: Message for the commit (default is a random message),
        verbose: Verbose (default False)
    """

    try:
        print("1")
        if params["verbose"]:
            print("[*] Trying to upload file(s) {f} in {r} for handle {h}".format(f=params["to_be_uploaded_file_list"], r=params["repo"], h=params["user"]))

        g = Github(params["user"], params["password"])
        print("2")

        repo = g.get_user().get_repo(params["repo"])
        file_list = params["to_be_uploaded_file_list"]
        print("3")

        file_names = [x.rsplit("/", 1)[1] for x in file_list]
        if params["commit_message"] is None:
            commit_message = 'KML-file update {}'.format(randint(0, 100)*randint(0,100)/randint(1, 100))
        else:
            commit_message = params["commit_message"]
        print("4")

        master_ref = repo.get_git_ref('heads/'+str(params["branch"]))
        master_sha = master_ref.object.sha
        base_tree = repo.get_git_tree(master_sha)
        print("5")

        element_list = list()
        for i, entry in enumerate(file_list):
            with open(entry) as input_file:
                data = input_file.read()
            element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
            element_list.append(element)
        print("6")

        tree = repo.create_git_tree(element_list, base_tree)
        parent = repo.get_git_commit(master_sha)

        commit = repo.create_git_commit(commit_message, tree, [parent])
        master_ref.edit(commit.sha)
    except Exception as e:
        print("Exception: {}".format(e))
        return False

    if params["verbose"]:
        print("[*] Uploading successful!")

    return True
