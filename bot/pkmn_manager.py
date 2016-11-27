import random
import requests
import dict
from common import ResourceManager

URL = 'http://pokeapi.co/api/v2/pokemon/{}/'

class PokemonManager(object):
    def __init__(self):
        self.correct_answers = dict()
        self.pos_response_manager = ResourceManager('pokemon_correct.txt')
        self.neg_response_manager = ResourceManager('pokemon_incorrect.txt')

    def whos_that_pkmn(self, channel):
        answer = self.correct_answers.pop(channel, None)
        if answer is None:
            return self.random_pkmn(channel)
        else:
            return 'It was {}. Guess you aren\'t a Pokemon Master.'.format(answer)            

    def random_pkmn(self, channel):
        num = random.randint(1, 151)
        link = URL
        target = link.format(num)
        try:
            response = requests.get(target)
        except requests.exceptions.RequestException:
            return 'Sorry, Tyler says no. No Pokemons for you.'
        else:
            pokemon = response.json()
            sprite = pokemon['sprites']['front_default']
            self.correct_answers[channel] = pokemon['name']
            return 'Who\'s that Pokemon? {}'.format(sprite)

    def check_response(self, user, channel, msg):
        if (channel in self.correct_answers):
            answer = self.correct_answers[channel]
            tokens = msg.split()
        if answer in tokens:
            return self.guessed_correctly(user, channel)
            else:
                return '<@{}> {}'.format(user, self.neg_response_manager.get_response())

    def guessed_correctly(self, user, channel):
        random_response = self.pos_response_manager.get_response()
        revealed_name = self.reveal_answer()
        return '{} {} You go <@{}>!'.format(random_response, revealed_name, user)
        
    def choose_pkmn(self, target):
        link = URL
        pkmn = link.format(target)
        try:
            response = requests.get(pkmn)
        except requests.exceptions.RequestException:
            return None
        else:
            pokemon = response.json()
            if 'sprites' in pokemon:
                return "Go! {}!\n{}".format(pokemon['forms']['name'].title(), pokemon['sprites']['front_default'])
