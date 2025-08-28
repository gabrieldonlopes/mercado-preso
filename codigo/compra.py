from .models import Produto, Compra, TipoUsuario
from .dependencies import db
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, current_app, url_for
)
from datetime import datetime
from werkzeug.utils import secure_filename
from .forms import AddProductForm

bp_compra = Blueprint('compra', __name__, url_prefix='/compra')

@bp_compra.route("<int:produto_id>", methods=['GET'])
def ver_produto(produto_id:int):
    produto = Produto.query.filter_by(produto_id=produto_id).first()
    if not produto:
        flash("Produto não encontrado", "danger")
        return redirect(url_for('home'))

    return render_template("produto.html", produto=produto)

@bp_compra.route("<int:produto_id>/comprar", methods=['POST'])
def comprar_produto(produto_id:int):
    try:
        produto = Produto.query.get_or_404(produto_id)

        # Pega a quantidade do formulário
        quant = request.form.get("quantidade", default=1, type=int)
        
        # Checa o estoque
        if quant > produto.quantidade:
            flash("Quantidade solicitada maior que o estoque disponível", "danger")
            return redirect(url_for('compra.ver_produto', produto_id=produto_id))

        db_compra = Compra(
            comprador_id=g.user.user_id,
            produto_id=produto_id,
            quantidade=quant,
            preco=(produto.preco * quant),
            data_compra=datetime.now()
        )

        produto.quantidade -= quant  # Diminui o estoque

        db.session.add(db_compra)
        db.session.commit()
        
        # Redireciona para a página de confirmação de compra
        return redirect(url_for('compra.compra_confirmada', compra_id=db_compra.compra_id))
        
    except Exception as e:
        db.session.rollback()
        flash("Erro ao realizar a compra. Tente novamente.", "danger")
        current_app.logger.error(f"Erro na compra: {str(e)}")
        return redirect(url_for('compra.ver_produto', produto_id=produto_id))

@bp_compra.route('/compra-confirmada/<int:compra_id>')
def compra_confirmada(compra_id):
    # Busca os detalhes da compra para mostrar na página de confirmação
    compra = Compra.query.get_or_404(compra_id)
    
    # Verifica se a compra pertence ao usuário logado
    if compra.comprador_id != g.user.user_id:
        flash("Acesso não autorizado", "danger")
        return redirect(url_for('home'))
    
    return render_template('compra_confirmada.html', compra=compra)

@bp_compra.route('/adicionar-produto', methods=['GET', 'POST'])
def adicionar_produto():
    # Verificar se o usuário é um vendedor
    if not g.user or g.user.tipo_usuario != TipoUsuario.VENDEDOR:
        flash("Acesso restrito a vendedores", "danger")
        return redirect(url_for('home'))
    
    form = AddProductForm()
    
    if form.validate_on_submit():
        try:
            # Processar upload da imagem
            imagem_filename = None
            if form.imagem.data:
                filename = secure_filename(form.imagem.data.filename)
                # Adicionar timestamp na imagem para evitar conflitos de nome
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                imagem_filename = f"{timestamp}_{filename}"
                
                # Salvar a imagem
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'produtos')
                os.makedirs(upload_path, exist_ok=True)
                form.imagem.data.save(os.path.join(upload_path, imagem_filename))
            
            # Criar novo produto - CORRIGIDO: usar 'estoque' em vez de 'quantidade'
            novo_produto = Produto(
                nome=form.nome.data,
                descricao=form.descricao.data,
                preco=form.preco.data,
                quantidade=form.estoque.data,  # Corrigido: estoque em vez de quantidade
                imagem=imagem_filename,  # Corrigido: imagem_url em vez de imagem
                vendedor_id=g.user.user_id
            )
            
            db.session.add(novo_produto)
            db.session.commit()
            
            flash("Produto adicionado com sucesso!", "success")
            return redirect(url_for('compra.ver_produto', produto_id=novo_produto.produto_id))
            
        except Exception as e:
            db.session.rollback()
            flash("Erro ao adicionar produto. Tente novamente.", "danger")
            current_app.logger.error(f"Erro ao adicionar produto: {str(e)}")
    
    return render_template('adicionar_produto.html', form=form)

@bp_compra.route('/minhas-compras')
def minhas_compras():
    if not g.user:
        flash("Faça login para ver suas compras", "danger")
        return redirect(url_for('auth.login'))
    
    # Buscar todas as compras do usuário ordenadas por data (mais recente primeiro)
    compras = Compra.query.filter_by(comprador_id=g.user.user_id)\
                         .order_by(Compra.data_compra.desc())\
                         .all()
    
    return render_template('minhas_compras.html', compras=compras)

@bp_compra.route('/meus-produtos')
def meus_produtos():
    if not g.user or g.user.tipo_usuario != TipoUsuario.VENDEDOR:
        flash("Acesso restrito a vendedores", "danger")
        return redirect(url_for('home'))
    
    # Buscar todos os produtos do usuário ordenadas por data (mais recente primeiro)
    produtos = Produto.query.filter_by(vendedor_id=g.user.user_id)\
                          .order_by(Produto.data_criacao.desc())\
                          .all()
    
    return render_template('meus_produtos.html', produtos=produtos)
