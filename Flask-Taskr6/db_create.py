# -*- coding:Utf8 -*-


from project import db

########################
#    Main Program :    #
########################


if __name__ == '__main__':
    # Initialize database schema (all tables, views, triggers)
    db.create_all()

    # Commit changes
    db.session.commit()
