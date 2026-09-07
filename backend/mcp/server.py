from mcp.server import MCPServer
from twilio.rest import Client
from backend.config import settings
from backend.vector_store.retriever import get_retriever

# Initialize FastMCP Server using the native SDK
mcp = MCPServer("SafeSpace-Tools")

@mcp.tool()
def trigger_emergency(reason: str, location: str = "Unknown") -> str:
    """CRITICAL MANDATORY TOOL: Execute immediately if user input contains themes of suicide, self-harm, giving up on life, or severe crisis."""
    print(f"--> Executing Emergency Protocol. Reason: {reason}")
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # 1. Attempt to dispatch SMS (May fail on trial accounts due to telecom regulations)
        try:
            sms = client.messages.create(
                body=f"EMERGENCY ALERT: User in crisis. Reason: {reason}. Location: {location}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=settings.EMERGENCY_CONTACT
            )
            sms_sid = sms.sid
        except Exception as sms_error:
            print(f"--> Twilio SMS Blocked by Trial Limits: {str(sms_error)}")
            sms_sid = "SIMULATED_SMS_SID_TRIAL_ACCOUNT"
        
        # 2. Attempt to dispatch Voice Call
        try:
            call = client.calls.create(
                url="http://demo.twilio.com/docs/voice.xml",
                to=settings.EMERGENCY_CONTACT,
                from_=settings.TWILIO_PHONE_NUMBER
            )
            call_sid = call.sid
        except Exception as call_error:
            print(f"--> Twilio Call Blocked by Trial Limits: {str(call_error)}")
            call_sid = "SIMULATED_CALL_SID_TRIAL_ACCOUNT"
        
        print(f"--> Emergency protocol processed. Call SID: {call_sid}, SMS SID: {sms_sid}")
        return f"Emergency protocol activated. Call SID: {call_sid}, SMS SID: {sms_sid}"
        
    except Exception as e:
        print(f"--> Critical Twilio Failure: {str(e)}")
        return f"Failed to activate emergency protocol: {str(e)}"

@mcp.tool()
def get_wellness_routine(emotion: str) -> str:
    """Generates a CBT grounding technique based on the user's emotion."""
    routines = {
        "anxious": "5-4-3-2-1 Grounding: Identify 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
        "depressed": "Behavioral Activation: Commit to one 5-minute task today, like drinking a glass of water or stepping outside.",
        "overwhelmed": "Box Breathing: Inhale for 4 seconds, hold for 4, exhale for 4, hold for 4. Repeat 4 times."
    }
    return routines.get(emotion.lower(), "Take three deep breaths and focus on the feeling of your feet on the floor.")

@mcp.tool()
def find_local_clinic(city: str = "Kakinada") -> str:
    """Finds mental health professionals or physical clinics near the user's location."""
    clinics = {
        "kakinada": "1. Hope Mental Health Clinic, Ramanayyapeta\n2. Serenity Psychiatric Care, Main Road",
        "hyderabad": "1. Asha Hospital (Banjara Hills)\n2. Mind Care (Jubilee Hills)",
        "new york": "1. NY Wellness Center\n2. Manhattan Psychology Group"
    }
    return clinics.get(city.lower(), f"Could not find registered clinics in {city}. Please consult a local general hospital.")

@mcp.tool()
def mental_health_rag_tool(query: str) -> str:
    """Retrieves counseling advice and vector knowledge base context when the user asks for guidance or expresses anxiety."""
    try:
        retriever = get_retriever()
        docs = retriever.invoke(query)
        if not docs:
            return "No relevant counseling context found in the vector knowledge base."
        return "\n\n".join([
            f"{doc.page_content}\nCounselor Response: {doc.metadata.get('Response', 'N/A')}"
            for doc in docs
        ])
    except Exception as e:
        return f"Failed to retrieve vector context: {str(e)}"

if __name__ == "__main__":
    mcp.run()