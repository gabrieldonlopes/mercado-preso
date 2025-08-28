from models import Produto
from . import db

def ver_todos_produtos() -> list[Produto]:
    produtos = Produto.query.all()

    return [
        {
            "produto_id":p.produto_id,
            "nome":p.nome,
            "descricao":p.descricao,
            "preco":p.preco,
            "quantidade":p.quantidade,
            "vendedor_id":p.vendedor_id,
            "data_cricao":p.data_criacao,
            "imagem":p.imagem
        } 
        for p in produtos]

