from qrodizio.ext.database import db

class dbFacade:
    def add_commit_session(db, o):
        db.session.add(o)
        db.session.commit()

    def delete_commit_session(db, o):
        db.session.delete(o)
        db.session.commit()    