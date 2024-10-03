import arcade
import arcade.gui


class SettingsOverlay(arcade.View):
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view  # Stocker la vue précédente
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Créer une boîte verticale pour les boutons
        self.v_box = arcade.gui.UIBoxLayout()

        # Bouton "Back"
        button_back = arcade.gui.UIFlatButton(text="Back", width=200)
        self.v_box.add(button_back.with_space_around(bottom=20))
        button_back.on_click = self.exit_settings

        # Ajouter le menu en position centrale
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        # Afficher la vue précédente (le jeu ou le menu)
        self.previous_view.on_draw()

        # Dessiner un rectangle semi-transparent pour l'overlay des paramètres
        arcade.draw_lrtb_rectangle_filled(0, self.window.width, self.window.height, 0, (0, 0, 0, 210))

        # Dessiner les éléments de l'UI des paramètres
        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """Capture tous les clics et ne les laisse pas passer à l'arrière-plan."""
        if self.manager:
            self.manager.on_mouse_press(x, y, button, modifiers)
        return True  # Empêcher la propagation des événements

    def on_mouse_release(self, x, y, button, modifiers):
        """Capture les relâchements de souris."""
        if self.manager:
            self.manager.on_mouse_release(x, y, button, modifiers)
        return True  # Empêcher la propagation des événements

    def on_mouse_motion(self, x, y, dx, dy):
        """Bloquer les mouvements de la souris pour empêcher les effets de survol."""
        if self.manager:
            self.manager.on_mouse_motion(x, y, dx, dy)
        return True  # Bloquer la propagation du mouvement de la souris

    def on_key_press(self, key, modifiers):
        """Capture tous les événements clavier."""
        if self.manager:
            self.manager.on_key_press(key, modifiers)
        return True  # Empêcher la propagation des événements

    def on_key_release(self, key, modifiers):
        """Capture tous les événements clavier."""
        if self.manager:
            self.manager.on_key_release(key, modifiers)
        return True  # Empêcher la propagation des événements

    def exit_settings(self, event):
        """Retourner à la vue précédente."""
        self.manager.disable()
        self.window.show_view(self.previous_view)

