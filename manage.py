#from flask migrate import Migrate,MigrateCommand
from flask_script import Manager
from app import app,db

manager=Manager(app)
#migrate=Migrate(app,db)
#b.add_command(db,MigrateCommand)

if __name__=="__main__":
    app.config['DEBUG']=True
    manager.run()
