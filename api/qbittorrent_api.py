import os
import time
import requests

session = requests.session()

def get_base_url():
    return os.environ.get("BASE_URL", "http://127.0.0.1:8080/api/v2")


def login():
    """
    Log in to the qBittorrent Web UI.
    :return: True if login is successful, False otherwise.
    """

    login_url = f"{get_base_url()}/auth/login"
    print (f"Logging in to {login_url} with username {os.getenv('USERNAME')}")
    
    data = {
        'username': os.getenv('USERNAME'),
        'password': os.getenv('PASSWORD')
    }
    response = session.post(login_url, data=data)

    if response.text.strip() == "Ok.":
        print("Login successful!")
        return True
    else:
        print(f"Login failed: {response.text}")
        return False
    

def list_torrents():
    torrents_url = f"{get_base_url()}/torrents/info"
    response = session.get(torrents_url)
    if not response.ok:
        print(f"Error retrieving torrents: {response.text}")
        return []
    return response.json()
    

def delete_torrent(torrent_name, torrent_hash, delete_files=True):
    """
    Delete a torrent using its hash.
    :param torrent_hash: The unique hash of the torrent to delete.
    :param delete_files: If True, also delete the downloaded data.
    """
    data = {
        "hashes": torrent_hash,
        "deleteFiles": "true" if delete_files else "false",
    }
    delete_url = f"{get_base_url()}/torrents/delete"
    response = session.post(delete_url, data=data)
    if response.ok:
        print("\033[92m" + f"Successfully deleted torrent {torrent_name}" + "\033[0m")
    else:
        print("\033[91m" + f"Failed to delete torrent {torrent_name}: {response.text}" + "\033[0m")