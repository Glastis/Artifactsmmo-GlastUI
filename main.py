import arcade
import arcade.gui

from ui.MainMenu import MainMenu
import constants.prog as prog

class ArtifactUI(arcade.Window):
    def __init__(self):
        super().__init__(1800, 1000, prog.prog_title)
        self.main_menu = MainMenu()
        self.show_view(self.main_menu)


def main():
    window = ArtifactUI()
    arcade.run()


if __name__ == "__main__":
    main()