import random

def get_response(message: str) -> str:
    p_message = message.lower().strip(" ")

    if p_message == 'hello':
        return 'Hey there!'

    if message == 'roll':
        return str(random.randint(1, 6))
    
    if message[0:3]=="!f ":
        movie = message[3:].split()
        return "https://www.letterboxd.com/film/"+"-".join(movie)+ "/"

    if p_message == '!help':
        return '`This is a help message that you can modify.`'

    return 'I didn\'t understand what you wrote. Try typing "!help".'


