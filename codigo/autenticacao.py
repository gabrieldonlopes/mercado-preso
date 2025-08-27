from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
import functools

from .models import Usuario, TipoUsuario
from . import db
from .forms import RegistrationForm, LoginForm

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')

@bp_auth.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            usuario = Usuario(
                nome=form.nome.data,
                email=form.email.data,
                tipo_usuario=TipoUsuario(int(form.tipo_usuario.data)),
                senha=generate_password_hash(form.senha.data)
            )
            
            db.session.add(usuario)
            db.session.commit()
            
            flash("Conta criada com sucesso! Faça login para continuar.", "success")
            return redirect(url_for('auth.login'))
            
        except IntegrityError:
            db.session.rollback()
            flash("Erro ao criar conta. Tente novamente.", "danger")
    
    return render_template('auth/register.html', form=form)

@bp_auth.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(nome=form.nome.data).first()
        session.clear()
        session['usuario_id'] = user.usuario_id
        flash(f"Bem-vindo de volta, {user.nome}!", "success")
        return redirect(url_for('home'))
    
    return render_template('auth/login.html', form=form)

@bp_auth.before_app_request
def load_logged_in_user():
    usuario_id = session.get('usuario_id')
    
    if usuario_id is None:
        g.user = None
    else:
        try:
            g.user = Usuario.query.get(usuario_id)
        except:
            g.user = None

@bp_auth.route('/logout')
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for('home'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Você precisa fazer login para acessar esta página.", "warning")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view