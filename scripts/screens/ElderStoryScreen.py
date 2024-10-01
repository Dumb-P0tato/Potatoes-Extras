from math import ceil
from random import choice

import pygame.transform
import pygame_gui.elements

from scripts.cat.cats import Cat
from scripts.game_structure import image_cache
from scripts.game_structure.game_essentials import game, MANAGER, screen_x, screen_y
from scripts.game_structure.ui_elements import (
    UIImageButton,
    UISpriteButton,
    UIRelationStatusBar,
)
from scripts.utility import get_text_box_theme, scale, shorten_text_to_fit
from .Screens import Screens


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

        self.back_button = UIImageButton(
            scale(pygame.Rect((50, 50), (210, 60))), "", object_id="#back_button"
        )

        self.selected_frame_1 = pygame_gui.elements.UIImage(
            scale(pygame.Rect((100, 160), (400, 700))),
            pygame.transform.scale(
                image_cache.load_image("resources/images/mediator_selected_frame.png"),
                (400, 700),
            ),
        )
        self.selected_frame_1.disable()

        self.cat_bg = pygame_gui.elements.UIImage(
            scale(pygame.Rect((100, 940), (1400, 300))),
            pygame.transform.scale(
                pygame.image.load(
                    "resources/images/choosing_frame.png"
                ).convert_alpha(),
                (1400, 300),
            ),
        )
        self.cat_bg.disable()
        self.starclan_story_button = UIImageButton(
            scale(pygame.Rect((560, 700), (210, 60))),
            "SC",
            object_id="",
            manager=MANAGER,
        )
        self.df_story_button = UIImageButton(
            scale(pygame.Rect((800, 700), (210, 60))),
            "DF",
            object_id="",
            manager=MANAGER,
        )

        self.next_med = UIImageButton(
            scale(pygame.Rect((952, 540), (68, 68))),
            "",
            object_id="#arrow_right_button",
        )
        self.last_med = UIImageButton(
            scale(pygame.Rect((560, 540), (68, 68))), "", object_id="#arrow_left_button"
        )

        self.next_page = UIImageButton(
            scale(pygame.Rect((866, 1224), (68, 68))),
            "",
            object_id="#relation_list_next",
        )
        self.previous_page = UIImageButton(
            scale(pygame.Rect((666, 1224), (68, 68))),
            "",
            object_id="#relation_list_previous",
        )

        self.deselect_1 = UIImageButton(
            scale(pygame.Rect((136, 868), (254, 60))),
            "",
            object_id="#remove_cat_button",
        )

        addon = ""
        if game.settings["dark mode"]:
            addon = "_dark"

        self.results_box = pygame_gui.elements.UIImage(
            scale(pygame.Rect((1100, 160), (400, 700))),
            pygame.transform.scale(
                image_cache.load_image(f"resources/images/custom_choice_bg{addon}.png"),
                (400, 700),
            )
        )

        self.results = pygame_gui.elements.UITextBox(
            "",
            scale(pygame.Rect((1120, 250), (350, 540))),
            object_id=get_text_box_theme("#text_box_22_horizcenter_spacing_95"),
            manager=MANAGER,
        )

        self.error = pygame_gui.elements.UITextBox(
            "",
            scale(pygame.Rect((560, 75), (458, 115))),
            object_id=get_text_box_theme("#text_box_22_horizcenter_spacing_95"),
            manager=MANAGER,
        )

        self.random1 = UIImageButton(
            scale(pygame.Rect((396, 864), (68, 68))),
            "",
            object_id="#random_dice_button",
        )

        self.search_bar_image = pygame_gui.elements.UIImage(
            scale(pygame.Rect((110, 1250), (236, 68))),
            pygame.image.load("resources/images/search_bar.png").convert_alpha(),
            manager=MANAGER,
        )
        self.search_bar = pygame_gui.elements.UITextEntryLine(
            scale(pygame.Rect((120, 1258), (230, 55))),
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
            x_value = 630
            elder = self.elders[self.selected_elder]

            # Clear elder as selected cat
            if elder == self.selected_cat_1:
                self.selected_cat_1 = None
                self.update_selected_cats()

            self.elder_elements["elder_image"] = pygame_gui.elements.UIImage(
                scale(pygame.Rect((x_value, 180), (300, 300))),
                pygame.transform.scale(elder.sprite, (300, 300)),
            )

            name = str(elder.name)
            short_name = shorten_text_to_fit(name, 240, 22)
            self.elder_elements["name"] = pygame_gui.elements.UILabel(
                scale(pygame.Rect((x_value - 10, 480), (320, -1))),
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
                scale(pygame.Rect((x_value, 520), (310, 120))),
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

        x = 130
        y = 970
        chunked_cats = self.chunks(self.current_listed_cats, 24)
        if chunked_cats:
            for cat in chunked_cats[self.page - 1]:
                if game.clan.clan_settings["show fav"] and cat.favourite != 0:
                    _temp = pygame.transform.scale(
                                pygame.image.load(
                                    f"resources/images/fav_marker_{cat.favourite}.png").convert_alpha(),
                                (100, 100))
                        
                    self.cat_buttons.append(
                        pygame_gui.elements.UIImage(
                            scale(pygame.Rect((x, y), (100, 100))), _temp
                        )
                    )
                    self.cat_buttons[-1].disable()

                self.cat_buttons.append(
                    UISpriteButton(
                        scale(pygame.Rect((x, y), (100, 100))),
                        cat.sprite,
                        cat_object=cat,
                    )
                )
                x += 110
                if x > 1400:
                    y += 110
                    x = 130

    def update_selected_cats(self):
        for ele in self.selected_cat_elements:
            self.selected_cat_elements[ele].kill()
        self.selected_cat_elements = {}

        for ele in self.faith_bars:
            self.faith_bars[ele].kill()
        self.faith_bars = {}

        self.draw_info_block(self.selected_cat_1, (100, 160))

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
            scale(pygame.Rect((x + 60, y + 14), (280, 280))),
            pygame.transform.scale(cat.sprite, (280, 280)),
        )

        name = str(cat.name)
        short_name = shorten_text_to_fit(name, 250, 30)
        self.selected_cat_elements["name" + tag] = pygame_gui.elements.UILabel(
            scale(pygame.Rect((x, y + 300), (400, 60))),
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
            scale(pygame.Rect((x + 22, y + 352), (360, -1))),
            object_id="#text_box_22_horizcenter",
            manager=MANAGER,
        )

        cat_faith = round(cat.faith)

        y_pos = y + 510
        x_pos = x + 32

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
                    scale(pygame.Rect((x_pos, y_pos), (20, 78))),
                    image_cache.load_image(image_path).convert_alpha())
                x_pos += 30
        else:
            faith_text = "Faith unknown"

        self.selected_cat_elements["col1_faithtext"] = pygame_gui.elements.UITextBox(
            faith_text,
            scale(pygame.Rect((x + 22, y + 592), (360, -1))),
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
        # Only update the positions if the search text changes
        if self.search_bar.is_focused and self.search_bar.get_text() == "name search":
            self.search_bar.set_text("")
        if self.search_bar.get_text() != self.previous_search_text:
            self.update_search_cats(self.search_bar.get_text())
        self.previous_search_text = self.search_bar.get_text()
