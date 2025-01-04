from math import ceil
from random import choice

import pygame.transform
import pygame_gui.elements

from scripts.cat.cats import Cat
from scripts.game_structure import image_cache
from scripts.game_structure.game_essentials import game
from scripts.game_structure.ui_elements import (
    UIImageButton,
    UISpriteButton,
    UISurfaceImageButton
)
from scripts.utility import (
    get_text_box_theme,
    ui_scale,
    shorten_text_to_fit,
    ui_scale_dimensions,
)
from .Screens import Screens
from ..game_structure.screen_settings import MANAGER
from ..ui.generate_box import get_box, BoxStyles
from ..ui.generate_button import get_button_dict, ButtonStyles
from ..ui.get_arrow import get_arrow
from ..ui.icon import Icon


class ElderStoryScreen(Screens):
    def __init__(self, name=None):
        super().__init__(name)
        self.back_button = None
        self.selected_elder = None
        self.selected_cat_1 = None
        self.search_bar = None
        self.search_bar_image = None
        self.elder_elements = {}
        self.elders = []
        self.cat_buttons = []
        self.page = 1
        self.selected_cat_elements = {}
        self.faith_bars = {}
        self.allow_romantic = True
        self.current_listed_cats = None
        self.previous_search_text = ""

    def handle_event(self, event):

        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.back_button:
                self.change_screen("profile screen")
            elif event.ui_element == self.last_med:
                self.selected_elder -= 1
                self.update_elder_info()
            elif event.ui_element == self.next_med:
                self.selected_elder += 1
                self.update_elder_info()
            elif event.ui_element == self.next_page:
                self.page += 1
                self.update_page()
            elif event.ui_element == self.previous_page:
                self.page -= 1
                self.update_page()
            elif event.ui_element == self.deselect_1:
                self.selected_cat_1 = None
                self.update_selected_cats()
            elif event.ui_element == self.starclan_story_button:
                game.patrolled.append(self.elders[self.selected_elder].ID)
                output = Cat.elder_story(
                    self.elders[self.selected_elder],
                    self.selected_cat_1,
                    chosen_story = "starclan"
                )
                self.results.set_text(output)
                self.update_selected_cats()
                self.update_elder_info()
            elif event.ui_element == self.df_story_button:
                game.patrolled.append(self.elders[self.selected_elder].ID)
                output = Cat.elder_story(
                    self.elders[self.selected_elder],
                    self.selected_cat_1,
                    chosen_story = "darkforest"
                )
                self.results.set_text(output)
                self.update_selected_cats()
                self.update_elder_info()
            elif event.ui_element == self.random1:
                self.selected_cat_1 = self.random_cat()
                self.update_selected_cats()
            elif event.ui_element in self.cat_buttons:
                self.selected_cat_1 = event.ui_element.return_cat_object()
                self.update_selected_cats()

    def screen_switches(self):
        super().screen_switches()
        self.show_mute_buttons()
        # Gather the elders:
        self.elders = []
        for cat in Cat.all_cats_list:
            if cat.status == "elder" and not (
                cat.dead or cat.outside
            ):
                self.elders.append(cat)

        self.page = 1

        if self.elders:
            if Cat.fetch_cat(game.switches["cat"]) in self.elders:
                self.selected_elder = self.elders.index(
                    Cat.fetch_cat(game.switches["cat"])
                )
            else:
                self.selected_elder = 0
        else:
            self.selected_elder = None

        self.back_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((25, 25), (105, 30))),
            get_arrow(2) + " Back",
            get_button_dict(ButtonStyles.SQUOVAL, (105, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )

        self.selected_frame_1 = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((50, 80), (200, 350))),
            get_box(BoxStyles.ROUNDED_BOX, (200, 350)),
        )
        self.selected_frame_1.disable()

        self.cat_bg = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((50, 470), (700, 150))),
            get_box(BoxStyles.ROUNDED_BOX, (700, 150)),
        )
        self.cat_bg.disable()
        self.starclan_story_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((280, 350), (105, 30))),
            "StarClan",
            get_button_dict(ButtonStyles.SQUOVAL, (105, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )
        self.df_story_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((400, 350), (105, 30))),
            "Dark Forest",
            get_button_dict(ButtonStyles.SQUOVAL, (105, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )

        self.next_med = UISurfaceImageButton(
            ui_scale(pygame.Rect((476, 270), (34, 34))),
            Icon.ARROW_RIGHT,
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
        )
        self.last_med = UISurfaceImageButton(
            ui_scale(pygame.Rect((280, 270), (34, 34))),
            Icon.ARROW_LEFT,
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
        )

        self.next_page = UISurfaceImageButton(
            ui_scale(pygame.Rect((433, 619), (34, 34))),
            Icon.ARROW_RIGHT,
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            manager=MANAGER,
        )
        self.previous_page = UISurfaceImageButton(
            ui_scale(pygame.Rect((333, 619), (34, 34))),
            Icon.ARROW_LEFT,
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            manager=MANAGER,
        )

        self.deselect_1 = UISurfaceImageButton(
            ui_scale(pygame.Rect((68, 434), (127, 30))),
            "Remove Cat",
            get_button_dict(ButtonStyles.SQUOVAL, (127, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )

        addon = ""
        if game.settings["dark mode"]:
            addon = "_dark"

        self.results_box = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((550, 80), (200, 350))),
            pygame.transform.scale(
                image_cache.load_image(f"resources/images/custom_choice_bg{addon}.png"),
                (400, 700),
            )
        )

        self.results = pygame_gui.elements.UITextBox(
            "",
            ui_scale(pygame.Rect((560, 125), (175, 270))),
            object_id=get_text_box_theme("#text_box_22_horizcenter_spacing_95"),
            manager=MANAGER,
        )

        self.error = pygame_gui.elements.UITextBox(
            "",
            ui_scale(pygame.Rect((280, 37), (229, 57))),
            object_id=get_text_box_theme("#text_box_22_horizcenter_spacing_95"),
            manager=MANAGER,
        )
        self.random1 = UISurfaceImageButton(
            ui_scale(pygame.Rect((198, 432), (34, 34))),
            "\u2684",
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            manager=MANAGER,
            sound_id="dice_roll",
        )

        self.search_bar_image = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((55, 625), (118, 34))),
            pygame.image.load("resources/images/search_bar.png").convert_alpha(),
            manager=MANAGER,
        )
        self.search_bar = pygame_gui.elements.UITextEntryLine(
            ui_scale(pygame.Rect((60, 629), (115, 27))),
            object_id="#search_entry_box",
            initial_text="name search",
            manager=MANAGER,
        )

        self.update_buttons()
        self.update_elder_info()

    def random_cat(self):
        if self.selected_cat_list():
            random_list = [
                i for i in self.all_cats_list if i.ID not in self.selected_cat_list()
            ]
        else:
            random_list = self.all_cats_list
        return choice(random_list)

    def update_elder_info(self):
        for ele in self.elder_elements:
            self.elder_elements[ele].kill()
        self.elder_elements = {}

        if (
            self.selected_elder is not None
        ):  # It can be zero, so we must test for not None here.
            x_value = 315
            elder = self.elders[self.selected_elder]

            # Clear elder as selected cat
            if elder == self.selected_cat_1:
                self.selected_cat_1 = None
                self.update_selected_cats()

            self.elder_elements["elder_image"] = pygame_gui.elements.UIImage(
                ui_scale(pygame.Rect((x_value, 90), (150, 150))),
                pygame.transform.scale(elder.sprite, (150, 150)),
            )

            name = str(elder.name)
            short_name = shorten_text_to_fit(name, 120, 11)
            self.elder_elements["name"] = pygame_gui.elements.UILabel(
                ui_scale(pygame.Rect((x_value - 5, 240), (160, -1))),
                short_name,
                object_id=get_text_box_theme(),
            )

            text = elder.personality.trait + "\n" + elder.experience_level

            if elder.not_working():
                text += "\nThis cat isn't able to work"
                self.starclan_story_button.disable()
                self.df_story_button.disable()
            else:
                text += "\nThis cat can work"
                self.starclan_story_button.enable()
                self.df_story_button.enable()

            self.elder_elements["details"] = pygame_gui.elements.UITextBox(
                text,
                ui_scale(pygame.Rect((x_value, 260), (155, 60))),
                object_id=get_text_box_theme("#text_box_22_horizcenter_spacing_95"),
                manager=MANAGER,
            )

            elder_number = len(self.elders)
            if self.selected_elder < elder_number - 1:
                self.next_med.enable()
            else:
                self.next_med.disable()

            if self.selected_elder > 0:
                self.last_med.enable()
            else:
                self.last_med.disable()

        else:
            self.last_med.disable()
            self.next_med.disable()

        self.update_buttons()
        self.update_list_cats()

    def update_list_cats(self):
        self.all_cats_list = [
            i
            for i in Cat.all_cats_list
            if (i.ID != self.elders[self.selected_elder].ID)
            and not (i.dead or i.outside)
            and i.moons > 0
        ]
        self.all_cats = self.chunks(self.all_cats_list, 24)
        self.current_listed_cats = self.all_cats_list
        self.all_pages = (
            int(ceil(len(self.current_listed_cats) / 24.0))
            if len(self.current_listed_cats) > 24
            else 1
        )
        self.update_page()

    def update_page(self):
        for cat in self.cat_buttons:
            cat.kill()
        self.cat_buttons = []
        if self.page > self.all_pages:
            self.page = self.all_pages
        elif self.page < 1:
            self.page = 1

        if self.page >= self.all_pages:
            self.next_page.disable()
        else:
            self.next_page.enable()

        if self.page <= 1:
            self.previous_page.disable()
        else:
            self.previous_page.enable()

        x = 65
        y = 485
        chunked_cats = self.chunks(self.current_listed_cats, 24)
        if chunked_cats:
            for cat in chunked_cats[self.page - 1]:
                if game.clan.clan_settings["show fav"] and cat.favourite != 0:
                    _temp = pygame.transform.scale(
                                pygame.image.load(
                                    f"resources/images/fav_marker_{cat.favourite}.png").convert_alpha(),
                                (50, 50))
                        
                    self.cat_buttons.append(
                        pygame_gui.elements.UIImage(
                            ui_scale(pygame.Rect((x, y), (50, 50))), _temp
                        )
                    )
                    self.cat_buttons[-1].disable()

                self.cat_buttons.append(
                    UISpriteButton(
                        ui_scale(pygame.Rect((x, y), (50, 50))),
                        cat.sprite,
                        cat_object=cat,
                    )
                )
                x += 55
                if x > 700:
                    y += 55
                    x = 65

    def update_selected_cats(self):
        for ele in self.selected_cat_elements:
            self.selected_cat_elements[ele].kill()
        self.selected_cat_elements = {}

        for ele in self.faith_bars:
            self.faith_bars[ele].kill()
        self.faith_bars = {}

        self.draw_info_block(self.selected_cat_1, (50, 80))

        self.update_buttons()

    def draw_info_block(self, cat, starting_pos: tuple):
        if not cat:
            return

        other_cat = [Cat.fetch_cat(i) for i in self.selected_cat_list() if i != cat.ID]
        if other_cat:
            other_cat = other_cat[0]
        else:
            other_cat = None

        tag = str(starting_pos)

        x = starting_pos[0]
        y = starting_pos[1]

        self.selected_cat_elements["cat_image" + tag] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((x + 30, y + 7), (140, 140))),
            pygame.transform.scale(cat.sprite, (140, 140)),
        )

        name = str(cat.name)
        short_name = shorten_text_to_fit(name, 125, 15)
        self.selected_cat_elements["name" + tag] = pygame_gui.elements.UILabel(
            ui_scale(pygame.Rect((x, y + 150), (200, 30))),
            short_name,
            object_id="#text_box_30_horizcenter",
        )

        col1 = ""
        col1 += str(cat.moons)
        if cat.moons == 1:
            col1 += " moon"
        else:
            col1 += " moons"
        if len(cat.personality.trait) > 15:
            _t = cat.personality.trait[:13] + ".."
        else:
            _t = cat.personality.trait
        col1 += "\n" + _t
        col1 += "<br>"

        if cat.moons < 6:
            col1 += "???"
        else:
            col1 += cat.skills.skill_string()

        self.selected_cat_elements["col1" + tag] = pygame_gui.elements.UITextBox(
            col1,
            ui_scale(pygame.Rect((x + 11, y + 176), (180, -1))),
            object_id="#text_box_22_horizcenter",
            manager=MANAGER,
        )

        cat_faith = round(cat.faith)

        y_pos = y + 255
        x_pos = x + 16

        faith_text = "Mrrp?"

        if cat_faith < 0:
            if cat_faith < -5:
                faith_text = "Heavy Dark Forest faith"
            else:
                faith_text = "Slight Dark Forest faith"
            cat_faith *= -1
            image_path = "resources/images/relation_bar_red.png"
        elif cat_faith > 0:
            if cat_faith > 5:
                faith_text = "Heavy StarClan faith"
            else:
                faith_text = "Slight StarClan faith"
            image_path = "resources/images/relation_bar_green.png"
        else:
            faith_text = "Neutral faith"
            image_path = "resources/images/relation_bar.png"

        if cat.moons > 5:
            for i in range(cat_faith):
                self.faith_bars[str(i)] = pygame_gui.elements.UIImage(
                    ui_scale(pygame.Rect((x_pos, y_pos), (10, 38))),
                    image_cache.load_image(image_path).convert_alpha())
                x_pos += 30
        else:
            faith_text = "Faith unknown"

        self.selected_cat_elements["col1_faithtext"] = pygame_gui.elements.UITextBox(
            faith_text,
            ui_scale(pygame.Rect((x + 11, y + 296), (180, -1))),
            object_id="#text_box_22_horizcenter",
            manager=MANAGER,
        )


    def selected_cat_list(self):
        output = []
        if self.selected_cat_1:
            output.append(self.selected_cat_1.ID)

        return output

    def update_buttons(self):
        error_message = ""

        invalid_elder = False
        if self.selected_elder is not None:
            if self.elders[self.selected_elder].not_working():
                invalid_elder = True
                error_message += "This elder can't work this moon. "
            elif self.elders[self.selected_elder].ID in game.patrolled:
                invalid_elder = True
                error_message += "This elder has already worked this moon. "
        else:
            invalid_elder = True

        invalid_pair = False

        if self.selected_cat_1 is None:
            invalid_pair = True

        self.error.set_text(error_message)

        if invalid_elder or invalid_pair:
            self.starclan_story_button.disable()
            self.df_story_button.disable()
        else:
            self.starclan_story_button.enable()
            self.df_story_button.enable()

    def update_search_cats(self, search_text):
        """Run this function when the search text changes, or when the screen is switched to."""
        self.current_listed_cats = []
        Cat.sort_cats(self.all_cats_list)

        search_text = search_text.strip()
        if search_text not in ["", "name search"]:
            for cat in self.all_cats_list:
                if search_text.lower() in str(cat.name).lower():
                    self.current_listed_cats.append(cat)
        else:
            self.current_listed_cats = self.all_cats_list.copy()

        self.all_pages = (
            int(ceil(len(self.current_listed_cats) / 24.0))
            if len(self.current_listed_cats) > 24
            else 1
        )

        Cat.ordered_cat_list = self.current_listed_cats
        self.update_page()

    def exit_screen(self):
        self.selected_cat_1 = None

        for ele in self.elder_elements:
            self.elder_elements[ele].kill()
        self.elder_elements = {}

        for cat in self.cat_buttons:
            cat.kill()
        self.cat_buttons = []

        for ele in self.selected_cat_elements:
            self.selected_cat_elements[ele].kill()
        self.selected_cat_elements = {}

        for ele in self.faith_bars:
            self.faith_bars[ele].kill()
        self.faith_bars = {}

        self.elders = []
        self.back_button.kill()
        del self.back_button
        self.selected_frame_1.kill()
        del self.selected_frame_1
        self.cat_bg.kill()
        del self.cat_bg
        self.starclan_story_button.kill()
        del self.starclan_story_button
        self.df_story_button.kill()
        del self.df_story_button
        self.last_med.kill()
        del self.last_med
        self.next_med.kill()
        del self.next_med
        self.deselect_1.kill()
        del self.deselect_1
        self.next_page.kill()
        del self.next_page
        self.previous_page.kill()
        del self.previous_page
        self.results.kill()
        del self.results
        self.results_box.kill()
        del self.results_box
        self.random1.kill()
        del self.random1
        self.error.kill()
        del self.error
        self.search_bar_image.kill()
        del self.search_bar_image
        self.search_bar.kill()
        del self.search_bar

    def chunks(self, L, n):
        return [L[x : x + n] for x in range(0, len(L), n)]

    def on_use(self):
        super().on_use()
        # Only update the positions if the search text changes
        if self.search_bar.is_focused and self.search_bar.get_text() == "name search":
            self.search_bar.set_text("")
        if self.search_bar.get_text() != self.previous_search_text:
            self.update_search_cats(self.search_bar.get_text())
        self.previous_search_text = self.search_bar.get_text()
