from db.models import Chat, Member
from db.db import new_session


class ChatService:

    def create_chat(self, chat_obj):
        chat_id = chat_obj['chat']['id']
        chat_name = chat_obj['chat']['title']
        owner_id = chat_obj['from']['id']
        owner_name = chat_obj['from']['username']

        with new_session() as session:
            chat = session.query(Chat).filter_by(telegram_id=chat_id).first()
            if chat:
                return
            new_chat = Chat(
                telegram_id=chat_id,
                name=chat_name,
                manager_id=owner_id
            )
            session.add(new_chat)
            session.flush()

            member = Member(
                name=owner_name,
                telegram_id=owner_id,
                chat_id=new_chat.id
            )
            session.add(member)
            session.commit()

    def add_member(self, member_obj, chat_obj):
        with new_session() as session:
            chat = session.query(Chat).filter_by(telegram_id=chat_obj['id']).first()
            print(chat.id)

            member = session.query(Member).filter_by(telegram_id=member_obj['id'], chat_id=chat.id).first()
            if member:
                return

            new_member = Member(
                name=member_obj['username'],
                telegram_id=member_obj['id'],
                chat_id=chat.id
            )
            session.add(new_member)
            session.commit()


    def get_chats(self, member_id):
        with new_session() as session:
            members = session.query(Member).filter_by(telegram_id=member_id).all()
            chats = [member.chat_id for member in members]

            chats = session.query(Chat).filter(Chat.id.in_(chats)).all()
            return chats

    def get_chat_id(self, name):
        with new_session() as session:
            chat = session.query(Chat).filter_by(name=name).first()
            return chat.id
