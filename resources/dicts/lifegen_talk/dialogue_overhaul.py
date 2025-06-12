import json
import re

# pylint: disable=bare-except
cluster_addons = [
    "upstanding", "brooding", "sweet", "cool", "unlawful", "silly", "neurotic", "introspective",
    "unabashed", "assertive", "stable",
    "bloodthirsty", "fierce", "bold", "daring", "confident", "arrogant", "competitive", "smug", "impulsive", "noisy",
    "cold", "gloomy", "strict", "vengeful", "grumpy", "bullying", "secretive", "aloof", "stoic", "reserved",
    "charismatic", "cunning", "charming", "manipulative", "leader-like", "passionate", "witty",
    "flexible", "mellow", "flamboyant", "righteous", "ambitious", "responsible", "bossy", "know-it-all",
    "loyal", "justified", "methodical", "lonesome", "calm", "wise", "thoughtful", "quiet", "daydreamer",
    "nervous", "insecure", "careful", "meek", "cowardly", "emotional", "troublesome", "childish", "playful", "strange",
    "attention-seeker", "rebellious", "bouncy", "energetic", "spontaneous", "faithful", "polite", "disciplined", 
    "patient", "trusting", "compassionate", "loving", "oblivious", "sincere", "humble",
    "shameless", "honest", "adventurous", "sneaky", "obsessive",
    "teacher", "hunter", "fighter", "runner", "climber", "swimmer", "speaker",
    "mediator", "clever", "insightful", "sense", "kitsitter", "story", "lore",
    "camp", "healer", "star", "omen", "dream", "clairvoyant", "prophet",
    "ghost", "explorer", "tracker", "artistan", "guardian", "tunneler", "navigator",
    "song", "grace", "clean", "innovator", "comforter", "matchmaker", "thinker",
    "cooperative", "scholar", "time", "treasure", "fisher", "language", "sleeper", "dark"
]

rel_addons = [
    "plike",
    "plove",
    "rlike",
    "rlove",
    "dislike",
    "hate",
    "neutral",
    "trust",
    "comfort",
    "respect",
    "jealous"
]

file_nums = {}

file_names = [
    "apprentice",
    "choice_dialogue",
    "crush",
    "deputy",
    "elder",
    "exiled",
    "flirt",
    "insults",
    "former Clancat",
    "general_no_kit",
    "general_no_newborn",
    "general_outsider",
    "general_you_kit",
    "general",
    "kitten",
    "kittypet",
    "leader",
    "loner",
    "mediator apprentice",
    "mediator",
    "medicine cat apprentice",
    "medicine cat",
    "newborn",
    "queen",
    "queen's apprentice",
    "rogue",
    "warrior",
    "focuses/hailstorm",
    "focuses/leader",
    "focuses/starving",
    "focuses/unknown_murder",
    "focuses/valentines",
    "focuses/war",
    "focuses/halloween",
    "focuses/april_fools",
    "focuses/new_years"
]

cluster_tags = [
    "assertive", "unlawful", "unabashed", "sweet", "stable", "cool", "brooding", "unlawful", "introspective",
    "silly", "neurotic", "upstanding",

    'adventurous', 'aloof', 'ambitious', 'arrogant',
    'bloodthirsty', 'bold', 'bouncy', 'calm', 'careful',
    'confident', 'competitive', 'cold', 'charismatic',
    'cunning', 'cowardly', 'childish', 'compassionate',
    'daring', 'emotional', 'energetic', 'fierce', 'flexible',
    'faithful', 'flamboyant', 'grumpy', 'gloomy', 'humble',
    'insecure', 'justified', 'loyal', 'lonesome', 'loving',
    'meek', 'mellow', 'methodical', 'nervous', 'oblivious',
    'obsessive', 'playful', 'reserved', 'righteous', 'responsible',
    'rebellious', 'strict', 'stoic', 'sneaky', 'strange', 'sincere',
    'shameless', 'spontaneous', 'thoughtful', 'troublesome', 'trusting',
    'vengeful', 'witty', 'wise', 'impulsive', 'bullying',
    'attention-seeker', 'charming', 'daring', 'noisy', 'daydreamer',
    'polite', 'know-it-all', 'bossy', 'disciplined', 'patient',
    'manipulative', 'secretive', 'rebellious', 'grumpy', 'passionate',
    'honest', 'leader-like', 'smug', "sweet_trait"
]

they_age_tags = ["they_app", "they_adult", "they_older", "they_sameage", "they_younger"]
you_age_tags = ["you_not_kit", "you_app", "you_older", "you_younger"]

just_statuses = [
    "newborn", "kitten", "medicine cat", "medicine cat apprentice",
    "queen", "queen's apprentice", "warrior", "apprentice",
    "mediator", "mediator apprentice", "deputy", "leader", "elder",
    "any", "Any"
    ]

# tags that will go into the "relationship" constraint
relationship_values = [
    "hate", "jealousy", "platonic", "dislike", "romantic", "admiration", "respect", "trust", "comfort", "neutral",
    "from_your_parent", "from_adopted_parent", "adopted_parent", "half_sibling",
    "littermate", "siblings_mate", "cousin", "adopted_sibling", "parents_siblings",
    "from_mentor", "from_df_mentor", "from_your_kit", "from_your_apprentice",
    "from_df_apprentice", "from_mate", "from_parent", "adopted_parent", "from_kit",
    "sibling", "from_adopted_kit", "non-related", "murderedthem", "murderedyou", "grievingthem", "grievingyou", "non-mates"
]
they_condition_tags = [
    "they_blind", "they_born_blind", "they_went_blind", "only_they_went_blind", "only_they_born_blind", "only_they_blind",
    "they_deaf", "they_born_deaf", "they_went_deaf", "only_they_went_deaf", "only_they_born_deaf", "they_hearing", "only_they_deaf",
    "they_recovering_from_birth", "they_ill", "they_injured", "they_grieving", "they_starving", "they_pregnant",

    "they_allergies", "they_dizzy", "they_nightmares", "they_crookedjaw", "they_failingeyesight",
    "they_failingeyesight", "they_lastinggrief", "they_paralyzed", "they_hearingloss", "they_headaches", "they_raspylungs",
    "they_recurringshock", "they_seizureprone", "they_wastingdisease"
]
you_condition_tags = [
    "you_blind", "you_born_blind", "you_went_blind", "only_you_went_blind", "only_you_born_blind", "only_you_blind",
    "you_deaf", "you_born_deaf", "you_went_deaf", "only_you_went_deaf", "only_you_born_deaf", "only_you_deaf",
    "you_recovering_from_birth", "you_ill", "you_injured", "you_grieving", "you_starving", "you_pregnant",

    "you_allergies", "you_dizzy", "you_nightmares", "you_crookedjaw", "you_failingeyesight",
    "you_failingeyesight", "you_lastinggrief", "you_paralyzed", "you_hearingloss", "you_headaches", "you_raspylungs",
    "you_recurringshock", "you_seizureprone", "you_wastingdisease"
]

num = 0

insult_num = 0

insult_dialogue = []

abbrev_list = [
        "r_c",
        "r_c1",
        "r_c2",
        "l_n",
        "d_c",
        "d_n",
        "r_a", 
        "r_m",
        "y_p",
        "tm_n",
        "t_l", 
        "t_m", 
        "t_p",
        "t_a",
        "t_s",
        "t_k",
        "t_ka",
        "t_kk",
        "y_m",
        "t_p_positive",
        "t_p_negative",
        "m_n",
        "r_q",
        "r_k",
        "r_e",
        "their_crush",
        "your_crush",
        "r_w1",
        "r_w2",
        "r_w3",
        "r_w",
        "y_a",
        "r_s",
        "r_i",
        "y_s",
        "y_l",
        "r_d",
        "df_y_a",
        "df_m_n",
        "r_c_sc",
        "a_n",
        "t_q",
        "y_k",
        "y_kk",
        "rdf_c",
        "fc_c",
        "v_c",
        "l_c",
        "e_c",
        "rsh_c",
        "rsh_w",
        "rsh_e",
        "rsh_a",
        "rsh_d",
        "rsh_m",
        "rsh_k",
        "sh_d",
        "sh_l",
        "n_r1",
        "n_r2",
        "yg_c",
        "tg_c"
    ]

def underscore_replace(string, dialogue_id=""):
    """
    replaces the underscores in abbrevs with hyphens
    """
    new_string = string
    # test = False
    for abbrev in abbrev_list:
        match = re.search(rf'\b\w*{re.escape(abbrev)}\w*\b', string)
        if match:
            abbrev = match.group(0) 
            rel=False
            cluster=False

            new_abbrev = abbrev

            if any(t in abbrev for t in rel_addons):
                rel = True
            if any(t in abbrev for t in cluster_addons):
                cluster = True
            if rel and not cluster:
                new_abbrev = abbrev.replace("_", "-", 1)
            if cluster and not rel:
                new_abbrev = "-".join(abbrev.rsplit("_", 1))
            if cluster and rel:
                new_abbrev = abbrev.replace("_", "-", 1)
                new_abbrev = "-".join(new_abbrev.rsplit("_", 1))

            # if new_abbrev != abbrev:
            #     if abbrev == "plike_r_c_silly":
            #         test = True
            #         print("ABBREV CHANGE:", abbrev, "=>", new_abbrev)

            if "t_p_positive" in abbrev:
                abbrev = abbrev.replace("t_p_positive", "plove-t_p")
            if "t_p_pos" in abbrev:
                abbrev = abbrev.replace("t_p_pos", "plove-t_p")
            if "t_p_negative" in abbrev:
                abbrev = abbrev.replace("t_p_negative", "dislike-t_p")

            new_string = new_string.replace(abbrev, new_abbrev)
            # if dialogue_id == "abbrev_test":
            #     print("REPLACING", abbrev, "=>", new_abbrev)

        new_string = new_string.replace("t_p_positive", "plove-t_p")
        new_string = new_string.replace("t_p_pos", "plove-t_p")
        new_string = new_string.replace("t_p_negative", "dislike-t_p")
    # if test:
    #     print("NEW STRING 2:", new_string)

    if dialogue_id == "abbrev_test":
        print("NEW STRING:", new_string)
    return new_string

for FILE in file_names:
    # new file location
    file_path = f'resources/dicts/lifegen_talk/new/{FILE}.json'
    file_nums[FILE] = 0
    dialogue_json = None
    # old file location
    with open(f"resources/dicts/lifegen_talk/{FILE}.json", 'r') as read_file:
        dialogue_json = json.loads(read_file.read())

    dialogue_dict = {}
   
    for i in dialogue_json.items():
        num += 1
        file_nums[FILE] += 1

        
        if isinstance(i[1], list):
            key = i[0]
            tags = i[1][0]
            dialogue = i[1][1]
            if "insult" in tags and dialogue not in insult_dialogue:
                insult_num += 1
                insult_dialogue.append(dialogue)
            new_dialogue = \
            {key: {
                "tags": [
                    i.lower() for i in tags
                ],
                "intro": [
                    i for i in dialogue
                    ]
                }
            }

            dialogue_dict.update(new_dialogue)
        elif isinstance(i[1], dict):
            # print("dict dialogue:", i[0])
            dialogue_dict.update({i[0]: i[1]})

    overwrite = True
    new_dialogue_dict = {}
    if overwrite is True:
        for dialogue_item in dialogue_dict.items():

            you_constraint = {}
            they_constraint = {}

            relationship_constraint = []
            season_constraint = []
            biome_constraint = []

            tags = dialogue_item[1]["tags"] if "tags" in dialogue_item[1] else []
            try:
                dialogue = dialogue_item[1]["intro"]
            except KeyError:
                try:
                    dialogue = dialogue_item[1]["intro_text"]
                except:
                    print(dialogue_item[0], "in", FILE, "has no intro or intro_text?")

            choice_blocks = {}

            if "intro_choices" in dialogue_item[1]:
                for i in dialogue_item[1].items():
                    if i[0] in ["tags", "intro"]:
                        continue
                    choice_blocks.update({i[0]: i[1]})

            newtags = []
            for i in tags:
                if i.lower() == "any":
                    continue
                i.replace(" ", "_")
                newtags.append(i)
            
            
            for item in newtags.copy():
                # CLUSTER TAGS
                # non they/you tags get put into they_cluster_constraint
                for cluster in cluster_tags:
                    if cluster in newtags:
                        newtags.remove(cluster)
                        if "cluster" not in they_constraint:
                            they_constraint["cluster"] = [cluster]
                        else:
                            they_constraint["cluster"].append(cluster)

                    if f"they_{cluster}" in newtags:
                        newtags.remove(f"they_{cluster}")
                        if "cluster" not in they_constraint:
                            they_constraint["cluster"] = [cluster]
                        else:
                            they_constraint["cluster"].append(cluster)
                    if f"you_{cluster}" in newtags:
                        newtags.remove(f"you_{cluster}")
                        if "cluster" not in you_constraint:
                            you_constraint["cluster"] = [cluster]
                        else:
                            you_constraint["cluster"].append(cluster)

                if item.startswith("min_plike"):
                    relationship_constraint.append(item.replace("min_plike", "min_platonic"))
                    newtags.remove(item)
                if item.startswith("min_plove"):
                    relationship_constraint.append(item.replace("min_plove", "min_platonic"))
                    newtags.remove(item)
                if item.startswith("min_rlike"):
                    relationship_constraint.append(item.replace("min_rlike", "min_romantic"))
                    newtags.remove(item)
                if item.startswith("min_rlove"):
                    relationship_constraint.append(item.replace("min_rlove", "min_romantic"))
                    newtags.remove(item)
                # STATUSES
                # non you/they go into you_status_constraint....
                # but i think people have been using it in both ways tbh
                for status in just_statuses:
                    if status.replace(" ", "") == item:
                        newtags.remove(item)
                        if "status" not in you_constraint:
                            you_constraint["status"] = [status]
                        else:
                            you_constraint["status"].append(status)
                    elif status == item.replace("_", " "):
                        newtags.remove(item)
                        if "status" not in you_constraint:
                            you_constraint["status"] = [status]
                        else:
                            you_constraint["status"].append(status)

                    if f"they_{status}" == item:
                        newtags.remove(item)
                        if "status" not in they_constraint:
                            they_constraint["status"] = [status]
                        else:
                            they_constraint["status"].append(status)
                    elif f"they_{status.replace(' ', '_')}" == item:
                        newtags.remove(item)
                        if "status" not in they_constraint:
                            they_constraint["status"] = [status]
                        else:
                            they_constraint["status"].append(status)
                    elif f"they_{status.replace(' ', '')}" == item:
                        newtags.remove(item)
                        if "status" not in they_constraint:
                            they_constraint["status"] = [status]
                        else:
                            they_constraint["status"].append(status)
                    if f"they_not_{status}" == item:
                        newtags.remove(item)
                        if "status" not in they_constraint:
                            they_constraint["status"] = ["not_" + status]
                        else:
                            they_constraint["status"].append(status)
                    elif f"they_not_{status.replace(' ', '_')}" == item:
                        newtags.remove(item)
                        if "status" not in they_constraint:
                            they_constraint["status"] = ["not_" + status]
                        else:
                            they_constraint["status"].append("not_" + status)
                    elif f"they_not_{status.replace(' ', '')}" == item:
                        newtags.remove(item)
                        if "status" not in they_constraint:
                            they_constraint["status"] = ["not_" + status]
                        else:
                            they_constraint["status"].append("not_" + status)

                    if f"you_{status}" == item:
                        newtags.remove(item)
                        if "status" not in you_constraint:
                            you_constraint["status"] = [status]
                        else:
                            you_constraint["status"].append(status)
                    elif f"you_{status.replace(' ', '_')}" == item:
                        newtags.remove(item)
                        if "status" not in you_constraint:
                            you_constraint["status"] = [status]
                        else:
                            you_constraint["status"].append(status)
                    elif f"you_{status.replace(' ', '')}" == item:
                        newtags.remove(item)
                        if "status" not in you_constraint:
                            you_constraint["status"] = [status]
                        else:
                            you_constraint["status"].append(status)
                    if f"you_not_{status}" == item:
                        newtags.remove(item)
                        if "status" not in you_constraint:
                            you_constraint["status"] = ["not_" + status]
                        else:
                            you_constraint["status"].append("not_" + status)
                    elif f"you_not_{status.replace(' ', '_')}" == item:
                        newtags.remove(item)
                        if "status" not in you_constraint:
                            you_constraint["status"] = ["not_" + status]
                        else:
                            you_constraint["status"].append("not_" + status)
                    elif f"you_not_{status.replace(' ', '')}" == item:
                        newtags.remove(item)
                        if "status" not in you_constraint:
                            you_constraint["status"] = ["not_" + status]
                        else:
                            you_constraint["status"].append("not_" + status)

                for item in they_age_tags:
                    age = item.replace('they_', '')
                    if item in newtags:
                        newtags.remove(item)
                        if age == "app":
                            age = "adolescent"
                        if "age" not in they_constraint:
                            they_constraint["age"] = [age]
                        else:
                            they_constraint["age"].append(age)

                for item in you_age_tags:
                    age = item.replace('you_', '')
                    if item in newtags:
                        newtags.remove(item)
                        if age == "app":
                            age = "adolescent"
                        if "age" not in you_constraint:
                            you_constraint["age"] = [item]
                        else:
                            you_constraint["age"].append(item)

                new_perma_tags = {
                    "only_XX_deaf": "deaf:any:true",
                    "XX_deaf": "deaf:any:false",
                    
                    "only_XX_born_deaf": "deaf:true:true",
                    "XX_born_deaf": "deaf:true:false",
                    
                    "only_XX_went_deaf": "deaf:false:true",
                    "XX_went_deaf": "deaf:false:false",

                    "XX_hearing": "hearing",

                    "only_XX_blind": "blind:any:true",
                    "XX_blind": "blind:any:false",
                    
                    "only_XX_born_blind": "blind:true:true",
                    "XX_born_blind": "blind:true:false",
                    
                    "only_XX_went_blind": "blind:false:true",
                    "XX_went_blind": "blind:false:false",

                    "XX_allergies": "allergies:any:true",
                    "XX_dizzy": "constantly dizzy:any:true",
                    "XX_nightmares": "constant nightmares:any:true",
                    "XX_crookedjaw": "crooked jaw:any:true",
                    "XX_failingeyesight": "failing eyesight:any:true",
                    "XX_onebadeye": "one bad eye:any:true",
                    "XX_lastinggrief": "lasting grief:any:true",
                    "XX_paralyzed": "paralyzed:any:true",
                    "XX_hearingloss": "hearing loss:any:true",
                    "XX_headaches": "persistent headaches:any:true",
                    "XX_raspylungs": "raspy lungs:any:true",
                    "XX_recurringshock": "recurring shock:any:true",
                    "XX_seizureprone": "seizure prone:any:true",
                    "XX_wastingdisease": "wasting disease:any:true",

                    "XX_recovering_from_birth": "recovering from birth",
                    "XX_ill": "illness:any",
                    "XX_injured": "injury:any",

                    "XX_grieving": "grief stricken",
                    "XX_guilty": "guilt",
                    "XX_starving": "starving",
                    "XX_pregnant": "pregnant"
                }

                for item in they_condition_tags:
                    condition = item.replace("they_", "")
                    newitem = item.replace("they", "XX")
                    if item in newtags:
                        newtags.remove(item)
                        if newitem in new_perma_tags:
                            if "condition" not in they_constraint:
                                they_constraint["condition"] = [new_perma_tags[newitem]]
                            else:
                                they_constraint["condition"].append(new_perma_tags[newitem])
                        else:
                            if "condition" not in they_constraint:
                                they_constraint["condition"] = [condition]
                            else:
                                they_constraint["condition"].append(condition)

                for item in you_condition_tags:
                    condition = item.replace("you_", "")
                    newitem = item.replace("you", "XX")
                    if item in newtags:
                        newtags.remove(item)
                        if newitem in new_perma_tags:
                            if "condition" not in you_constraint:
                                you_constraint["condition"] = [new_perma_tags[newitem]]
                            else:
                                you_constraint["condition"].append(new_perma_tags[newitem])
                        else:
                            if "condition" not in you_constraint:
                                you_constraint["condition"] = [condition]
                            else:
                                you_constraint["condition"].append(condition)

                #  the fucking rest of it
                for item in ["they_dead", "they_ur", "they_sc", "they_df"]:
                    tag = item.split("_")[1]
                    if item in newtags:
                        newtags.remove(item)
                        if tag == "dead":
                            tag = "any"
                        if "dead" not in they_constraint:
                            they_constraint["dead"] = [tag]
                        else:
                            they_constraint["dead"].append(tag)
                        

                for item in ["you_dead", "you_ur", "you_sc", "you_df"]:
                    tag = item.split("_")[1]
                    if item in newtags:
                        newtags.remove(item)
                        if tag == "dead":
                            tag = "any"
                        if "dead" not in you_constraint:
                            you_constraint["dead"] = [tag]
                        else:
                            you_constraint["dead"].append(tag)
                
                if "you_shunned" in newtags:
                    newtags.remove("you_shunned")
                    you_constraint["shunned"] = True
                if "both_shunned" in newtags:
                    you_constraint["shunned"] = True
                if "you_grieving" in newtags:
                    newtags.remove("you_grieving")
                    you_constraint["grieving"] = True
                if "you_forgiven" in newtags:
                    newtags.remove("you_forgiven")
                    you_constraint["forgiven"] = True
                
                if "they_shunned" in newtags:
                    newtags.remove("they_shunned")
                    they_constraint["shunned"] = True
                if "both_shunned" in newtags:
                    newtags.remove("both_shunned")
                    they_constraint["shunned"] = True
                if "they_grieving" in newtags:
                    newtags.remove("they_grieving")
                    they_constraint["grieving"] = True
                if "they_forgiven" in newtags:
                    newtags.remove("they_forgiven")
                    they_constraint["forgiven"] = True

                for item in ["they_clanfounder",
                            "they_clanborn",
                            "they_outsiderroots",
                            "they_half-clan",
                            "they_formerlyaloner",
                            "they_formerlyarogue",
                            "they_formerlyakittypet",
                            "they_formerlyaoutsider",
                            "they_originallyfromanotherclan",
                            "they_orphaned",
                            "they_abandoned",
                            "they_ancientspirit"
                            ]:
                    tag = item.split("_")[1]
                    if item in newtags:
                        newtags.remove(item)
                        if "backstory" not in they_constraint:
                            they_constraint["backstory"] = [tag]
                        else:
                            they_constraint["backstory"].append(tag)
                

                for item in ["you_clanfounder",
                            "you_clanborn",
                            "you_outsiderroots",
                            "you_half-clan",
                            "you_formerlyaloner",
                            "you_formerlyarogue",
                            "you_formerlyakittypet",
                            "you_formerlyaoutsider",
                            "you_originallyfromanotherclan",
                            "you_orphaned",
                            "you_abandoned",
                            "you_ancientspirit"
                            ]:
                    tag = item.split("_")[1]
                    if item in newtags:
                        newtags.remove(item)
                        if "backstory" not in you_constraint:
                            you_constraint["backstory"] = [tag]
                        else:
                            you_constraint["backstory"].append(tag)
                
                for item in relationship_values:
                    for tag in newtags.copy():
                        if item in tag:
                            newtags.remove(tag)
                            rel_tag = ""
                            if tag in [
                                "platonic_love", "platonic_like", "romantic_love", "romantic_like", "hate", "jealousy",
                                "dislike", "admiration", "respect", "trust", "comfort"
                                ]:
                                if "_" in tag:
                                    if tag in ["platonic_love", "romantic_love", ]:
                                        rel_tag = f"min_{tag.split('_')[0]}_50"
                                    if tag in ["platonic_like", "romantic_like", "dislike"]:
                                        rel_tag = f"min_{tag.split('_')[0]}_20"
                                elif tag == "hate":
                                    rel_tag = "min_dislike_50"
                                elif tag == "admiration":
                                    rel_tag = "min_respect_50"
                                else:
                                    rel_tag = f"min_{tag}_50"
                            else:
                                rel_tag = tag
                            relationship_constraint.append(rel_tag.replace(" ", "_"))
            
            for tag in newtags.copy():
                if "they_deadfor" in tag:
                    newtags.remove(tag)
                    if "dead" in they_constraint:
                        they_constraint["dead"].append(tag)
                    else:
                        they_constraint["dead"] = [tag]
                if "you_deadfor" in tag:
                    newtags.remove(tag)
                    if "dead" in you_constraint:
                        you_constraint["dead"].append(tag)
                    else:
                        you_constraint["dead"] = [tag]
            
            if "flirt" in newtags:
                newtags.remove("flirt")

            if "sc_faith" in newtags:
                newtags.remove("sc_faith")
                they_constraint["min_max_faith"] = [0, 9]
            if "df_faith" in newtags:
                newtags.remove("df_faith")
                they_constraint["min_max_faith"] = [-9, 0]

            for season in ["leafbare", "leaffall", "greenleaf", "newleaf"]:
                if season in newtags:
                    newtags.remove(season)
                    season_constraint.append(season)

            for biome in ["forest", "mountainous", "plains", "beach", "wetlands", "desert"]:
                if biome in newtags:
                    newtags.remove(biome)
                    biome_constraint.append(biome)

            if "they_outside" in newtags:
                newtags.remove("they_outside")

            if "they_guide" in newtags:
                newtags.remove("they_guide")
                if "status" in you_constraint:
                    you_constraint["status"].append("guide")
                else:
                    you_constraint["status"] = ["guide"]

            if "you_dftrainee" in newtags:
                newtags.remove("you_dftrainee")
                if "status" in you_constraint:
                    you_constraint["status"].append("df_trainee")
                else:
                    you_constraint["status"] = ["df_trainee"]
            if "you_notdftrainee" in newtags:
                newtags.remove("you_not_df_trainee")
                if "status" in you_constraint:
                    you_constraint["status"].append("not_df_trainee")
                else:
                    you_constraint["status"] = ["not_df_trainee"]

            if "they_dftrainee" in newtags:
                newtags.remove("they_dftrainee")
                if "status" in they_constraint:
                    they_constraint["status"].append("df_trainee")
                else:
                    they_constraint["status"] = ["df_trainee"]
            if "they_not_dftrainee" in newtags:
                newtags.remove("they_not_dftrainee")
                if "status" in they_constraint:
                    they_constraint["status"].append("not_df_trainee")
                else:
                    they_constraint["status"] = ["not_df_trainee"]

            # young elder
            if "they_young_elder" in newtags:
                newtags.remove("they_young_elder")
                if "status" in they_constraint:
                    they_constraint["status"].append("elder")
                else:
                    they_constraint["status"] = ["elder"]
                if "age" in they_constraint:
                    they_constraint["age"].append("kitten")
                    they_constraint["age"].append("adolescent")
                    they_constraint["age"].append("young adult")
                    they_constraint["age"].append("adult")
                else:
                    they_constraint["age"] = ["kitten", "adolescent", "young adult", "adult"]
            if "you_young_elder" in newtags:
                newtags.remove("you_young_elder")
                if "status" in you_constraint:
                    you_constraint["status"].append("elder")
                else:
                    you_constraint["status"] = ["elder"]
                if "age" in you_constraint:
                    you_constraint["age"].append("kitten")
                    you_constraint["age"].append("adolescent")
                    you_constraint["age"].append("young adult")
                    you_constraint["age"].append("adult")
                else:
                    you_constraint["age"] = ["kitten", "adolescent", "young adult", "adult"]
            
            # no kit
            if "no_kit" in newtags:
                newtags.remove("no_kit")
                if "age" in you_constraint:
                    you_constraint["age"].append("not_kitten")
                else:
                    you_constraint["age"] = ["not_kitten"]
                if "age" in they_constraint:
                    they_constraint["age"].append("not_kitten")
                else:
                    they_constraint["age"] = ["not_kitten"]
            if "no_newborn" in newtags:
                newtags.remove("no_newborn")
                if "age" in you_constraint:
                    you_constraint["age"].append("not_newborn")
                else:
                    you_constraint["age"] = ["not_newborn"]
                if "age" in they_constraint:
                    they_constraint["age"].append("not_newborn")
                else:
                    they_constraint["age"] = ["not_newborn"]

            skill_list = [
                'teacher', 'hunter', 'fighter', 'runner', 'climber', 'swimmer', 'speaker',
                'mediator1', 'clever', 'insightful', 'sense', 'kitsitter', 'story', 'lore',
                'camp', 'healer', 'star', 'omen', 'dream', 'clairvoyant', 'prophet',
                'ghost', 'explorer', 'tracker', 'artistan', 'guardian', 'tunneler', 'navigator',
                'song', 'grace', 'clean', 'innovator', 'comforter', 'matchmaker', 'thinker',
                'cooperative', 'scholar', 'time', 'treasure', 'fisher', 'language', 'sleeper', 'dark'
            ]
            for skill in skill_list:
                if f"they_{skill}" in newtags:
                    newtags.remove(f"they_{skill}")
                    they_constraint["skill"] = [str(skill.upper() + ",1")]
                if f"you_{skill}" in newtags:
                    newtags.remove(f"you_{skill}")
                    you_constraint["skill"] = [str(skill.upper() + ",1")]

            # lowercasing them
            for tag in newtags:
                tag = tag.lower()

            for status in just_statuses:
                if FILE == status:
                    if ( ("status" in they_constraint and
                        status not in they_constraint["status"]) or
                        "status" not in they_constraint
                        ):
                        if "status" not in they_constraint:
                            they_constraint["status"] = [tag]
                        else:
                            they_constraint["status"].append(tag)
            
            # testing
            # puts all y_c/t_c stuff into a single constraint. closer to the current tag system
            # yc_list = []
            # for name, tags in you_constraint.items():
            #     if isinstance(tags, list):
            #         for i in tags:
            #             yc_list.append(i)
            #     elif isinstance(tags, bool):
            #         yc_list.append(name)
            # you_constraint = yc_list
            # tc_list = []
            # for name, tags in they_constraint.items():
            #     if isinstance(tags, list):
            #         for i in tags:
            #             tc_list.append(i)
            #     elif isinstance(tags, bool):
            #         tc_list.append(name)
            # they_constraint = tc_list

            dialogue_block = {
                    "y_c": you_constraint,
                    "t_c": they_constraint,
                    "season": season_constraint,
                    "biome": biome_constraint,
                    "relationship": relationship_constraint,
                    "tags": newtags,
                    "intro": dialogue,
                    }
            if choice_blocks:
                for block in choice_blocks.items():
                    dialogue_block.update({block[0]: block[1]})

            new_dict = {
                dialogue_item[0]: dialogue_block
                }
            
            dict_copy = new_dict.copy()

            # replacing abbrevs with hyphenated versions
            # dislike_r_w => dislike-r_w
            # this will help clean up the pronoun test (hopefully..........) and looks a bit better
            for text in dict_copy.items():
                dialogue_ID = text[0]
                dialogue_dict = text[1]
                for block in dialogue_dict.items():
                    if block[0] in ["tags", "relationship", "t_c", "y_c", "season", "biome"]:
                        continue
                    dialogue = block[1]
                    updated_block_contents = []
                    if isinstance(dialogue, list):
                        # actual dialogue lines
                        for string in dialogue:
                            new_string = underscore_replace(string, dialogue_id=dialogue_ID)

                            updated_block_contents.append(new_string)
                    else:
                        # choice dicts
                        # accesses the choice button text to replace abbrevs then rebuilts the dict
                        choice_copy = dialogue.copy()
                        for string in dialogue:
                            choicestuff = dialogue[string]
                            try:
                                text = choicestuff["text"]
                                next_scene = choicestuff["next_scene"]
                            except Exception as e:
                                print(dialogue_ID, "in", FILE, "is formatted incorrectly!")
                                print(e)

                            new_text = underscore_replace(text)

                            choice_copy.update(
                                {
                                    string: {
                                        "text": new_text,
                                        "next_scene": next_scene
                                    }
                                }
                            )

                        updated_block_contents = choice_copy

                    new_dict[dialogue_ID][block[0]] = updated_block_contents

                    # print("UPDATED TO:", new_dict[block[0]])

            # removing empty blocks
            for item in new_dict.items():
                for i in item[1].copy():
                    if item[1][i] == []:
                        item[1].pop(i)

            new_dialogue_dict.update(new_dict)

        # now here go through everythign AGAIN to rewrite into the new, FINAL format
        # because i dont want to redo the replacing w hyphens thing. that was annoying

        for dialogue_ID, dialogue_contents in new_dialogue_dict.items():
            they_cluster = dialogue_contents["they_cluster"] if "they_cluster" in dialogue_contents else []
            they_status = dialogue_contents["they_status"] if "they_status" in dialogue_contents else []
            they_condition = dialogue_contents["they_condition"] if "they_condition" in dialogue_contents else []
            
            you_cluster = dialogue_contents["you_cluster"] if "you_cluster" in dialogue_contents else []
            you_status = dialogue_contents["you_status"] if "you_status" in dialogue_contents else []
            you_condition = dialogue_contents["you_condition"] if "you_condition" in dialogue_contents else []

            relationship = dialogue_contents["relationship"] if "relationship" in dialogue_contents else []
            d_tags = dialogue_contents["tags"] if "tags" in dialogue_contents else []


    if overwrite is False:
        new_dialogue_dict = dialogue_dict

    with open(file_path, 'w') as json_file:
        json.dump(new_dialogue_dict, json_file, indent=4, separators=(',', ': '))


# for FILE in file_names:
#     print(FILE, file_nums[FILE])
# print(num)
# print("INSULTS:", insult_num)