class Artist():

    def __init__(self, name, genres, popularity):
        self.name = name
        self.genres = genres
        self.popularity = [popularity]
        self.songs = []

    # can have short, medium, or long term, reped by nums 1, 2, 3 respectively
    def expand_popularity(self, new_pop):
        self.popularity.append(new_pop)

    def print_self(self):
        print('Artist: ' + self.name + ' genres ' + str(self.genres) + ' popularities: ' + str(self.popularity))

