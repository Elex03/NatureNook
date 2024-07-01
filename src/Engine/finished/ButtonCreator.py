from ButtonManager import ButtonManager

class ButtonCreator:
    def __init__(self, button_manager):
        self.button_manager = button_manager

    def create_buttons(self):
        # Main menu buttons
        self.button_manager.create_button("resume", 50, 200, "button_resume.png", 1, "main")
        self.button_manager.create_button("options", 43, 325, "button_options.png", 1, "main")
        self.button_manager.create_button("quit", 36, 450, "button_quit.png", 1, "main")
        self.button_manager.create_button("Logo", -40, 30, "Naturenook.png", 1, "main")


        # Options menu buttons
        self.button_manager.create_button("audio", 225, 200, "button_audio.png", 1, "options")
        self.button_manager.create_button("back", 332, 450, "button_back.png", 1, "options")

        # Audio menu buttons
        self.button_manager.create_button("back", 150, 350, "button_back.png", 1, "resume")  # Add back button for audio menu
