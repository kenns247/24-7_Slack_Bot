class resource_manager(object):
    def __init__(self, file_name):
        with open(os.path.join('./resources', file_name), 'r') as f:
            self.responses = f.read().splitlines()

    def get_response(self):
        return random.choice(self.responses)

    def get_all(self):
        return ' \n'.join(line for line in self.responses)

    def get_count(self):
        return len(self.responses)