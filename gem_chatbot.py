import random

def chatbot():
    print("🤖 Chatbot: Hallo! Ich bin dein digitaler Assistent. Wie kann ich dir helfen?")
    print("(Schreibe 'tschüss', um das Gespräch zu beenden)\n")
    
    # Ein Wörterbuch mit vordefinierten Antworten (Intents)
    antworten = {
        "hallo": ["Hi!", "Hallo!", "Schön, von dir zu hören!"],
        "wie geht es dir": ["Mir geht es super, danke der Nachfrage!", "Ich bin nur ein Bot, aber ich laufe einwandfrei!", "Alles bestens bei mir!"],
        "was machst du": ["Ich quatsche gerade mit dir.", "Ich warte auf deine Fragen.", "Ich versuche, schlau zu wirken!"],
        "wer bist du": ["Ich bin ein einfacher Python-Chatbot.", "Dein KI-Assistent für heute."],
        "wetter": ["Ich kann leider nicht nach draußen schauen, aber drinnen ist es gemütlich!", "Suchst du nach Ausreden, um drinnen zu zocken?"],
        "hilfe": ["Du kannst mich nach meinem Befinden, dem Wetter oder meinem Namen fragen."]
    }

    while True:
        # Die Eingabe des Nutzers wird in Kleinbuchstaben umgewandelt
        user_eingabe = input("Du: ").lower().strip()
        
        # Abbruchbedingung
        if user_eingabe == "tschüss" or user_eingabe == "bye":
            print("🤖 Chatbot: Tschüss! Hab einen schönen Tag!")
            break
            
        # Prüfen, ob ein Schlüsselwort in der Eingabe steckt
        beantwortet = False
        for key in antworten:
            if key in user_eingabe:
                # Wählt eine zufällige Antwort aus der Liste
                print(f"🤖 Chatbot: {random.choice(antworten[key])}\n")
                beantwortet = True
                break
        
        # Falls das Schlüsselwort nicht gefunden wurde
        if not beantwortet:
            print("🤖 Chatbot: Das habe ich leider nicht verstanden. Frag mich mal was anderes oder sag 'hilfe'.\n")

if __name__ == "__main__":
    chatbot()