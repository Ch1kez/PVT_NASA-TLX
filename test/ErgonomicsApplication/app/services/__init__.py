
ERGONOMICSAPPLICATION
|   app.py
|   config.py
|   README.md
|   requirements.txt
|
+---app
|   |   __init__.py
|   |
|   +---database
|   |       database.py
|   |       models.py
|   |       __init__.py
|   |
|   +---repository
|   |       TestRepository.py
|   |       UserRepository.py
|   |       __init__.py
|   |
|   +---schemas
|   |       TestResultsSchema.py
|   |       UserSchema.py
|   |       __init__.py
|   |
|   \---services
|           TestService.py
|           UserService.py
|           __init__.py
|
+---tests
|       test_nasa_tlx_logic.py
|       test_pvt_logic.py
|       test_user_service.py
|       __init__.py
|
\---ui
    |   window_manager.py
    |   __init__.py
    |
    +---assets
    |   |   logo.png
    |   |
    |   \---icons
    |           test.png
    |           user.png
    |
    +---components
    |       CenteredFrame.py
    |       ErrorLabel.py
    |       StyledButton.py
    |       __init__.py
    |
    \---screens
            AuthWindow.py
            LoginWindow.py
            MainWindow.py
            NASA_TLXWindow.py
            PVTWindow.py
            RegisterWindow.py
            ReportWindow.py
            ResultsWindow.py
            TestInstructionWindow.py
            TestSelectionWindow.py
            __init__.py
