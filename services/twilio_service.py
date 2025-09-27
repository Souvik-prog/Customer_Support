from twilio.twiml.voice_response import VoiceResponse

def create_initial_greeting() -> str:
    response = VoiceResponse()
    response.say(
        "Hello! Thank you for calling our AI customer support line. How can I help you today?",
        voice='alice'
    )

    response.gather(input='speech', action='/handle-speech', speech_timeout='auto', speech_model='experimental_conversations')

    response.redirect('/voice')
    return str(response)

def create_ai_response(ai_text: str) -> str:
    response = VoiceResponse()

    response.say(ai_text, voice='alice')

    response.pause(length=1)

    response.say("Is there anything else I can help you with?", voice='alice')
    response.gather(input='speech', action='/handle-speech', speech_timeout='auto', speech_model='experimental_conversations')

    response.hangup()
    return str(response)

