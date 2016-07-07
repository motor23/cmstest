from ikcms.ws_components.auth.base import encrypt_password
from models.main import User


def initialize(session):
    print('Adding root user')
    user = session.query(User).filter_by(login='root').first()
    if user is None:
        user = User()
    user.login = 'root'
    user.password = encrypt_password('root')
    user.name = 'Administrator'
    session.merge(user)
    session.commit()
