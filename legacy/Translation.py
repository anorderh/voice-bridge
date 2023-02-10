from deep_translator import GoogleTranslator

def translate(text, from_code="en", to_code="es"): # 'from' and 'to' represent language conversion
    return GoogleTranslator(source=from_code, target=to_code).translate(text)