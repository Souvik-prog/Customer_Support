from fastapi import FastAPI, Response, Form
from services.ai_services import claude_service
from services.twilio_services import create_initial_greeting, create_ai_response
import uvicorn

app = FastAPI()


@app.post("/voice")
@app.get("/voice")
async def voice():
    """
    Handles the initial incoming call from Twilio.
    It generates a TwiML response to greet the user and start listening.
    """
    print("--- Incoming Call Received: Hitting /voice endpoint ---")
    twiml_response = create_initial_greeting()
    return Response(content=twiml_response, media_type="application/xml")


@app.post("/handle-speech")
async def handle_speech(SpeechResult: str = Form(...)):

    user_speech = SpeechResult
    print(f"--- User Said: '{user_speech}'. Hitting /handle-speech endpoint ---")

    ai_response_text = "I'm sorry, I had a problem processing that. Could you please say it again?"

    if user_speech:
        ai_response_text = claude_service.get_response(user_speech)

    print(f"--- AI Responded: '{ai_response_text}' ---")

    twiml_response = create_ai_response(ai_response_text)
    return Response(content=twiml_response, media_type="application/xml")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

