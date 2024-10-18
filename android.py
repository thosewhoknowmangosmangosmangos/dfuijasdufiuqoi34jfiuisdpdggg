from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import os
import random
from PIL import Image as PILImage

# Paths to the folders (change these paths to your specific one
tshirt_folder = "C:/Users/Acer/Desktop/BAWOVSKI SHO/assets/t-shirts"
pants_folder = "C:/Users/Acer/Desktop/BAWOVSKI SHO/assets/pants"
shoes_folder = "C:/Users/Acer/Desktop/BAWOVSKI SHO/assets/shoes"

class OutfitGenerator(BoxLayout):
    def __init__(self, **kwargs):
        super(OutfitGenerator, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = 20
        self.spacing = 10
        
        # Left panel for buttons
        self.button_panel = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        self.add_widget(self.button_panel)

        # Buttons
        self.generate_button = Button(text="Generate Outfit", on_press=self.generate_outfit)
        self.button_panel.add_widget(self.generate_button)

        self.other_pants_button = Button(text="Other Pants", on_press=self.generate_other_pants)
        self.button_panel.add_widget(self.other_pants_button)

        self.other_shoes_button = Button(text="Other Shoes", on_press=self.generate_other_shoes)
        self.button_panel.add_widget(self.other_shoes_button)

        self.other_shirt_button = Button(text="Other Shirt", on_press=self.generate_other_shirt)
        self.button_panel.add_widget(self.other_shirt_button)

        self.export_button = Button(text="Export Outfit", on_press=self.export_outfit)
        self.button_panel.add_widget(self.export_button)

        # Scrollable canvas for displaying the outfit
        self.canvas_panel = ScrollView(size_hint=(0.7, 1))
        self.canvas_box = BoxLayout(size_hint_y=None, orientation='vertical')
        self.canvas_box.bind(minimum_height=self.canvas_box.setter('height'))
        self.canvas_panel.add_widget(self.canvas_box)
        self.add_widget(self.canvas_panel)

        # Initialize the outfit images
        self.current_outfit = [None, None, None]  # [tshirt, pants, shoes]
        self.outfit_image = Image(size_hint=(1, None), height=1280)
        self.canvas_box.add_widget(self.outfit_image)

    def generate_outfit(self, *args):
        # Select random images from each folder
        tshirt_image = self.get_random_image(tshirt_folder)
        pants_image = self.get_random_image(pants_folder)
        shoes_image = self.get_random_image(shoes_folder)

        # Save current outfit for export
        self.current_outfit = [tshirt_image, pants_image, shoes_image]
        
        # Display the images
        self.display_combined_outfit()

    def get_random_image(self, folder):
        images = [img for img in os.listdir(folder) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
        selected_image = random.choice(images)
        return os.path.join(folder, selected_image)

    def display_combined_outfit(self):
        # Create a new blank image with 1280x1280 resolution for display
        combined_image = PILImage.new('RGB', (1280, 1280), color='white')

        if self.current_outfit[0]:  # Shirt (upper-left)
            shirt_img = PILImage.open(self.current_outfit[0]).resize((600, 600), PILImage.LANCZOS)
            combined_image.paste(shirt_img, (0, 0))  # Position at (0, 0)

        if self.current_outfit[1]:  # Pants (middle-right)
            pants_img = PILImage.open(self.current_outfit[1]).resize((600, 600), PILImage.LANCZOS)
            combined_image.paste(pants_img, (640, 400))  # Position at (640, 400)

        if self.current_outfit[2]:  # Shoes (bottom-left)
            shoes_img = PILImage.open(self.current_outfit[2]).resize((600, 600), PILImage.LANCZOS)
            combined_image.paste(shoes_img, (0, 850))  # Position at (0, 850)

        # Save combined image for display
        combined_image.save("combined_outfit.png")
        self.outfit_image.source = "combined_outfit.png"
        self.outfit_image.reload()

    def generate_other_pants(self, *args):
        pants_image = self.get_random_image(pants_folder)
        self.current_outfit[1] = pants_image  # Update pants
        self.display_combined_outfit()

    def generate_other_shoes(self, *args):
        shoes_image = self.get_random_image(shoes_folder)
        self.current_outfit[2] = shoes_image  # Update shoes
        self.display_combined_outfit()

    def generate_other_shirt(self, *args):
        tshirt_image = self.get_random_image(tshirt_folder)
        self.current_outfit[0] = tshirt_image  # Update shirt
        self.display_combined_outfit()

    def export_outfit(self, *args):
        if any(self.current_outfit):  # Check if any item is selected
            save_path = self.save_file_popup()
            if save_path:
                # Save the current outfit to the specified path
                combined_image = PILImage.new('RGB', (1280, 1280), color='white')
                if self.current_outfit[0]:
                    shirt_img = PILImage.open(self.current_outfit[0]).resize((600, 600), PILImage.LANCZOS)
                    combined_image.paste(shirt_img, (0, 0))

                if self.current_outfit[1]:
                    pants_img = PILImage.open(self.current_outfit[1]).resize((600, 600), PILImage.LANCZOS)
                    combined_image.paste(pants_img, (640, 400))

                if self.current_outfit[2]:
                    shoes_img = PILImage.open(self.current_outfit[2]).resize((600, 600), PILImage.LANCZOS)
                    combined_image.paste(shoes_img, (0, 850))

                # Save combined image
                combined_image.save(save_path)
                self.show_popup("Success", "Outfit exported successfully!")

    def save_file_popup(self):
        # Create a FileChooser popup to save the image
        content = FileChooserIconView()
        popup = Popup(title="Save Outfit", content=content, size_hint=(0.9, 0.9))
        content.bind(on_submit=lambda *x: self.dismiss_save_popup(popup, x[1][0]))
        popup.open()
        return None

    def dismiss_save_popup(self, popup, selection):
        popup.dismiss()
        if selection:
            return selection[0]
        return None

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Button(text=message), size_hint=(0.6, 0.4))
        popup.open()

class OutfitGeneratorApp(App):
    def build(self):
        return OutfitGenerator()

if __name__ == "__main__":
    OutfitGeneratorApp().run()
