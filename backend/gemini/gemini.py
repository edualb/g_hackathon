import time
from google.protobuf.json_format import MessageToDict
from vertexai.generative_models import (
    GenerativeModel,
    FunctionDeclaration,
    Tool
)

model = GenerativeModel("gemini-1.0-pro")

gemini_func = FunctionDeclaration(
    name="get_synergies",
    description="Get Skill Synergies",
    parameters={
        "type": "object",
        "properties": {
            "synergies": {
                "type": "array",
                "description": "List of Skill Synergies with values",
                "items": {
                    "type": "object",
                    "properties": {
                        "synergy_id": {
                            "type": "integer",
                            "description": "The Synergy identifier",
                        },
                        "synergy_score": {
                            "type": "number",
                            "format": "float",
                            "description": "The Synergy score",
                        },
                        "synergy_reason": {
                            "type": "string",
                            "description": "The Synergy reason",
                        },
                        "skill_a_id": {
                            "type": "integer",
                            "description": "The Skill identifier (skill_a_id)",
                        },
                        "skill_a_buff_id": {
                            "type": "integer",
                            "description": "The Buff Skill identifier (skill_a_buff_id)",
                        },
                        "skill_b_id": {
                            "type": "integer",
                            "description": "The Skill identifier (skill_b_id)",
                        },
                        "skill_b_buff_id": {
                            "type": "integer",
                            "description": "The Buff Skill identifier (skill_b_buff_id)",
                        },
                    },
                }
            },
        }
    },
)

gemini_tool = Tool(
    function_declarations=[gemini_func]
)

def get_synergies(prompt: str):
    try:
        data = {
            "error": None
        }

        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.7},
            tools=[]
        )

        if not response:
            data["error"] = "AI API is not working"
            return data
        if len(response.candidates) <= 0:
            data["error"] = "AI returns no candidate"
            return data
        if not response.candidates[0].content:
            data["error"] = "AI returns no content"
            return data
        if len(response.candidates[0].content.parts) <= 0:
            data["error"] = "AI returns no content parts"
            return data

        # avoinding 500 internal error from Vertex AI
        time.sleep(5)

        response_scores = model.generate_content(
            f"""
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
            {response.candidates[0].content.parts[0].text}
            """,
            generation_config={"temperature": 0.7},
            tools=[gemini_tool]
        )

        if not response_scores:
            data["error"] = "AI API is not working"
            return data
        if len(response_scores.candidates) <= 0:
            data["error"] = "AI returns no candidate"
            return data
        if not response_scores.candidates[0].content:
            data["error"] = "AI returns no content"
            return data
        if len(response_scores.candidates[0].content.parts) <= 0:
            data["error"] = "AI returns no content parts"
            return data
        if not response_scores.candidates[0].content.parts[0].function_call:
            data["error"] = "AI returns no function call"
            return data
        if not response_scores.candidates[0].content.parts[0].function_call.args:
            data["error"] = "AI returns no function call arguments"
            return data

        synergies = []
        for key, value in response_scores.candidates[0].content.parts[0].function_call.args.items():
            if key != "synergies":
                continue

            for v in value:
                if not v.__dict__['_pb']['skill_b_buff_id']:
                    continue
                if not v.__dict__['_pb']['skill_a_buff_id']:
                    continue
                if not v.__dict__['_pb']['synergy_score']:
                    continue
                if not v.__dict__['_pb']['skill_b_id']:
                    continue
                if not v.__dict__['_pb']['synergy_reason']:
                    continue
                if not v.__dict__['_pb']['skill_a_id']:
                    continue

                synergy = {
                    "a_skill_id": MessageToDict(v.__dict__["_pb"]['skill_a_id']),
                    "a_ravencard_id": MessageToDict(v.__dict__["_pb"]['skill_a_buff_id']),
                    "b_skill_id": MessageToDict(v.__dict__["_pb"]['skill_b_id']),
                    "b_ravencard_id": MessageToDict(v.__dict__["_pb"]['skill_b_buff_id']),
                    "score": MessageToDict(v.__dict__["_pb"]['synergy_score']),
                    "reason": MessageToDict(v.__dict__["_pb"]['synergy_reason']),
                }
                synergies.append(synergy)
        data["value"] = synergies

        if len(synergies) == 0:
            data["error"] = "AI allucinates"
        return data
    except:
        data["error"] = "Google AI API error"
        return data