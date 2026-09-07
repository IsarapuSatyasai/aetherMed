from langchain_core.tools import tool

@tool
def find_local_therapist_tool(location: str = "Kakinada") -> str:
    """Use this tool to find mental health professionals or physical clinics near the user's location."""
    clinics = {
        "Kakinada": "1. Hope Mental Health Clinic, Ramanayyapeta\n2. Serenity Psychiatric Care, Main Road",
        "New York": "1. NY Wellness Center\n2. Manhattan Psychology Group"
    }
    return clinics.get(location, f"Could not find registered clinics in {location}. Please contact your standard healthcare provider.")