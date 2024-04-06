prompt_synergy_extractor = """
# Role
You are an assistant who helps developers to extract information from text.

# Glossary
- synergy_id (integer): The Synergy identifier
- synergy_score (float): The Synergy score
- synergy_reason (string): The Synergy reason
- skill_a_id (integer): The Skill identifier (skill_a_id)
- skill_a_buff_id (integer): The Buff Skill identifier (skill_a_buff_id)
- skill_b_id (integer): The Skill identifier (skill_b_id)
- skill_b_buff_id (integer): The Buff Skill identifier (skill_b_buff_id)

# Guidelines
From the "Text" provided, extract the following information of each "Skill Synergy": "synergy_id", "synergy_score", "skill_a_id", "skill_a_buff_id", "skill_b_id", "skill_b_buff_id" and "synergy_score".

# Text
{input}
"""

def get_prompt_synergy_extractor(text: str):
    return prompt_synergy_extractor.format(
        input=text
    )


prompt_evaluation = """
# Role
You are an assistant who helps players of MMORPG to build the skills combos of their character.

# Glossary
- Spell Defense: Reduces magic damage taken 
- Weapon Defense: Reduces physical damage taken 
- Spell Power: Increases your damage when using magic-based abilities and weapons
- Weapon Power: Increases your damage when using physical-based abilities and weapons 
- Healing Power: Increases the healing done by your abilities 
- Maximum Health: Increases your total health 
- Maximum Mana: Increases your total mana 
- Health Regeneration: Increases your passive health regeneration
- Mana Regeneration: Increases your passive mana regeneration
- Precision: Increases your chance to land a critical hit
- Impact: Increases the damage (%) of your critical hits
- Haste: Increases your attack speed and reduces your casting time and global cooldown

- Buff: It is a positive status effect that enhances the abilities or attributes of a player character or allied NPC (Non-Player Character). Examples: Increased Attributes, Regeneration, Enhanced Damage, Resistance, Haste, Shielding, Crowd Control Immunity.
- Debuff: It is a negative status effect inflicted upon a player character or an enemy NPC (Non-Player Character) by another player character or NPC. Examples: Poison, Bleed, Slow, Silence, Stun, Blind, DoT (Damage over Time) and decreasing the target's defenses, resistances, or attributes

- Tank Attributes: The attributes to prioritize are "Spell Defense", "Weapon Defense", "Maximum Health", "Maximum Mana", "Health Regeneration" and "Mana Regeneration"
- Healer Attributes: The attributes to prioritize are "Healing Power", "Health Regeneration", "Maximum Mana", "Mana Regeneration"
- Spell Damage Attributes: The attributes to prioritize are "Spell Power", "Maximum Mana", "Mana Regeneration", "Precision", "Impact" and "Haste"
- Meele Damage Attributes: The attributes to prioritize are "Weapon Power", "Maximum Health", "Health Regeneration", "Precision", "Impact" and "Haste"
- Ranged Damage Attributes: The attributes to prioritize are "Weapon Power", "Maximum Mana", "Mana Regeneration", "Precision", "Impact" and "Haste"


# Input Properties
- Weights (object):
    - Tank (float): The weight for "Tank Attributes"
    - Healer (float): The weight for "Healer Attributes"
    - Spell Damage (float): The weight for "Spell Damage Attributes"
    - Meele Damage (float): The weight for "Meele Damage Attributes"
    - Ranged Damage (float): The weight for "Ranged Damage Attributes"
    - Debuff (float): The weight for habilities which generates "Debuff"
    - Buff (float): The weight for habilities which generates "Buff"

- Skills Synergy:
    Synergy_{{number}}:
        - ID (integer): Synergy identifier
        - skill_a (object):
            - skill_id (integer): Unique identifier for the skill "A".
            - skill_channeling (boolean): Whether the skill requires channeling to cast.
            - skill_mana_cost (string or float): Mana cost of the skill (percentage or fixed value).
            - skill_range (integer): Range of the skill. values more than or equal to 3 is good for the weights "Healer", "Spell Damage" and "Ranged Damage"
            - skill_cooldown (string): Cooldown time of the skill (e.g., "60s").
            - skill_description (string): Description of the skill's effect.
            - skill_buff_id (integer): The bonus description identifier.
            - skill_buff (string): The bonus description agregating the skill's effect.
        - skill_b (object):
            - skill_id (integer): Unique identifier for the skill "B".
            - skill_channeling (boolean): Whether the skill requires channeling to cast.
            - skill_mana_cost (string or float): Mana cost of the skill (percentage or fixed value).
            - skill_range (integer): Range of the skill. values more than or equal to 3 is good for the weights "Healer", "Spell Damage" and "Ranged Damage"
            - skill_cooldown (string): Cooldown time of the skill (e.g., "60s").
            - skill_description (string): Description of the skill's effect.
            - skill_buff_id (integer): The bonus description identifier.
            - skill_buff (string): The bonus description agregating the skill's effect.

# Example Input
- Weights:
    - Tank: 0.2
    - Healer: 0.0
    - Spell Damage: 0.0
    - Meele Damage: 0.6
    - Ranged Damage: 0.0
    - Debuff: 0.1
    - Buff: 0.1

- Skills Synergy:
    Synergy_1:
        - ID: 1
        - skill_a:
            - skill_id: 37
            - skill_name: "Bash"
            - skill_channeling: false
            - skill_mana_cost: 1%
            - skill_range: 1
            - skill_cooldown: 1 second(s)
            - skill_description: "Swings your weapon with force, dealing 100.0% (Weapon Power) weapon damage. Every third Bash (Spell) deals 100.0% (Weapon Power) weapon damage to the main target and 50.0% (Weapon Power) weapon damage in a small area around you, causing 20% slow for 2 seconds to all targets."
            - skill_buff_id: 2
            - skill_buff: "Whenever you use Bash (Spell) there is a 6.0% chance for it to reset the cooldown of your Smiting Smash (Spell), allowing Smiting Smash (Spell) to be cast at a value that's equal to consuming 50 Aether for free. This effect can occur once every 20 seconds."
        - skill_b:
            - skill_id: 107
            - skill_name: "Smiting Smash"
            - skill_channeling: false
            - skill_mana_cost: 3%
            - skill_range: 1
            - skill_cooldown: 1 second(s)
            - skill_description: "Deals 100.0% (Weapon Power) weapon damage to all targets around you, lowering their (Attack Power) by 10% and slowing them by 10% for 6 seconds. Increases (Attack Power) reduction and slow effectiveness dealt to targets by 5% per 10 Aether consumed."
            - skill_buff_id: 5
            - skill_buff: "Smithing Smash (Spell) now applies Overwhelmed for 6 seconds to targets hit by it. Targets affected by Overwhelmed will receive increased damage and slow from Bash (Spell). Damage is increased by 12.5% and slow is increased by 60.0%."
    Synergy_2:
        - ID: 2
        - skill_a:
            - skill_id: 37
            - skill_name: "Bash"
            - skill_channeling: false
            - skill_mana_cost: 1%
            - skill_range: 1
            - skill_cooldown: 1 second(s)
            - skill_description: "Swings your weapon with force, dealing 100.0% (Weapon Power) weapon damage. Every third Bash (Spell) deals 100.0% (Weapon Power) weapon damage to the main target and 50.0% (Weapon Power) weapon damage in a small area around you, causing 20% slow for 2 seconds to all targets."
            - skill_buff_id: 2
            - skill_buff: "Whenever you use Bash (Spell) there is a 6.0% chance for it to reset the cooldown of your Smiting Smash (Spell), allowing Smiting Smash (Spell) to be cast at a value that's equal to consuming 50 Aether for free. This effect can occur once every 20 seconds."
        - skill_b:
            - skill_id: 107
            - skill_name: "Smiting Smash"
            - skill_channeling: false
            - skill_mana_cost: 3%
            - skill_range: 1
            - skill_cooldown: 1 second(s)
            - skill_description: "Deals 100.0% (Weapon Power) weapon damage to all targets around you, lowering their (Attack Power) by 10% and slowing them by 10% for 6 seconds. Increases (Attack Power) reduction and slow effectiveness dealt to targets by 5% per 10 Aether consumed."
            - skill_buff_id: 6
            - skill_buff: "Smiting Smash (Spell) will apply Blessed Resonance to targets hit by it for 10 seconds, Blessed Resonance increases the damage of your Blessed Earth (Spell) by 25.0%."

# Example Output
- Skills Synergy:
    Synergy_1:
        - ID: 1
        - Score: 0.94
        - Skills:
            - skill_a_id: 37
            - skill_a_buff_id: 2
            - skill_b_id: 107 
            - skill_b_buff_id: 5
        - Reason: The Synergy between the skills increases the chance to channel "Smithing Smash" skill often, it increases your "Meele Damage".
    Synergy_2:
        - ID: 2
        - Score: 0.17
        - Skills:
            - skill_a_id: 37
            - skill_a_buff_id: 2
            - skill_b_id: 107 
            - skill_b_buff_id: 6
        - Reason: Besides increases the "Meele Damage", there is little Synergy between the skills.

# Guidelines
Always specify the "Synergy ID", "Score", "skill_a_id", "skill_a_buff_id", "skill_b_id", "skill_b_buff_id" and "Reason".
When explaining the "Reason" describe the functionalities of each synergy in detail.

# Task
Given two skills (A and B), score the synergy (0.0 to 1.0) between the "skill_description" of A and B based on the "Weights" provided, "skill_buff", "skill_name", "skill_channeling", "skill_mana_cost", "skill_range" and "skill_cooldown".
        
# Input:
- Weights:
    - Tank: {tank_w}
    - Healer: {healer_w}
    - Spell Damage: {spell_damage_w}
    - Meele Damage: {meele_damage_w}
    - Ranged Damage: {ranged_damage_w}
    - Debuff: {debuff_w}
    - Buff: {buff_w}

- Skills Synergy:{evaluation_input}
"""

def get_prompt_evaluation(a_arch: dict, b_arch: dict, weights: dict, a_skill_id: int, b_skill_id: int):
    a_skill = {}
    for a_spell in a_arch['spells']:
        if a_spell['id'] != a_skill_id:
            continue
        a_skill = a_spell

    b_skill = {}
    for b_spell in b_arch['spells']:
        if b_spell['id'] != b_skill_id:
            continue
        b_skill = b_spell
    
    synergy_id = 1
    evaluation_input = ""
    for ravencard_a in a_skill['ravencards']:
        for ravencard_b in b_skill['ravencards']:
            a_mana = a_skill['mana']
            if a_skill['mana'] == "":
                a_mana = "0%"

            b_mana = b_skill['mana']
            if b_skill['mana'] == "":
                b_mana = "0%"

            a_range = a_skill['range']
            if a_skill['range'] <= 0:
                a_range = 0

            b_range = b_skill['range']
            if b_skill['range'] <= 0:
                b_range = 0

            evaluation_input = f"""{evaluation_input}
    Synergy_{synergy_id}:
        - ID: {synergy_id}
        - skill_a:
            - skill_id: {a_skill['id']}
            - skill_name: {a_skill['name']}
            - skill_channeling: {a_skill['channeling']}
            - skill_mana_cost: {a_mana}
            - skill_range: {a_range}
            - skill_cooldown: {a_skill['cooldown']} second(s)
            - skill_description: {a_skill['description']}
            - skill_buff_id: {ravencard_a['id']}
            - skill_buff: {ravencard_a['description']}
        - skill_b:
            - skill_id: {b_skill['id']}
            - skill_name: {b_skill['name']}
            - skill_channeling: {b_skill['channeling']}
            - skill_mana_cost: {b_mana}
            - skill_range: {b_range}
            - skill_cooldown: {b_skill['cooldown']} second(s)
            - skill_description: {b_skill['description']}
            - skill_buff_id: {ravencard_b['id']}
            - skill_buff: {ravencard_b['description']}"""

            synergy_id += 1

    return prompt_evaluation.format(
        tank_w = weights['tank'],
        healer_w = weights['healer'],
        spell_damage_w = weights['spell_damage'],
        meele_damage_w = weights['meele_damage'],
        ranged_damage_w = weights['ranged_damage'],
        debuff_w = weights['debuff'],
        buff_w = weights['buff'],
        evaluation_input = evaluation_input
    )