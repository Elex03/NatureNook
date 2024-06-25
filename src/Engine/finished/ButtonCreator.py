from ButtonManager import ButtonManager

class ButtonCreator:
    def __init__(self, button_manager):
        self.button_manager = button_manager

    def create_buttons(self):
        # Main menu buttons
        self.button_manager.create_button("resume", 304, 125, "button_resume.png", 1, "main")
        self.button_manager.create_button("options", 297, 250, "button_options.png", 1, "main")
        self.button_manager.create_button("quit", 290, 375, "button_quit.png", 1, "main")

        # Options menu buttons
        self.button_manager.create_button("audio", 225, 200, "button_audio.png", 1, "options")
        self.button_manager.create_button("back", 332, 450, "button_back.png", 1, "options")

        # Audio menu buttons
        self.button_manager.create_button("back", 150, 350, "button_back.png", 1, "audio")  # Add back button for audio menu
