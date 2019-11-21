class Usuario:
    def __init__(self, id = "",nome = "",email = "",senha = ""):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__senha = senha
    def getNome(self):
        return self.__nome
    def getSenha(self):
        return self.__senha
    def getEmail(self):
        return self.__email
    def getId(self):
        return self.__id