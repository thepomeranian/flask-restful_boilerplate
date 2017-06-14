from app import  manager, models, db
import datetime
from flask_migrate import MigrateCommand


@manager.command
def seed():
    user = models.Users()
    user.username = 'stacki'
    user.password = 'stacki'
    user.display_name = 'stacki'
    user.admin = True
    user.local = True
    user.created_on = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()

manager.add_command('db', MigrateCommand)

manager.run()
