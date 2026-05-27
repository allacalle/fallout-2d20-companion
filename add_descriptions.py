#!/usr/bin/env python3
"""Extract descriptions from PDF and add them to JSON data files."""

import json, os, pdfplumber, re

DATA_DIR = "data"
PDF_FILE = "Fallout - The Role Playing Game.pdf"

def load_json(name):
    with open(os.path.join(DATA_DIR, name)) as f:
        return json.load(f)

def save_json(name, data):
    with open(os.path.join(DATA_DIR, name), 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

# Armor class descriptions (from PDF pages 135-137)
ARMOR_DESCRIPTIONS = {
    "raider": (
        "Makeshift armor employed by raiders and other cutthroat types across the wastes. "
        "It varies considerably in quality and appearance but tends to be made of scrap metal rudely battered into shape, "
        "reinforced by metal bars, wire, and leather straps. This barbaric appearance is often bolstered by grisly trophies "
        "such as skulls or other body parts."
    ),
    "leather": (
        "Tanned and toughened animal hide, shaped into crude armor pieces and held together with leather straps and stitching. "
        "Leather armor provides decent protection against energy attacks compared to metal armor, but is less effective against physical impacts."
    ),
    "metal": (
        "Shaped metal plating held together—and held on—with leather or cloth straps, which provide decent protection from physical impacts "
        "such as melee attacks and gunshots, but less protection against energy attacks, as the metal plating conducts heat."
    ),
    "combat": (
        "Specially made armor pieces, designed pre-War and issued to the soldiers of the U.S. Armed Forces. "
        "It was constructed to keep the wearer protected from physical and energy attacks alike without being cumbersome or awkward to wear. "
        "The Brotherhood of Steel tend to use Combat armor for their troops when Power Armor is unavailable or unsuitable for the mission."
    ),
    "synth": (
        "Developed by The Institute, Synth armor is distinctive and provides excellent protection, especially from energy weapons, "
        "but can only really be found within the Commonwealth and other locations where Institute synths travel. "
        "The rarity of its manufacture means that it's hard to acquire for anyone not on good terms with the Institute, and expensive even then."
    ),
    "vault_security": (
        "Consisting of a long bulletproof apron and shoulder pads, plus an accompanying shock-resistant helmet, "
        "this armor was issued in small quantities to every vault for those vault-dwellers chosen to act as security personnel. "
        "It provides modest protection and isn't especially bulky, but it is unlikely to stand up to heavy combat, "
        "simply because vaults were expected to be controlled environments, lacking in the heavy armaments found outside."
    ),
}

# Headgear descriptions (from PDF pages 127-129)
HEADGEAR_DESCRIPTIONS = {
    "Formal Hat": (
        "A smart-looking hat, that'll look the part adorning your head during a business engagement or formal event. "
        "Or just because you like how it looks and it keeps the sun off your face. Many examples are somewhat battered and worn "
        "from neglect and ill-use, but they're still functional."
    ),
    "Gas Mask": (
        "A rubber and leather mask with a plastic visor, which fits with an air-tight seal over the face. "
        "The front of the mask contains a filter which cleanses the air of contaminants like dust and gas."
    ),
    "Hard Hat": (
        "A light metal or plastic hat intended to protect the head from bumps and collisions in a busy industrial workplace "
        "or construction site. Not really intended to protect from combat, but if you're lacking a helmet, a hard hat is better than nothing."
    ),
    "Hood or Cowl": (
        "A cloth or leather covering for the head and neck. Provides a little protection from the elements, and easily combined "
        "with a mask or kerchief to cover the mouth and nose to keep dust and fumes out. Handy in the wasteland if you're caught "
        "outside without better protection."
    ),
    "Sack Hood": (
        "A simple cloth sack pulled over the head, with holes cut for vision and breathing. "
        "A crude and unsettling garment, offering minimal protection but serving to hide the wearer's identity."
    ),
    "Welder's Visor": (
        "A protective visor with a dark lens designed to shield the eyes from the intense light of welding. "
        "The heavy construction provides reasonable protection against impacts as well."
    ),
    "Army Helmet": (
        "A helmet made of metal, plastic, and light ceramics, designed to protect a soldier's head from shrapnel. "
        "The helmet is lined with supportive padding to ensure a secure fit."
    ),
    "Brotherhood of Steel Hood": (
        "The matching headpiece for the Brotherhood of Steel uniform, this close-fitting hood was developed before the Great War "
        "for wearers of Power Armor. It is designed to plug into the helmet of a suit of Power Armor, providing a closer interface "
        "to the armor's systems, as well as containing an earpiece and microphone for the armor's internal radio."
    ),
    "Brotherhood Scribe's Hat": (
        "This lightweight leather cap and goggles are provided as an accompaniment to the Brotherhood Scribe's Armor, "
        "to protect the head from hazardous conditions."
    ),
    "Casual Hat": (
        "A simple, lightweight hat, normally with a peak or brim to keep the sunlight out of the wearer's eyes."
    ),
}

# Consumable descriptions (from PDF pages 158-173)
CONSUMABLE_DESCRIPTIONS = {
    # FOOD items (pages 158-161)
    "BlamCo Brand Mac and Cheese": (
        "A packaged box of dried macaroni pasta and a packet of powdered cheese mix. "
        "A pre-War staple that's still perfectly edible decades later."
    ),
    "Bottle of Water (Purified)": (
        "A sealed bottle of clean, purified water. Safe to drink and free from contaminants and radiation."
    ),
    "Brahmin Steak": (
        "A grilled piece of meat from a brahmin. The closest thing to a pre-War steak you're likely to find, "
        "a good piece of grilled brahmin makes for a satisfying meal."
    ),
    "Carrot": (
        "A root vegetable grown in soil. Provides decent nutrition and is relatively easy to grow. A staple of wasteland agriculture."
    ),
    "Carrot Soup": (
        "A simple soup made with carrot as its main ingredient. Hearty and filling."
    ),
    "Cram": (
        "A can of processed meat, typically containing a mixture of brahmin, radstag, and other meats. "
        "The can is sealed for preservation and can last for decades."
    ),
    "Crispy Squirrel Bits": (
        "Chunks of squirrel meat cooked until crispy. A decent snack, if not particularly filling."
    ),
    "Deathclaw Egg": (
        "The egg of a deathclaw. Extremely dangerous to acquire, but highly prized for its nutritional value."
    ),
    "Deathclaw Egg Omelette": (
        "An omelette made from a deathclaw egg. A legendary meal that provides exceptional nourishment."
    ),
    "Deathclaw Meat": (
        "Meat taken from a slain deathclaw. Extremely dangerous to obtain, but highly nutritious and prized across the wasteland."
    ),
    "Deathclaw Steak": (
        "A cooked slab of deathclaw meat. The process of cooking has enhanced its nutritional value and eliminated the radiation hazard."
    ),
    "Fancy Lads Snack Cakes": (
        "A box of pre-War packaged snack cakes, filled with a sweet, creamy center. Surprisingly well-preserved despite their age."
    ),
    "Fried Radroach": (
        "A cooked radroach, prepared for eating. While not the most appetizing meal, it provides decent sustenance in a pinch."
    ),
    "Grilled Radstag": (
        "A cooked portion of radstag meat. The lean, gamey meat provides nourishment and a feeling of vitality."
    ),
    "Grilled Herring": (
        "A fish grilled over an open flame. Simple but effective wasteland fare."
    ),
    "Iguana on a Stick": (
        "A skewer of iguana meat roasted over a fire. A common street food in many settlements."
    ),
    "Iguana Bits": (
        "Small pieces of dried or cooked iguana meat. A lightweight, portable source of protein."
    ),
    "Iguana Soup": (
        "A simple soup made with iguana meat and vegetables. Warm and filling."
    ),
    "Inspirational Speech by President Eden": (
        "A pre-War recording or transcript of a speech by President John Henry Eden. "
        "Listening to or reading it fills you with a sense of purpose and determination."
    ),
    "InstaMash": (
        "A packet of dehydrated mashed potatoes. Just add water (heated or not) and you have a quick, filling meal."
    ),
    "Mac and Cheese (Box)": (
        "A box of pre-War macaroni and cheese mix. The cheese powder may have lost some of its flavor, "
        "but it's still a comforting meal."
    ),
    "Mirelurk Cake": (
        "A dense cake or patty made from ground mirelurk meat. Surprisingly tasty and filling."
    ),
    "Mirelurk Egg": (
        "The egg of a mirelurk. Prized for its rich flavor and nutritional content."
    ),
    "Mirelurk Egg Omelette": (
        "An omelette made from a mirelurk egg. Said to sharpen the mind and improve focus."
    ),
    "Mirelurk Jerky": (
        "Dried, cured strips of mirelurk meat. A long-lasting source of protein that travels well."
    ),
    "Mirelurk Meat": (
        "Meat taken from inside the carapace of a mirelurk. Difficult to extract but delicious and nutritious."
    ),
    "Mirelurk Steamer Claws": (
        "The claws of a mirelurk, steamed and prepared for eating. A true delicacy in the wasteland."
    ),
    "Mole Rat Meat": (
        "Meat taken from a mole rat. Not the most appetizing food, but it's edible and provides sustenance."
    ),
    "Mole Rat Chunks": (
        "Chopped and cooked pieces of mole rat meat. Better than eating it raw, but still an acquired taste."
    ),
    "Mutfruit": (
        "Pronounced 'mute-fruit', and short for mutated fruit, mutfruit is a mutated form of apple, "
        "which comes in several different varieties depending on where you are."
    ),
    "Mutant Hound Chops": (
        "Cooked chops of mutant hound meat. Still not the tastiest food, but no longer hazardous."
    ),
    "Mutant Hound Meat": (
        "A cut of meat taken from a dead mutant hound. This meat's off-green color and lumpy texture suggests "
        "that it would be quite unpleasant to eat."
    ),
    "Pork 'n' Beans": (
        "A can containing a complete meal: beans stewed in a tomato sauce with chunks of cured pork belly. "
        "The tin may be slightly rusted, but the contents are still edible."
    ),
    "Potato Crisps": (
        "A can of salted or flavored potato chips, sealed in an inert environment for freshness. "
        "A common snack pre-War, still found in most places where people lived or worked."
    ),
    "Potted Meat": (
        "A small metal tin of mixed processed meat, typically containing mixtures of meat from brahmin, radstags, "
        "mole rats, mongrel dogs, and anything else the maker can get their hands on."
    ),
    "Queen Mirelurk Egg": (
        "An exceptionally rare and large egg from a queen mirelurk. Extremely dangerous to obtain, "
        "but prized as one of the finest delicacies in the wasteland."
    ),
    "Queen Mirelurk Steamer Claws": (
        "The massive claws of a queen mirelurk, steamed and prepared. A legendary meal worthy of wasteland royalty."
    ),
    "Radroach Egg": (
        "The egg of a radroach. Small and unappetizing, but edible in a pinch."
    ),
    "Radroach Meat": (
        "Meat taken from a radroach. Not particularly tasty, but it's a common source of protein in the wasteland."
    ),
    "Radscorpion Egg": (
        "The egg of a radscorpion. Not easy to get hold of, as they tend to be found in places where there are radscorpions."
    ),
    "Radscorpion Egg Omelette": (
        "Made from a radscorpion egg, these omelettes are highly prized by those who make considerable use of combat drugs, "
        "as something about the food cleanses the body to remove chemical dependencies and addictions."
    ),
    "Radscorpion Meat": (
        "Meat taken from inside the carapace of a radscorpion, normally from the tail or one of the legs. "
        "Difficult to obtain, as it requires killing a radscorpion."
    ),
    "Radscorpion Steak": (
        "A cooked slab of radscorpion meat. The process of cooking has reduced the radiation below dangerous levels "
        "and enhanced the nutritional value."
    ),
    "Radstag Meat": (
        "Meat taken from a radstag, a mutated deer-like creature. Lean and gamey, it provides good nutrition."
    ),
    "Radstag Stew": (
        "A hearty stew made with radstag meat and vegetables. Warming and satisfying."
    ),
    "Razorgrain": (
        "A tall, fast-growing grass similar to wheat, which can be ground down to make flour for making bread and other staple foods."
    ),
    "Ribeye Steak": (
        "A grilled piece of meat from a brahmin. The closest thing to a pre-War steak you're likely to find."
    ),
    "Roasted Mirelurk Meat": (
        "A cooked portion of meat from a mirelurk. Though not to the same extent as the softshell meat, "
        "roasted mirelurk meat invigorates the body and mind."
    ),
    "Salisbury Steak": (
        "A ready-to-eat meal of ground beef mixed with breadcrumbs, onion, and egg, served with gravy. "
        "Pre-packaged, preserved, and sealed for freshness."
    ),
    "Squirrel Bits": (
        "A few scraps and chunks of squirrel meat. Squirrels, not being especially large creatures, do not have much meat on them."
    ),
    "Squirrel on a Stick": (
        "Chunks of squirrel meat skewered on a thin piece of wood for cooking, and then roasted over an open flame. "
        "Not enough meat for a decent meal, but certainly enough for a snack."
    ),
    "Squirrel Stew": (
        "Chunks of squirrel meat, along with carrot, tato, and some bloodleaf, cooked together to create a thick stew. "
        "More filling and appetizing than the ingredients individually."
    ),
    "Stingwing Filet": (
        "A cooked piece of stingwing meat. Not the most appetizing of foods, but surprisingly useful for those surviving "
        "in the wastelands, as it can sharpen the senses."
    ),
    "Stingwing Meat": (
        "Meat taken from the body of a stingwing, a mutated scorpionfly with a nasty sting. "
        "Doesn't look especially tasty, but it cooks reasonably well."
    ),
    "Sweet Roll": (
        "A small, sweetened pastry or baked confection normally made as a treat for children or people who need a bit of cheering up."
    ),
    "Tarberry": (
        "Small purple berries of the Tarberry plant, a water-grown crop similar to pre-War cranberries. "
        "A useful ingredient in several recipes."
    ),
    "Tato": (
        "A mutated hybrid of the pre-War tomato and potato plants, with the stem and reddish skin of the former "
        "and the brownish flesh of the latter. Tatos provide decent nutrition, but taste disgusting."
    ),
    "Vegetable Soup": (
        "A simple soup made with carrot and tato. A reasonably filling meal, sating both hunger and thirst, "
        "while also helping to fortify the body against radiation poisoning for a while."
    ),
    "Yao Guai Meat": (
        "Dangerous meat to obtain, Yao Guai meat comes from the bodies of slain Yao Guai, a ferocious mutated form of bear "
        "that roams the wastelands. The meat is highly prized and nutritious."
    ),
    "Yao Guai Ribs": (
        "A rack of ribs made with Yao Guai meat. Both a satisfying meal and inspire a sense of invincibility, "
        "while also boosting your tolerance for pain for a short while."
    ),
    "Yao Guai Roast": (
        "A roasted piece of Yao Guai meat cooked with carrot and tato. An extremely filling and satisfying meal, "
        "and many have claimed that it heightens their killer instinct."
    ),
    "Yum-Yum Deviled Eggs": (
        "Hard-boiled eggs stuffed with a spicy filling, which were preserved and sealed for freshness before the Great War."
    ),

    # Additional FOOD items (pages 153-158)
    "Baked Bloatfly": (
        "A bloatfly cooked over an open fire. Not particularly appetizing, but edible."
    ),
    "Bloatfly Meat": (
        "Meat taken from a bloatfly. Not particularly appetizing, but it's a source of protein."
    ),
    "Bloodbug Meat": (
        "Meat taken from a bloodbug. Slimy and unappealing, but edible when cooked."
    ),
    "Bloodbug Steak": (
        "A cooked slab of bloodbug meat. Surprisingly nutritious despite its unappealing origin."
    ),
    "Brahmin Meat": (
        "A cut of meat taken from a brahmin. A reliable source of protein in the wasteland."
    ),
    "Brain Fungus": (
        "A mutated fungus that grows in dark, damp places. Consuming it raw has adverse effects on mental clarity."
    ),
    "Canned Dog Food": (
        "A can of processed meat-based food, intended for dogs. Edible in a pinch, but deeply unappealing."
    ),
    "Cooked Softshell Meat": (
        "The softer meat from mirelurks, cooked into a rough steak. A high-energy meal, those who eat cooked softshell meat are often invigorated and eager for action for a while afterwards."
    ),
    "Corn": (
        "A highly versatile crop cultivated across the Americas for centuries. Corn remains largely unchanged by the War, and it remains a staple of wasteland agriculture."
    ),
    "Daddy-O": (
        "A pre-War recreational drug that alters perception and heightens mental acuity, but can lead to confusion and paranoia."
    ),
    "Dandy Boy Apples": (
        "Candied apples produced by the Dandy Boy company. An extremely sweet fruit-based snack packaged in a cardboard box."
    ),
    "Deathclaw Omelette": (
        "An omelette made from a deathclaw egg. In addition to being highly nutritious, it stimulates the natural healing processes of the body."
    ),
    "Food Paste": (
        "A flavorless mush, garish pink in color, developed by Vault-Tec as part of the Nutritional Alternative Paste Program. Fortified with vitamins and minerals, it remains unspoiled for over a century."
    ),
    "Glowing Fungus": (
        "A bioluminescent fungus that grows in irradiated areas. It has medicinal properties but also contains significant radiation."
    ),
    "Gourd": (
        "A large edible fruit, which is fleshy with a hard skin, like a pumpkin. The pulp inside can be eaten or used in cooking."
    ),
    "Grilled Radroach": (
        "A grilled chunk of meat taken from a radroach. Not especially appetizing, but sufficiently nutritious for those with few other choices."
    ),
    "Gum Drops": (
        "A pre-War confection of small drops of congealed gelatin, sweetened and flavored. The most common variety to survive the War were labelled as 'radioactive' for their powerful sour flavor."
    ),
    "Hubflower": (
        "A mutated flower that grows in the wasteland. It has mild healing properties when consumed."
    ),
    "Institute Food Packet": (
        "A small white box of food marked with the symbol of the Institute. Each box contains enriched ration bars filled with essential nutrients."
    ),
    "Melon": (
        "A large, green, juicy fruit with a hard outer rind. Once cut open, melons are very satisfying, sating hunger and quenching thirst."
    ),
    "Mirelurk Queen Steak": (
        "The rare, nutrient-rich meat of a mirelurk Queen. When properly prepared, it can fortify the body and provide a surge of health and vitality."
    ),
    "Mongrel Dog Meat": (
        "A chunk of meat taken from a mongrel dog. Can be cooked to make Mutt Chops."
    ),
    "Mutt Chops": (
        "Cuts of mongrel dog meat cooked to make them more nutritious and edible."
    ),
    "Noodle Cup": (
        "A simple cup of noodle soup. Moderately filling and thirst-quenching, and simple enough to make if you can find the ingredients."
    ),
    "Perfectly Preserved Pie": (
        "A slice of fruit pie shielded from the radioactive environment since before the Great War. Copious preservatives keep it as edible as the day it was made."
    ),
    "Refreshing Beverage": (
        "A pre-War sports drink designed to rehydrate and restore energy. Its electrolytic properties make it highly effective at revitalizing the body."
    ),
    "Silt Bean": (
        "A legume that grows in muddy or silty soil. Provides decent nutrition and can be used in various recipes."
    ),
    "Sugar Bombs": (
        "A pre-War breakfast cereal heavily sweetened with sugar. The box may have seen better days, but the contents are still edible, if absurdly sweet."
    ),

    # BEVERAGE items (pages 162-165)
    "Beer": (
        "One of the oldest beverages created by humans, beer is a carbonated alcoholic drink made from fermented cereal grains, "
        "popular pre-War to relax after a hard day's work."
    ),
    "Blood Pack": (
        "A bag of pre-War blood, intended for medical transfusions. Some wastelanders drink it for its nutritional content, "
        "though it's hardly a pleasant beverage."
    ),
    "Bourbon": (
        "A distinctly American type of whiskey, bourbon is a barrel-aged, distilled spirit made mainly of corn. "
        "Pre-War, those who favored it tended to get a reputation as being tough or rugged."
    ),
    "Brahmin Milk": (
        "Milk from a brahmin. This drink is a true lifesaver, as it has properties that cleanse radiation poisoning from the body."
    ),
    "Dirty Wastelander": (
        "An extremely potent alcoholic beverage, made from a blend of whiskey, Nuka-Cola, and Mutfruit, "
        "which has much the same effect as most alcoholic drinks, just moreso."
    ),
    "Dirty Water": (
        "Water collected from rivers, lakes, swimming pools, and any other unfiltered water source. "
        "It's not recommended to drink dirty water without filtering or purifying it first."
    ),
    "Glowing Blood Pack": (
        "A blood pack that has been contaminated with radioactive materials, causing it to glow. "
        "It still has some medical utility but at the cost of radiation exposure."
    ),
    "Irradiated Blood": (
        "A blood bag filled with discolored—often green—blood-like fluid. About as useful as a normal blood pack, "
        "but highly irradiated."
    ),
    "Melon Juice": (
        "Juice made from pressing the pulp of a melon. A refreshing and healthy drink which promotes the body's natural healing."
    ),
    "Moonshine": (
        "High-proof distilled spirits produced in an illicit or makeshift manner. Due to their unorthodox origins, "
        "moonshine can be dangerous to consume, often contaminated with dangerous chemicals."
    ),
    "Mutfruit Juice": (
        "Juice made from pressing the pulp of a mutfruit. A sweet and energizing beverage."
    ),
    "Nuka-Cola": (
        "The flagship beverage of the Nuka-Cola Corporation, this carbonated soft drink is instantly recognizable "
        "by its distinctive brown glass bottle and sweet, refreshing taste."
    ),
    "Nuka-Cherry": (
        "Produced by the Nuka-Cola Corporation after it bought the patent for a rival beverage, "
        "Nuka-Cherry is a blend of the typical Nuka-Cola recipe with a distinctive cherry flavoring and a bright red color."
    ),
    "Nuka-Cola Quantum": (
        "Introduced the same day the bombs fell, Nuka-Cola Quantum was the newest flavor, "
        "with twice the calories, twice the carbohydrates, twice the caffeine, and twice the taste. "
        "The drink's distinctive blue glow comes from a safe isotope additive."
    ),
    "Purified Water": (
        "Water which has been cleansed of any contaminants or radiation. Sometimes found in sealed cans or bottles in the wasteland."
    ),
    "Rum": (
        "A liquor made from fermenting then distilling sugarcane molasses. Rum has strong historic ties to naval and maritime traditions."
    ),
    "Tarberry Juice": (
        "Juice made from pressing tarberries. Drinking Tarberry juice has a potent stimulant effect, "
        "making the drinker energetic and ready for action."
    ),
    "Tato Juice": (
        "Juice made from pressing Tatos. Despite the unpleasant taste, Tato juice allows the drinker to dig more deeply "
        "into reserves of stamina and push themselves further."
    ),
    "Vodka": (
        "A clear distilled alcoholic beverage, made from fermented rye, wheat, potatoes, or sugar beet molasses."
    ),
    "Whiskey": (
        "A triple-distilled alcoholic beverage made using grain mash. Some wasteland distilleries exist producing "
        "post-War versions using corn and other available grains."
    ),
    "Wine": (
        "An alcoholic beverage made from fermented fruits, typically grapes. Pre-War bottles are still found "
        "in cellars and liquor stores across the wasteland."
    ),

    # CHEM items (pages 166-172)
    "Addictol": (
        "A powerful and effective pre-War medicine which cleanses the body of the effects of addiction "
        "and the withdrawal symptoms that accompany it."
    ),
    "Antibiotics": (
        "A dose of potent, broad-spectrum antibiotics that'll help clear out pretty much any infection or disease."
    ),
    "Berry Mentats": (
        "A portion of Mentats reformulated to promote brain activity and memory."
    ),
    "Buffout": (
        "A powerful and quick-acting steroid which gained popularity with athletes prior to the Great War. "
        "For a few minutes, it makes one stronger and tougher."
    ),
    "Buffjet": (
        "A potent cocktail of Buffout and Jet, combining the strength-enhancing effects of steroids "
        "with the accelerated reflexes of Jet."
    ),
    "Bufftats": (
        "An addictive cocktail of Buffout steroids and Mentats, heightening both physical prowess and awareness."
    ),
    "Calmex": (
        "A light tranquilizer used to calm the nerves. It isn't potent enough to function as a painkiller, "
        "but a dose can quiet a troubled mind."
    ),
    "Day Tripper": (
        "A mild pre-War relaxant and hallucinogen, Day Tripper was favored by Americans seeking a brief escape from reality. "
        "The resulting high made users more laid-back and relaxed."
    ),
    "Fury": (
        "An extremely powerful combat stimulant, Fury grants users a sense of invincibility, rendering them nearly immune to pain "
        "and recklessly dangerous in melee combat."
    ),
    "Grape Mentats": (
        "A variant of Mentats that enhances social grace and persuasiveness."
    ),
    "Healing Salve": (
        "A salve or ointment which can be applied to reduce pain and speed recovery from injury, "
        "typically made from several natural herbal ingredients."
    ),
    "Jet": (
        "An inhaled stimulant which creates an altered state of consciousness where time appears to slow, "
        "heightening reflexes and allowing the user to act more quickly during a moment of crisis."
    ),
    "Jet Fuel": (
        "A volatile variant of Jet, Jet Fuel provides a massive burst of energy in the user, "
        "allowing them to act more swiftly and decisively."
    ),
    "Med-X": (
        "A potent opiate analgesic which significantly reduces both the perception of pain "
        "and the natural emotional response to pain. In short, it's a powerful painkiller."
    ),
    "Mentats": (
        "A popular recreational and performance-enhancing drug before the Great War, "
        "Mentats enhance memory and speed mental processes."
    ),
    "Orange Mentats": (
        "A variant of Mentats which heighten awareness and sensory acuity."
    ),
    "Overdrive": (
        "An enhanced form of Psycho which massively stimulates aggression, making the user more dangerous in combat."
    ),
    "Psycho": (
        "A potent combat stimulant created by the U.S. Army to enhance the effectiveness of soldiers in battle, "
        "inducing a state of heightened aggression and reduced pain sensitivity."
    ),
    "Psycho Jet": (
        "A powerful, addictive cocktail of Psycho and Jet, which enhances aggression, dulls pain, "
        "and augments a target's reflexes and energy levels."
    ),
    "Psychobuff": (
        "A highly addictive cocktail of Psycho and Buffout steroids, combining the effects of the two drugs "
        "to produce a period of extreme strength, durability, and aggression."
    ),
    "Psychotats": (
        "A combination of Psycho and Mentats, providing enhanced combat performance while maintaining mental clarity."
    ),
    "Rad-X": (
        "A pre-War medication that temporarily fortifies the body against the effects of radiation poisoning."
    ),
    "RadAway": (
        "An intravenous drug which purges radiation from the user's body, absorbing radiation as it circulates through the user's bloodstream."
    ),
    "Skeeto Spit": (
        "A tribal remedy made from the saliva of mutated mosquitoes, known to temporarily bolster one's constitution."
    ),
    "Stimpak": (
        "A wonder of pre-War science, a Stimpak is a single-use syringe filled with a variety of potent healing agents, "
        "stimulants, and painkillers."
    ),
    "Super Stimpak": (
        "An enhanced version of the standard Stimpak, delivering a more concentrated dose of healing agents for greater effect."
    ),
    "Ultra Jet": (
        "An extremely concentrated form of Jet, it is significantly more potent and affects Ghouls as easily as it does humans."
    ),
    "X-Cell": (
        "A general-purpose performance enhancer still being developed before the Great War. "
        "Development was never finished, but prototype versions were distributed through the black market."
    ),
    "Rad-X (Diluted)": (
        "A diluted version of Rad-X, roughly half as effective but easier to find than the full-strength version."
    ),
    "RadAway (Diluted)": (
        "A diluted version of RadAway, roughly half as effective but easier to find than the full-strength version."
    ),
    "Stimpak (Diluted)": (
        "A diluted version of a Stimpak, roughly half as effective but easier to find than the full-strength version."
    ),
    "Stealth Boy": (
        "A compact device which generates a modulating refraction field that renders the user nearly invisible. "
        "One of the most interesting technologies developed before the War."
    ),
    "Robot Repair Kit": (
        "A device which can help to repair and reactivate damaged robots or Power Armor. "
        "Most robots have internal self-diagnostic and repair protocols which are activated when repairs are performed."
    ),
    "Stimpak Diffuser": (
        "This delivery mechanism allows the contents of a Super Stimpak to be dispersed into an aerosol cloud, "
        "providing a burst of medicinal vapor over a small area."
    ),
}

def add_armor_descriptions():
    armor = load_json("armor.json")
    class_map = {
        "raider": "raider",
        "leather": "leather",
        "metal": "metal",
        "combat": "combat",
        "synth": "synth",
        "vault_tec_security": "vault_security",
    }
    
    count = 0
    for item in armor:
        ac = item.get("armorClass", "")
        if ac in class_map:
            desc_key = class_map[ac]
            if desc_key in ARMOR_DESCRIPTIONS and "description" not in item:
                item["description"] = ARMOR_DESCRIPTIONS[desc_key]
                count += 1
    
    save_json("armor.json", armor)
    print(f"✓ Added descriptions to {count}/{len(armor)} armor items")

def add_headgear_descriptions():
    headgear = load_json("headgear.json")
    count = 0
    for item in headgear:
        name = item["name"]
        if name in HEADGEAR_DESCRIPTIONS and "description" not in item:
            item["description"] = HEADGEAR_DESCRIPTIONS[name]
            count += 1
    
    save_json("headgear.json", headgear)
    print(f"✓ Added descriptions to {count}/{len(headgear)} headgear items")

def add_consumable_descriptions():
    consumables = load_json("consumables.json")
    count = 0
    for item in consumables:
        name = item["name"]
        if name in CONSUMABLE_DESCRIPTIONS and "description" not in item:
            item["description"] = CONSUMABLE_DESCRIPTIONS[name]
            count += 1
    
    save_json("consumables.json", consumables)
    print(f"✓ Added descriptions to {count}/{len(consumables)} consumable items")

if __name__ == "__main__":
    add_armor_descriptions()
    add_headgear_descriptions()
    add_consumable_descriptions()
    print("\nDone! Descriptions added where applicable.")
