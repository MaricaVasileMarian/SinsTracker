import requests
import os
import zipfile
import shutil

GITHUB_API_URL = "https://github.com/MaricaVasileMarian/SinsTracker"
DOWNLOAD_URL = "https://github.com/{owner}/{repo}/archive/refs/tags/{tag}.zip"
VERSION_FILE = "version.txt"
UPDATE_FOLDER = "update_temp"

def get_current_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as f:
            return f.read().strip()
    return "0.0.0"

def get_latest_release_info(owner, repo):
    response = requests.get(GITHUB_API_URL.format(owner=owner, repo=repo))
    response.raise_for_status()
    return response.json()

def download_latest_release(owner, repo, tag):
    url = DOWNLOAD_URL.format(owner=owner, repo=repo, tag=tag)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    os.makedirs(UPDATE_FOLDER, exist_ok=True)
    zip_path = os.path.join(UPDATE_FOLDER, f"{repo}-{tag}.zip")
    
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(UPDATE_FOLDER)

def update_application():
    for item in os.listdir(UPDATE_FOLDER):
        s = os.path.join(UPDATE_FOLDER, item)
        d = os.path.join(".", item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    shutil.rmtree(UPDATE_FOLDER)

def check_for_updates(app):
    owner = "your_github_username"
    repo = "your_repo_name"
    
    try:
        current_version = get_current_version()
        release_info = get_latest_release_info(owner, repo)
        latest_version = release_info['tag_name']
        
        if latest_version > current_version:
            download_latest_release(owner, repo, latest_version)
            update_application()
            with open(VERSION_FILE, 'w') as f:
                f.write(latest_version)
            app.update_ui_after_download()
            print("Application updated to version", latest_version)
        else:
            print("No updates available. You are using the latest version.")
    except Exception as e:
        print("Failed to check for updates:", e)
