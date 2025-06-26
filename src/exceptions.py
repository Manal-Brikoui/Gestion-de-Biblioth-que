# exceptions.py

# Exception levée lorsqu’un livre est déjà emprunté et qu’on essaie de l’emprunter à nouveau
class LivreIndisponibleError(Exception):
    pass

# Exception levée lorsqu’un membre tente d’emprunter plus que le nombre autorisé de livres
class QuotaEmpruntDepasseError(Exception):
    pass

# Exception levée lorsqu’on tente d’effectuer une opération avec un membre inexistant
class MembreInexistantError(Exception):
    pass

# Exception levée lorsqu’on tente d’effectuer une opération sur un livre introuvable
class LivreInexistantError(Exception):
    pass
