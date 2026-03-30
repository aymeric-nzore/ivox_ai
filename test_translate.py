from core.translator import translate

if __name__ == "__main__":
    text = "Bonjour, comment vas-tu ?"
    print("Texte source :", text)
    print("Traduction :", translate(text))
