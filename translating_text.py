from deep_translator import MyMemoryTranslator

def translate_text():
    path = "transcript.txt"

    translated = MyMemoryTranslator(source='en-GB', target='hi-IN').translate_file(path)

    line = "-" * len(translated)
    print(line)
    print("Translated text: ", translated)
    print(line)


    with open("translated.txt", "w") as f:
        f.write(translated)

    return translated

