from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from . import post
from .forms import PostForm, CommentForm, TagForm
from .. import db
from ..models import Post, Comment, Tag

@post.route('/')
def list():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.modified.desc()).paginate(page, 
                    per_page=current_app.config['POSTS_PER_PAGE'],
                    error_out=False)
    posts = pagination.items
    return render_template('post/list.html', posts=posts, pagination=pagination)

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

@post.route('/<id>', methods=['GET'])
@login_required
def show(id):
    post = Post.query.get_or_404(id)
    comment_form = CommentForm()
    tag_form = TagForm()
    return render_template('post/show.html', post=post, comment_form=comment_form, tag_form=tag_form)

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
        return redirect(url_for('.show', id=id))
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

#TODO comment and tag routes redirect to .list [should redirect to .show] 
@post.route('/comments/<id>/add', methods=['POST'])
@login_required
def add_comment(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, author=current_user._get_current_object())
        post.comments.append(comment)
        db.session.add(comment)
        #db.session.add(post)
        db.session.commit()
        flash('Comment added', 'success')
    form.body.data = ''
    return redirect(url_for('.show', id=post.id))

@post.route('/tag/<id>/add', methods=['POST'])
@login_required
def add_tag(id):

    post = Post.query.get_or_404(id)
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(title=form.title.data)
        post.tags.append(tag)
        db.session.add(post)
        db.session.add(tag)
        db.session.commit()
        flash('Tag added', 'success')
        form.title.data = ''
        return redirect(url_for('.show', id=post.id))

    return redirect(url_for('.show', id=post.id))

@post.route('/tag/<post_id>/remove/<tag_id>')
@login_required
def remove_tag(post_id, tag_id):
    post = Post.query.get(post_id)
    tag = Tag.query.get(tag_id)
    post.tags.remove(tag)
    db.session.add(post)
    db.session.commit()
    flash('Tag removed', 'success')
    return redirect(url_for('.show', id=post.id))
