"""Recipe

Contains all useful information from a Paprika recipe

"""

import sqlite3

class DB:
    """ Simpler interface to the Paprika database - adds convenience functions """
    def init(self):
        self.conn = sqlite3.connect('Database/Paprika.sqlite')
        self.curs = self.conn.cursor()

    def getRecipebyName(self, name):
        self.curs.execute("SELECT Z_PK, ZCOOKTIME, ZDESCRIPTIONTEXT, ZDIFFICULTY, ZDIRECTIONS,"
                          "ZINGREDIENTS, ZNAME, ZNOTES, ZNUTRITIONALINFO, ZPREPTIME,"
                          "ZSERVINGS, ZSOURCE, ZSOURCEURL, ZTOTALTIME FROM ZRECIPE "
                          "WHERE ZNAME = %s", (name,))
        return Recipe(*self.curs.fetchone())


class Recipe:
    def __init__(self, pk, cooktime, descriptiontext, difficulty, directions,  ingredients, name, notes,
                 nutritionalinfo, preptime, servings, source, sourceurl, totaltime):
        self.pk = pk
        self.cooktime = cooktime
        self.descriptiontext = descriptiontext
        self.difficulty = difficulty
        self.directions = directions.split('\n')
        self.ingredients = ingredients.split('\n')
        self.name = name
        self.notes = notes
        self.preptime = preptime
        self.servings = servings
        self.source = source
        self.sourceurl = sourceurl
        self.totaltime = totaltime



if __name__ == '__main__':
    db = DB()
    r = db.getRecipebyName('Halibut with Rosemary Potatoes'))\
    print(r.ingredients)

