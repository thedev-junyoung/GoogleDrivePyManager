# English Version
Google Drive Manager
The Google Drive Manager is a Python class designed to simplify interactions with the Google Drive API, enabling easy file and folder management within Google Drive.

## Features
- User authentication with Google Drive API.
- Creation of folders within Google Drive.
- Uploading files to a specified folder in Google Drive.
- Searching for files within a specified folder.
- Downloading files from Google Drive.
- Exporting Google Workspace documents in different formats.
- Determining the file extension based on the filename or MIME type.

## Getting Started
To get started with the Google Drive Manager, follow these steps:

1. Set Up Google Drive API: Follow the Google Drive API documentation to enable the API and obtain your credentials.json file.

2. Create a Virtual Environment and Install Required Packages:

    2-1. Create a Virtual Environment: 
    Using a virtual environment is recommended to effectively manage dependencies for Python projects. Follow these steps to set up and activate a virtual environment: 
    Navigate to your project directory and execute the following command:

    ```
    python -m venv venv
    ```

    This command creates a new virtual environment named `venv` within your project directory.

    2-2. **Activate the Virtual Environment**:
    - On **Windows**, run:
        ```
        .\venv\Scripts\activate
        ```
    - On **macOS** and **Linux**, run:
        ```
        source venv/bin/activate
        ```
        
    If `(venv)` appears before your command prompt, the virtual environment is activated. Ensure the necessary Python packages are installed:
    ```
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```
    or
    ```
    pip install -r requirements.txt
    ```

3. Clone the Repository: Clone this repository to your local machine:

```shell
git clone https://github.com/thedev-junyoung/google-drive.git
```
4. Set Up Environment Variables: Create a .env file in the root directory of the project and define the following variables:
```makefile
CREDENTIALS_JSON = your_credentials_file_path.json
TOKEN_JSON = token.json
SHARED_DRIVE_ID = your_shared_drive_id
```

5. Initialize the Manager: Initialize the GoogleDriveManager class with your project's root directory, credentials file name, and token file name:

```python
Copy code
from google_drive_manager import GoogleDriveManager

manager = GoogleDriveManager('/path/to/your/project', 'credentials.json', 'token.json')
```
6. Use the Manager: You can now use the manager to perform various operations such as creating folders, uploading files, and more.

## Example Usage
```python
# Create a new folder
folder_id = manager.create_folder('New Folder')

# Upload a file to the newly created folder
file_id = manager.upload_file('/path/to/your/file.txt', folder_id)

# Download a file from Google Drive
manager.download_file(file_id)

# Search for files within a folder
manager.search_file(folder_id)

# Export a Google Workspace document
manager.export_file('your-google-docs-file-id')
```

## References

- Google Drive API Documentation: 
    - https://developers.google.com/drive
    - https://developers.google.com/drive/api/guides/about-sdk
    - https://developers.google.com/drive/api/quickstart/python
    - https://developers.google.com/drive/api/guides/about-files
    - ...




# 한글 버전


# 구글 드라이브 매니저

구글 드라이브 매니저는 구글 드라이브 API와의 상호작용을 단순화하기 위해 설계된 파이썬 클래스로, 구글 드라이브 내에서 파일 및 폴더 관리를 쉽게 할 수 있습니다.

## 기능

- 구글 드라이브 API와의 사용자 인증.
- 구글 드라이브 내에 폴더 생성.
- 지정된 폴더로 파일 업로드.
- 지정된 폴더 내에서 파일 검색.
- 구글 드라이브에서 파일 다운로드.
- 다양한 형식으로 구글 워크스페이스 문서 내보내기.
- 파일 이름 또는 MIME 타입을 기반으로 파일 확장자 결정.

## 시작하기

구글 드라이브 매니저를 시작하려면 다음 단계를 따르세요:

1. **구글 드라이브 API 설정**: 구글 드라이브 API 문서를 따라 API를 활성화하고 `credentials.json` 파일을 얻으세요.
    
2. **가상 환경 생성 및 필요한 패키지 설치**: 

    2-1. **가상 환경 생성**: 
    파이썬 프로젝트에 대한 의존성을 효과적으로 관리하기 위해 가상 환경 사용을 권장합니다. 
    가상 환경을 설정하고 활성화하기 위한 단계는 다음과 같습니다:
    프로젝트 디렉토리로 이동한 다음 다음 명령어를 실행하세요:
    ```
    python -m venv venv
    ```
    이 명령어는 프로젝트 디렉토리 내에 `venv`라는 이름의 새로운 가상 환경을 생성합니다.
    
    2-2. **가상 환경 활성화**:
    - **Windows**에서는 다음을 실행하세요:
        ```
        .\venv\Scripts\activate
        ```
        
    - **macOS**와 **Linux**에서는 다음을 실행하세요:
        ```
        source venv/bin/activate
        ```
    명령 프롬프트 앞에 `(venv)`가 표시되면 가상 환경이 활성화된 것입니다.
    필요한 파이썬 패키지가 설치되어 있는지 확인하세요:
    ```
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```
    or
    ```
    pip install -r requirements.txt

    ```
3. **저장소 클론**: 이 저장소를 로컬 머신으로 클론하세요:
    ```
    git clone https://github.com/thedev-junyoung/google-drive.git
    ```
4. **환경 변수 설정**: 프로젝트의 루트 디렉토리에 `.env` 파일을 생성하고 다음 변수를 정의하세요:
    
    ```makefileCopy
    CREDENTIALS_JSON = your_credentials_file_path.json 
    TOKEN_JSON = token.json 
    SHARED_DRIVE_ID = your_shared_drive_id
    ```
    
5. **매니저 초기화**: 프로젝트의 루트 디렉토리, 자격 증명 파일 이름, 토큰 파일 이름을 사용하여 GoogleDriveManager 클래스를 초기화하세요:
    
    ```python
    from google_drive_manager import GoogleDriveManager  manager = GoogleDriveManager('/path/to/your/project', 'credentials.json', 'token.json')
    ```
    
6. **매니저 사용**: 이제 매니저를 사용하여 폴더 생성, 파일 업로드 등 다양한 작업을 수행할 수 있습니다.
    

## 사용 예시

pythonCopy code

```python
# 새 폴더 생성 
folder_id = manager.create_folder('New Folder')  
# 새로 생성한 폴더에 파일 업로드 
file_id = manager.upload_file('/path/to/your/file.txt', folder_id)  
# 구글 드라이브에서 파일 다운로드 
manager.download_file(file_id)  
# 폴더 내에서 파일 검색 
manager.search_file(folder_id)  
# 구글 워크스페이스 문서 내보내기 
manager.export_file('your-google-docs-file-id')
```


## 참고 자료

- 구글 드라이브 API 문서: 
    - https://developers.google.com/drive
    - https://developers.google.com/drive/api/guides/about-sdk
    - https://developers.google.com/drive/api/quickstart/python
    - https://developers.google.com/drive/api/guides/about-files
    - ...