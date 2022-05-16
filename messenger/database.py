from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Client(Base):
    __tablename__ = 'client'

    login = Column(String, primary_key=True)
    info = Column(String)

    def __init__(self, login, info):
        self.login = login
        self.info = info

    def __repr__(self):
        return f'{self.__class__.__name__}' \
               f'({self.login}, {self.info})'


class ClientHist(Base):
    __tablename__ = 'client_hist'

    login_time = Column(DateTime, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.login'), nullable=False)
    ip_addr = Column(String)

    def __init__(self, log_time, cli_id, ip_addr):
        self.login_time = log_time
        self.client_id = cli_id
        self.ip_addr = ip_addr

    def __repr__(self):
        return f'{self.__class__.__name__}' \
               f'({self.login_time}, ' \
               f'({self.client_id}, ' \
               f'{self.ip_addr})'


class ContactList(Base):
    __tablename__ = 'contact_list'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('client.login'), nullable=False)
    client_id = Column(Integer, ForeignKey('client.login'), nullable=False)

    def __init__(self, key, own_id, cli_id):
        self.id = key
        self.owner_id = own_id
        self.client_id = cli_id

    def __repr__(self):
        return f'{self.__class__.__name__}' \
               f'({self.id}, ' \
               f'{self.owner_id}, ' \
               f'{self.client_id})'


if __name__ == "__main__":

    engine = create_engine('sqlite:///database.sqlite', echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    client_1 = Client('client_1', 'information')
    session.add(client_1)
    client_2 = Client('client_2', 'information')
    session.add(client_2)
    client_3 = Client('client_3', 'information')
    session.add(client_3)

    contact_1 = ContactList(1, 'client_1', 'client_2')
    session.add(contact_1)
    contact_2 = ContactList(2, 'client_1', 'client_3')
    session.add(contact_2)

    q1 = session.query(Client).all()
    q2 = session.query(ContactList).all()
    print(q1)
    print(q2)

    session.commit()
