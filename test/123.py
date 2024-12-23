import os
import shutil

# Define project structure
project_structure = {
    "ErgonomicsApplication": [
        "app.py", "config.py", "requirements.txt", "README.md",
        {
            "app": [
                "__init__.py",
                {"schemas": ["UserSchema.py", "TestResultsSchema.py"]},
                {"services": ["UserService.py", "TestService.py"]},
                {"repository": ["UserRepository.py", "TestRepository.py"]},
                {"database": ["models.py", "database.py"]},
            ]
        },
        {
            "ui": [
                "__init__.py", "window_manager.py",
                {"screens": [
                    "AuthWindow.py", "LoginWindow.py", "RegisterWindow.py", "MainWindow.py",
                    "TestSelectionWindow.py", "TestInstructionWindow.py", "PVTWindow.py",
                    "NASA_TLXWindow.py", "ResultsWindow.py", "ReportWindow.py"
                ]},
                {"components": ["CenteredFrame.py", "ErrorLabel.py", "StyledButton.py"]},
                {"assets": [
                    "logo.png",
                    {"icons": ["user.png", "test.png"]}
                ]}
            ]
        },
        {"tests": ["test_user_service.py", "test_pvt_logic.py", "test_nasa_tlx_logic.py"]}
    ]
}

# Helper function to create project structure
def create_structure(base_path, structure):
    for item in structure:
        if isinstance(item, str):
            open(os.path.join(base_path, item), 'w').close()  # Create empty file
        elif isinstance(item, dict):
            for folder, contents in item.items():
                folder_path = os.path.join(base_path, folder)
                os.makedirs(folder_path, exist_ok=True)
                create_structure(folder_path, contents)

# Create the project structure
base_path = "../ErgonomicsApplication"
if os.path.exists(base_path):
    shutil.rmtree(base_path)  # Clear previous attempts

os.makedirs(base_path, exist_ok=True)
create_structure(base_path, project_structure["ErgonomicsApplication"])