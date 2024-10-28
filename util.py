# Загружает промпт из папки /resources/prompts/
def load_prompt(name):
    with open("resources/prompts/" + name + ".txt", "r", encoding="utf8") as file:
        return file.read()

# Загружает промпт из папки /resources/message/
def load_message(name):
    with open("resources/message/" + name + ".txt", "r", encoding="utf8") as file:
        return file.read()