import uvicorn, json, time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from prompts.prompts import get_prompt_evaluation 
from gemini.gemini import get_synergies

folder_prefix = '/etc/ghackathon/data'

archetype_data_file = {
    1: f"{folder_prefix}/warfare.json",
    2: f"{folder_prefix}/archery.json",
    3: f"{folder_prefix}/shadow.json",
    4: f"{folder_prefix}/protection.json",
    5: f"{folder_prefix}/wizardry.json",
    6: f"{folder_prefix}/holy.json",
    7: f"{folder_prefix}/spiritual.json",
    8: f"{folder_prefix}/witchcraft.json",
}
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Weights(BaseModel):
    tank: float
    healer: float
    spell_damage: float
    meele_damage: float
    ranged_damage: float
    debuff: float
    buff: float

class SkillMetadata(BaseModel):
    archetype_id: int
    skill_id: int

class CombosInput(BaseModel):
    weights: Weights
    a_skill: SkillMetadata
    b_skill: SkillMetadata

@app.post("/combos")
async def generate_combos(input: CombosInput):
    a_data = {}
    with open(archetype_data_file[input.a_skill.archetype_id], 'r') as file:
        a_data = json.load(file)
    
    b_data = {}
    with open(archetype_data_file[input.b_skill.archetype_id], 'r') as file:
        b_data = json.load(file)
    
    weights = {
        'tank': input.weights.tank,
        'healer': input.weights.healer,
        'spell_damage': input.weights.spell_damage,
        'meele_damage': input.weights.meele_damage,
        'ranged_damage': input.weights.ranged_damage,
        'debuff': input.weights.debuff,
        'buff': input.weights.buff,
    }
    prompt_evaluation = get_prompt_evaluation(a_data, b_data, weights, input.a_skill.skill_id, input.b_skill.skill_id)

    synergies = get_synergies(prompt_evaluation)
    if synergies["error"] == "Google AI API error" or synergies["error"] == "AI allucinates":
        # give it a try (only one) in case the API returns an error or the AI allucinates
        print(f"AI error: '{synergies['error']}'. Give it one more chance...")
        time.sleep(10)
        synergies = get_synergies(prompt_evaluation)

    if synergies["error"] != None:
        print(f"AI error: {synergies['error']}. ignoring the synergie of this skill.")
        time.sleep(5)
        return {
            "error": "AI Alluciantion"
        }
    
    response = []
    sorted_synergies = sorted(synergies["value"], key=lambda x: x["score"], reverse=True)
    for skill in sorted_synergies:
        info = {
            "score": skill["score"],
            "reason": skill["reason"],
            "a_skill_id": skill['a_skill_id'],
            "a_ravencard_id": skill['a_ravencard_id'],
            "b_skill_id": skill['b_skill_id'],
            "b_ravencard_id": skill['b_ravencard_id']
        }
        response.append(info)

    return {
        "synergies": response
    }

@app.get("/healthcheck")
def healthcheck():
    return {
        "health": "OK"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)