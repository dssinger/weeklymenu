"""Recipe

Contains all useful information from a Paprika recipe
We assume that all recipes have been exported to the grocery list so we can use Paprika's parsing
"""

import sqlite3

class DB:
    """ Simpler interface to the Paprika database - adds convenience functions """
    def __init__(self):
        self.conn = sqlite3.connect('Database/Paprika.sqlite')
        self.curs = self.conn.cursor()

    def getRecipeByName(self, name):
        self.curs.execute("SELECT Z_PK, ZCOOKTIME, ZDESCRIPTIONTEXT, ZDIFFICULTY, ZDIRECTIONS,"
                          "ZINGREDIENTS, ZNAME, ZNOTES, ZNUTRITIONALINFO, ZPREPTIME,"
                          "ZSERVINGS, ZSOURCE, ZSOURCEURL, ZTOTALTIME FROM ZRECIPE "
                          "WHERE ZNAME = ?", (name,))
        return Recipe(*self.curs.fetchone())

    def getIngredientByName(self, name, recipename=None):

        query = "SELECT ZNAME, ZINGREDIENT, ZINSTRUCTION, ZQUANTITY, ZAISLENAME, ZLIST "\
                "FROM ZGROCERYITEM WHERE ZNAME = ?"
        if recipename:
            self.curs.execute(query + " AND ZRECIPENAME = ?", (name, recipename))
        else:
            self.curs.execute(query, (name,))
        return Ingredient(*self.curs.fetchone())

    def getPantry(self):
        """ Get all items from the pantry list """
        pantry = Pantry()
        query = "SELECT ZINGREDIENT FROM ZPANTRYITEM"
        self.curs.execute(query)
        for line in self.curs.fetchall():
            pantry.add(line[0])
        return pantry

class Pantry:

    def __init__(self):
      self.items = set()

    def canonicalize(self, s):
        "Make a canonical version of an item, getting rid of weird things"
        # Get rid of punctuation and lowercase the string
        s = s.lower()
        s = s.translate(str.maketrans({c: None for c in ',()-'}))
        # Remove qualifiers
        qualifiers = ("small", "medium", "large", "very", "fresh", "dried", "fine",
                      "dry", "minced", "warm", "finely", "coarsely", "chopped",
                      "freshly", "grated", "thin", "heaping", "teaspoon", "tablespoon",
                      "and", "crushed", "roughly", "a", "optional", "garnish", "kosher",
                      "hardware", "skillet", "flaky", "flakey", "whole", "of")

        s = s.split()
        s = ' '.join([w for w in s if w not in qualifiers])
        return s.strip()


    def add(self, name):
        name = self.canonicalize(name)
        if name:
            self.items.add(name)

    def query(self, name):
        name = self.canonicalize(name)
        return name in self.items



class Ingredient:
    def __init__(self, name, ingredient, instruction, quantity, aislename, list):
        self.name = name
        self.ingredient = ingredient
        self.instruction = instruction
        self.quantity = quantity
        self.aislename = aislename
        self.list = list

    def __repr__(self):
        ret = ''
        if self.quantity:
            ret = self.quantity + ' '
        ret += f'"{self.ingredient}"'
        if self.instruction:
            ret += f' ({self.instruction})'

        if self.aislename:
            ret += f' [On {self.aislename}]'
        if self.list:
            ret += f' [List: {self.list}]'
        ret += f'\n{self.name}'
        return ret

class Recipe:
    def __init__(self, pk, cooktime, descriptiontext, difficulty, directions,  ingredients, name, notes,
                 nutritionalinfo, preptime, servings, source, sourceurl, totaltime):
        self.pk = pk
        self.cooktime = cooktime
        self.descriptiontext = descriptiontext
        self.difficulty = difficulty
        self.directions = directions.split('\n')
        self.ingredients = [db.getIngredientByName(i, name) for i in ingredients.split('\n')]
        self.name = name
        self.notes = notes
        self.preptime = preptime
        self.servings = servings
        self.source = source
        self.sourceurl = sourceurl
        self.totaltime = totaltime



if __name__ == '__main__':
    db = DB()
    pantry = db.getPantry()
    print(list(sorted(pantry.items)))
    r = db.getRecipeByName('Halibut with Rosemary Potatoes')
    for item in r.ingredients:
        print(item, pantry.query(item.ingredient))
        print()

