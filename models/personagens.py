class Personagem:
    def __init__(self, id, nome, altura, peso, habilidades, itens):
        self.id = id
        self.nome = nome
        self.altura = altura
        self.peso = peso
        self.habilidades = habilidades

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "altura": self.altura,
            "peso": self.peso,
            "habilidades": self.habilidades
        }