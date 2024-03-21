import os
import io
import mimetypes
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

from dotenv import load_dotenv

class GoogleDriveManager:
    """
    A class for managing operations with Google Drive API.
    구글 드라이브 API 작업을 관리하는 클래스입니다.
    """
    # 프로젝트 루트 디렉토리, 인증 정보 파일 이름, 토큰 파일 이름 설정
    def __init__(self, project_root_dir, credentials_file_name, token_file_name):
        """
        Initialize GoogleDriveManager with project directory and credential files.
        프로젝트 디렉토리와 자격 증명 파일을 사용하여 GoogleDriveManager를 초기화합니다.
        
        Args:
            project_root_dir (str): The root directory of the project.
            프로젝트의 루트 디렉토리입니다.
            credentials_file_name (str): The file name of the credentials JSON file.
            자격 증명 JSON 파일의 파일 이름입니다.
            token_file_name (str): The file name of the token JSON file.
            토큰 JSON 파일의 파일 이름입니다.
        """
        self.project_root_dir = project_root_dir
        self.credentials_path = os.path.join(project_root_dir, credentials_file_name)
        self.token_path = os.path.join(project_root_dir, token_file_name)
        # Google Drive API 사용을 위한 권한 범위 설정
        self.scopes = [
            "https://www.googleapis.com/auth/drive.metadata.readonly",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        # 사용자 인증 수행
        self.creds = self.authenticate()
    
    # ref:
    # - https://developers.google.com/drive/api/guides/create-file
    # - https://developers.google.com/drive/api/guides/folder
    def create_folder(self, folder_name, parent_id=None):
        """
        Create a folder on Google Drive.
        구글 드라이브에 폴더를 생성합니다.
        
        Args:
            folder_name (str): The name of the folder to be created.
            생성할 폴더의 이름입니다.
            parent_id (str, optional): The parent folder ID. Defaults to None.
            상위 폴더의 ID입니다. 기본값은 None입니다.
        
        Returns:
            str: The ID of the created folder.
            생성된 폴더의 ID입니다.
        """
        service = self.create_service()
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]
        try:
            folder = service.files().create(body=file_metadata, fields='id', supportsAllDrives=True).execute()
            print(f'Folder ID: {folder.get("id")}')
            return folder.get('id')
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
        
    # ref: 
    # - https://developers.google.com/drive/api/guides/manage-uploads
    # - https://developers.google.com/drive/api/guides/manage-sharing // share

    def upload_file(self, file_stream_or_path, file_name, folder_id):
            """
            파일 또는 파일 스트림을 Google 드라이브에 업로드
            Args:
                file_stream_or_path : 업로드 할 파일 스트림 또는 파일 경로.
                file_name (str) : 업로드 할 파일의 이름입니다.
                folder_id (str) : 폴더의 ID로 파일을 업로드 할 수 있습니다.
            Returns:
                str: 업로드 된 파일의 ID.
            """
        service = self.create_service()

        # 파일 경로로부터 업로드하는 경우
        if isinstance(file_stream_or_path, str):
            file_path = file_stream_or_path
            mime_type, _ = mimetypes.guess_type(file_path)
            media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        # Flask의 FileStorage 객체 또는 Django의 UploadedFile 객체일 경우
        elif hasattr(file_stream_or_path, 'read'):
            # MIME 타입을 .content_type 또는 .mimetype 속성에서 가져옵니다.
            mime_type = getattr(file_stream_or_path, 'content_type', 
                                getattr(file_stream_or_path, 'mimetype', 'application/octet-stream'))
            media = MediaIoBaseUpload(file_stream_or_path, mimetype=mime_type, resumable=True)

        # 바이트 스트림 (io.BytesIO 객체)일 경우
        elif isinstance(file_stream_or_path, io.BytesIO):
            mime_type = 'application/octet-stream'  # 이 예시에서는 일반적인 바이너리 타입을 사용합니다.
            media = MediaIoBaseUpload(file_stream_or_path, mimetype=mime_type, resumable=True)

        else:
            raise ValueError("Unsupported file type")

        file_metadata = {'name': file_name, 'parents': [folder_id]}

        try:
            file = service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True).execute()
            return file.get('id')
        except Exception as error:  # 구체적인 예외 유형에 따라 수정할 수 있습니다.
            print(f'An error occurred: {error}')
            return None
    """ Deprecated
    def upload_file(self, file_stream_or_path, file_name, folder_id):

            service = self.create_service()

            # 파일 경로로부터 업로드하는 경우
            if isinstance(file_stream_or_path, str):
                file_path = file_stream_or_path
                mime_type, _ = mimetypes.guess_type(file_path)
                media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
            else:
                # 파일 스트림으로부터 업로드하는 경우
                file_stream = file_stream_or_path
                mime_type = file_stream.content_type  # Flask의 request.files['file'].content_type에서 MIME 타입을 얻을 수 있습니다.
                media = MediaIoBaseUpload(file_stream, mimetype=mime_type, resumable=True)

            if mime_type is None:
                mime_type = 'application/octet-stream'

            file_metadata = {'name': file_name, 'parents': [folder_id]}

            try:
                file = service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True).execute()
                print(f'File ID: {file.get("id")}')
                return file.get('id')
            except HttpError as error:
                print(f'An error occurred: {error}')
                return None
      """      

    # ref: https://developers.google.com/drive/api/guides/delete
    def delete_file_or_folder(self, file_id):
        """
        Delete a file or folder from Google Drive.
        구글 드라이브에서 파일 또는 폴더를 삭제합니다.
        
        Args:
            file_id (str): The ID of the file or folder to delete.
            삭제할 파일 또는 폴더의 ID입니다.
        """
        service = self.create_service()
        try:
            service.files().delete(fileId=file_id, supportsAllDrives=True).execute()
            print(f'File or Folder with ID: {file_id} has been deleted.')
        except HttpError as error:
            print(f'An error occurred: {error}')

    # ref: https://developers.google.com/drive/api/guides/search-files
    def search_file(self,folder_id):
        """
        Search files within a folder on Google Drive.
        구글 드라이브의 폴더 내에서 파일을 검색합니다.
        
        Args:
            folder_id (str): The ID of the folder to search files in.
            파일을 검색할 폴더의 ID입니다.
        
        Returns:
            list: A list of dictionaries containing file information.
            파일 정보를 포함하는 사전의 리스트입니다.
        """
        service = self.create_service()
        try:
            files = []
            page_token = None
            while True:
                # pylint: disable=maybe-no-member
                response = (
                    service.files()
                    .list(
                        #q="mimeType != 'application/vnd.google-apps.folder'",
                        includeItemsFromAllDrives=True,  # 공유 드라이브 항목 포함
                        q=f"'{folder_id}' in parents",  # 특정 폴더의 파일 검색
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                        supportsAllDrives=True,
                    )
                    .execute()
                )
                for file in response['files']:
                    print(f'File name: {file["name"]}, File ID: {file["id"]}')
                break

        except HttpError as error:
            print(f"An error occurred: {error}")
            files = None

        return files

    # ref: https://developers.google.com/drive/api/guides/manage-downloads#download-content
    def download_file(self, file_id, file_name=None):
        """
        Download a file from Google Drive.
        Google 드라이브에서 파일을 다운로드합니다.

        Args:
            file_id (str): The ID of the file to download.
                다운로드할 파일의 ID입니다.
            file_name (str, optional): The name to save the downloaded file as.
                If not provided, the file will be saved with the file ID and its extension.
                (default is None)
                다운로드한 파일을 저장할 이름입니다. 제공되지 않으면 파일 ID와 확장자를 사용하여 저장됩니다.
                (기본값은 None)

        Returns:
            BytesIO or None: A BytesIO object containing the downloaded file content, or None if download fails.
                다운로드된 파일 내용을 담은 BytesIO 객체이며, 다운로드에 실패한 경우 None입니다.
        """
        service = self.create_service()
        try:
            request = service.files().get_media(fileId=file_id)
            file_io = io.BytesIO()  # 파일 콘텐츠를 저장할 IO 스트림
            downloader = MediaIoBaseDownload(file_io, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}% complete.")

            file_io.seek(0)  # 파일 읽기를 위해 커서를 처음으로 이동

            # 파일 이름이 제공되지 않은 경우 파일 ID를 사용
            if not file_name:
                file_name = f"{file_id}{self.get_file_extension(file_id)}"

            # 파일 콘텐츠를 디스크에 저장
            file_io.seek(0)  # 파일 읽기를 위해 커서를 처음으로 이동
            with open(file_name, 'wb') as f:
                f.write(file_io.read())
                print(f"File saved as {file_name}")
            return file_io  # 파일 콘텐츠가 담긴 IO 스트림을 반환

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
        
    # ref: https://developers.google.com/drive/api/guides/manage-downloads#export-content
    def export_file(self, file_id):
        """
        Export a Google Workspace document in the specified format.
        지정된 형식으로 Google Workspace 문서를 내보냅니다.
        
        Args:
            file_id (str): The ID of the file to export.
            내보낼 파일의 ID입니다.
            mime_type (str): The MIME type of the file format to export.
            내보낼 파일 형식의 MIME 타입입니다.
        
        Returns:
            BytesIO: A BytesIO object containing the exported file content.
            내보낸 파일 내용을 담은 BytesIO 객체입니다.
        """
        service = self.create_service()
        try:
            mime_type = self.get_file_extension(file_id)
            # Drive API 클라이언트 생성
            request = service.files().export_media(fileId=file_id, mimeType=mime_type)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}% complete.")
            file.seek(0)  # 파일 읽기를 위해 커서를 처음으로 이동
            return file
        except HttpError as error:
                    print(f"An error occurred: {error}")
                    files = None
        return
    
        
    def authenticate(self):
        """
        Perform user authentication.
        사용자 인증을 수행합니다.
        
        Returns:
            Credentials: The authenticated credentials.
            인증된 자격 증명입니다.
        """
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except RefreshError:
                    creds = None
            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.scopes)
                creds = flow.run_local_server(port=0)
                with open(self.token_path, "w") as token:
                    token.write(creds.to_json())
        return creds
    def create_service(self):
        """
        Create Google Drive API service.
        구글 드라이브 API 서비스를 생성합니다.
        
        Returns:
            Resource: The Drive API service resource.
            드라이브 API 서비스 리소스입니다.
        """
        return build('drive', 'v3', credentials=self.creds)
    def get_file_extension(self, file_id):
        """
        Get the file extension either from the filename or based on its MIME type.
        파일 이름에서 파일 확장자를 가져오거나, 파일 이름에 확장자가 없는 경우 MIME 타입을 기반으로 확장자를 가져옵니다.

        Args:
            file_id (str): The ID of the file to get the extension for.
            파일의 확장자를 가져올 파일의 ID입니다.

        Returns:
            str: The file extension extracted from the filename or corresponding to the MIME type.
            파일 이름에서 추출된 파일 확장자이거나 MIME 타입에 해당하는 파일 확장자입니다.
        """
        service = self.create_service()
        try:
            file = service.files().get(fileId=file_id, fields='name, mimeType', supportsAllDrives=True).execute()
            file_name = file.get('name')
            mime_type = file.get('mimeType')

            # 파일 이름에서 확장자 추출 시도
            if '.' in file_name:
                extension = '.' + file_name.split('.')[-1]
                print(f'Extension from filename: {extension}')
            else:
                # 파일 이름에 확장자가 없는 경우 MIME 타입을 기반으로 확장자 결정
                extension_mapping = {
                    'application/vnd.google-apps.document': '.docx',
                    'application/vnd.google-apps.spreadsheet': '.xlsx',
                    'application/vnd.google-apps.presentation': '.pptx',
                    'application/pdf': '.pdf',
                    'text/plain': '.txt',
                    'application/rtf': '.rtf',
                    'application/zip': '.zip',
                    'image/jpeg': '.jpg',
                    'image/png': '.png',
                    'image/svg+xml': '.svg',
                    'application/msword': '.doc',  # MS Word 문서에 대한 확장자 추가
                    # 기타 필요한 MIME 타입 및 확장자 매핑
                }
                extension = extension_mapping.get(mime_type, '')
                print(f'Extension from MIME type: {extension}')

            return extension

        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
    
        
# Example usage
if __name__ == "__main__":
    # .env 파일에서 환경 변수 불러오기
    load_dotenv()
    # 환경 변수 사용
    PROJECT_ROOT_DIR = os.getcwd()
    CREDENTIALS_JSON = os.getenv('CREDENTIALS_JSON')
    TOKEN_JSON = os.getenv('TOKEN_JSON')
    SHARED_DRIVE_ID = os.getenv('SHARED_DRIVE_ID')


    # 프로젝트 디렉토리, 디렉토리로 부터의 json파일 위치, 디렉토리로 부터의 json파일 위치 
    manager = GoogleDriveManager(PROJECT_ROOT_DIR, CREDENTIALS_JSON, TOKEN_JSON)

    # 새 폴더 만들기
    # Create a new folder
    folder_id = manager.create_folder('New Folder')

    # 새로 만든 폴더에 파일 업로드
    # Upload a file to the newly created folder
    file_id = manager.upload_file('/path/to/your/file.txt', folder_id)

    # Google 드라이브에서 파일 다운로드
    # Download a file from Google Drive
    manager.download_file(file_id)

    # 폴더 내 파일 검색
    # Search for files within a folder
    manager.search_file(folder_id)

    # Google 워크스페이스 문서 내보내기
    # Export a Google Workspace document
    manager.export_file('your-google-docs-file-id')
