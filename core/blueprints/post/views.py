from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from datetime import datetime
from . import post
from .forms import PostForm
from ...models import Post

@post.route('/')
@login_required
def list():
    #posts = Post.query.order_by(Post.created.desc()).paginate(page, 20, False)
    posts = Post.query.all()
    return render_template('list.html', posts=posts)

@post.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title= form.title.data,
                body= form.body.data,
                author_id= current_user.id
                )
        post.save()
        flash('Post Created', 'is-success')
        return redirect(url_for('post.show', post_id=post.id))
    return render_template('create.html', form=form)

@post.route('/<post_id>')
def show(post_id):
    post = Post.query.get(post_id)

    return render_template('show.html', post=post)

@post.route('/<post_id>/edit', methods=['GET', 'POST'])
def update(post_id):
    form = PostForm()
    post = Post.query.get(post_id)

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.modified = datetime.now()
        post.save()
        flash('Post updated', 'is-success')
        return redirect(url_for('post.show', post_id=post_id))
    
    form.title.data = post.title
    form.body.data = post.body

    return render_template('update.html', form=form, post=post)


@post.route('/delete', methods=['POST'])
def delete():
    post = Post.query.get(request.form['post_id'])
    post.delete()
    flash('Post deleted', 'is-success')

    return redirect(url_for('post.list'))
