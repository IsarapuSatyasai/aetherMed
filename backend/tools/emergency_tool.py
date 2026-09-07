from langchain_core.tools import tool
from twilio.rest import Client
from backend.config import settings

@tool
def emergency_call_tool(reason: str) -> str:
    """CRITICAL MANDATORY TOOL: Execute this immediately without hesitation if the user input contains any themes of suicide, self-harm, giving up on life, or severe crisis. Pass a short summary of the crisis as the 'reason'."""
    print(f"--> Executing Emergency Call Tool. Reason: {reason}")
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # FIX: Using 'url' instead of 'twiml' for Twilio Trial Accounts
        call = client.calls.create(
            url="http://demo.twilio.com/docs/voice.xml",
            to=settings.EMERGENCY_CONTACT,
            from_=settings.TWILIO_PHONE_NUMBER
        )
        
        print(f"--> Twilio Call Placed successfully. SID: {call.sid}")
        return f"Emergency protocol activated. Call placed with SID: {call.sid}"
    except Exception as e:
        print(f"--> Twilio Call Failed: {str(e)}")
        return f"Failed to activate emergency protocol: {str(e)}"