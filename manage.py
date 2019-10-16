import os
from core import create_app, db
from core.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('APP_SETTINGS') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

#def make_shell_context():
#    return dict(app=app, db=db, User=User, Post=Post)

#manager.add_command('shell', Shell(make_context=make_shell_context)) # register app and models to shell
manager.add_command('db', MigrateCommand)

@manager.command
def hello():
    return 'Hello CMD'

@manager.command
def setup():
    recreate_db()
    Role.insert_roles()
    admin = Role.query.filter_by(name='Admin').first()

    """ Create default users account change these details in production """
    d = User(
            username='developer',
            email='developer@site.com',
            password='devpass',
            confirmed=True
            )
    
    d.roles.append(admin)

    a = User(
            username='ad@min',
            email='admin@site.com',
            password='adminpass',
            confirmed=True
            )
    
    #a.roles.append(admin)
    u = User(
            username='unc',
            email='unc@gmail.com',
            password='123')

    db.session.add(u)
    db.session.add(a)
    db.session.add(d)
    db.session.commit()
    
    return 'Default users created'

@manager.command
def create_users(count=100):
    """ Create seed users for testing """
    from sqlalchemy.exc import IntegrityError
    from random import seed
    import forgery_py

    seed()
    for i in range(count):
        u = User(
                username=forgery_py.internet.user_name(),
                email=forgery_py.internet.email_address(),
                password=forgery_py.lorem_ipsum.word()
                )
        u.about_me = forgery_py.lorem_ipsum.sentence()
        u.member_since=forgery_py.date.date(True)
        db.session.add(u)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        
        return 'Created {} users'.format(count)

@manager.command
def create_posts(count=100):
    from random import seed, randint
    import forgery_py

    seed()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count -1)).first()
        p = Post(
                title = forgery_py.lorem_ipsum.sentence(),
                body = forgery_py.lorem_ipsum.sentences(randint(1,3)),
                author_id=u.id
                )
        db.session.add(p)
        db.session.commit()
        return '{} Posts created'.format(Post.query.count())


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return 'Database Recreated'


if __name__ == '__main__':
    manager.run()
