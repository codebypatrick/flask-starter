from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from . import post
from .forms import PostForm, CommentForm
from .. import db
from ..models import Post, Comment

@post.route('/')
def list():
    posts = Post.query.all()
    return render_template('post/list.html', posts=posts)

@post.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, 
                    body=form.body.data, 
                    author=current_user._get_current_object()
                    )
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully', 'success')
        return redirect(url_for('.list'))
    return render_template('post/create.html', form=form)

@post.route('/<id>', methods=['GET', 'POST'])
@login_required
def show(id):
    post = Post.query.get_or_404(id)
    form = CommentForm() 
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                post=post,
                author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Comment added', 'success')
    return render_template('post/show.html', post=post, form=form)

@post.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('Post updated', 'success')
    form.title.data = post.title
    form.body.data = post.body
    return render_template('post/update.html', form=form, post=post)

#TODO soft delete (add a boolean deleted field)
@post.route('/remove/<id>', methods=['GET', 'POST'])
@login_required
def remove(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect(url_for('.list'))
