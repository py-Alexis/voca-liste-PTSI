import glob
import os
import io
from api.google_drive_api.Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload

# id of voca_list_ptsi folder in the drive
FOLDER_ID = "1GhMbzJhR1Rc2pA4VOHWSr0woy8FdOABv"

# ____________________ Setup the connection with google drive api ___________________

CLIENT_SECRET_FILE = "api/google_drive_api/credential.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]

try:
    drive_service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
except:
    print("no connected")

# ____________________________________________________________________________________


def download_file(file_id, file_name):
    request = drive_service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False

    while not done:
        status, done = downloader.next_chunk()

    fh.seek(0)

    with open(os.path.join("listes", file_name), "wb") as f:
        f.write(fh.read())
        f.close()

    print(f'the "{file_name}" file has finished downloading')

def sync_with_drive():
    # this function download file that are on the drive and not on the computer

    # get the list of file in the drive folder
    drive_content = drive_service.files().list(q=f"'{FOLDER_ID}' in parents").execute()
    # get the list of file in the computer folder
    computer_content = glob.glob("listes/*.json")

    # keeps the files basename
    for index, file in enumerate(computer_content):
        computer_content[index] = os.path.basename(file)

    # check if files in drive exist on the computer, if not it upload them in the lites folder on the computer
    for file in drive_content["files"]:
        if file["name"] not in computer_content:
            download_file(file["id"], file["name"])


if __name__ == "__main__":
    try:
        sync_with_drive()
        print("sync finish")
    except:
        print("error")
