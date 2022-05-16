from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class ContactList(Base):
    __tablename__ = 'contact_list'

    login = Column(String, primary_key=True)
    info = Column(String)

    def __init__(self, login, info):
        self.login = login
        self.info = info

    def __repr__(self):
        return f'{self.__class__.__name__}' \
               f'({self.login}, {self.info})'


class MessageHist(Base):
    __tablename__ = 'message_hist'

    message_time = Column(DateTime, primary_key=True)
    client_id = Column(Integer, ForeignKey('contact_list.login'), nullable=False)

    def __init__(self, log_time, cli_id, ip_addr):
        self.login_time = log_time
        self.client_id = cli_id

    def __repr__(self):
        return f'{self.__class__.__name__}' \
               f'({self.message_time}, ' \
               f'({self.client_id}, ' \



if __name__ == "__main__":

    engine = create_engine('sqlite:///client_database.sqlite', echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    contact_1 = ContactList('client_2', 'information')
    session.add(contact_1)
    contact_2 = ContactList('client_3', 'information')
    session.add(contact_2)

    q1 = session.query(ContactList).all()
    print(q1)

    session.commit()
