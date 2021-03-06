"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import os
from services.project import ProjectService
from services.dashboard import DashboardService
from services.state import StateMenuService

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from db.models import Project
from db.db import new_session
from services.chat import ChatService


API_TOKEN = os.getenv("TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.my_chat_member_handler()
async def on_bot_join(channel: types.Chat):
    service = ChatService()
    bot_ = channel['new_chat_member']
    status = bot_['status']

    if status == "member":
        await bot.send_message(channel['chat']['id'], 'Hi, everyone!')

    service.create_chat(channel)


@dp.message_handler(commands=['registration'])
async def register_member(message: types.Message):
    service = ChatService()
    service.add_member(message['from'], message['chat'])
    member_name = message['from']['username']
    await bot.send_message(message['chat']['id'], f"{member_name}, can see the chat in bot")


@dp.message_handler(commands=['craftdashboard'])
async def craft_dashboard(message: types.Message):

    user_id = message.from_user.id
    state = StateMenuService(user_id=user_id)
    state.change_state('create_dashboard')
    await message.reply(f'Name the dashboard:')

@dp.message_handler(commands=['createdashboard'])
async def create_dashboard(message: types.Message):


    user_id = message.from_user.id
    state = StateMenuService(user_id=user_id)
    project_name = state.choices_project


    if not state.choices_project:
        await message.reply(f'You can choice the project')
        return
    with new_session() as session:
        project = session.query(Project).filter_by(name=project_name).first()

    service = DashboardService()
    name = message.text.split(' ')[1]
    dashboard = service.create_dashboard(name, project.id)
    await message.reply(f'Dashboard {name} has been created')


@dp.message_handler(commands=['craftproject'])
async def craft_project(message: types.Message):
    user_id = message.from_user.id
    state = StateMenuService(user_id=user_id)
    state.change_state('create_project')
    await message.reply(f'Name the project (1 word without space):')



@dp.message_handler(commands=['createproject'])
async def create_project(message: types.Message):
    user_id = message.from_user.id
    service = ProjectService()
    name = message.text.split(' ')[1]
    project = service.create_project(name, user_id)
    state = StateMenuService(user_id)
    state.change_state('init')
    dashboard_id = 1
    kb = state.get_keyboard()

    await message.reply(f'Project {name} has been created!', reply_markup=kb)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user_id = message.from_user.id
    state = StateMenuService(user_id=user_id)
    state.change_state('pre_init')
    kb = state.get_keyboard(member_id=user_id)
    state.change_state('choice_chat')
    await message.reply("Hi, I'm managment bot!\nI'll help you with installation.\nYou need to do my commands.\nGood luck!\nChoose group:", reply_markup=kb)


@dp.message_handler(commands=['projects'])
async def projects(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    user_id = message.from_user.id
    service = ProjectService()
    state = StateMenuService(user_id=user_id)
    chat_id= ChatService().get_chat_id(state.choices_chat)
    print(chat_id)
    projects = service.get_projects(user_id=user_id, chat_id=chat_id)
    state.change_state('projects')
    kb = state.get_keyboard(projects=projects)
    state.change_state('choice')
    await message.reply("Choose project", reply_markup=kb)

@dp.message_handler(commands=['back'])
async def back(message: types.Message):
    user_id = message.from_user.id
    state = StateMenuService(user_id=user_id)
    state.change_state('init')
    kb = state.get_keyboard()
    state.choices_project = None
    await message.reply("0", reply_markup=kb)


@dp.message_handler()
async def on_message(message: types.Message):
    user_id = message.from_user.id
    state = StateMenuService(user_id=user_id)
    project_name = state.choices_project
    if state.state == "create_project":
        service = ProjectService()
        chat_service = ChatService()
        name = message.text.split(' ')[0]
        chat = chat_service.get_chat_id(state.choices_chat)

        service.create_project(name=name, user_id=user_id, chat_id=chat)

        state.change_state('init')
        kb = state.get_keyboard()
        await message.reply(f'Project {name} has been created!', reply_markup=kb)

    elif state.state == 'choice_chat':
        chat = message.text
        state.choices_chat = chat

        state.change_state('init')
        kb = state.get_keyboard()
        await message.reply(f'You can create or choose project', reply_markup=kb)

    elif state.state == "choice":
        project = message.text
        state.choices_project = project
        kb = state.get_keyboard()
        state.change_state("choice_dashboard")
        await message.reply(f'You can create or choose dashboard', reply_markup=kb)

    elif state.state == "choice_dashboard":
        dashboard = message.text
        service = DashboardService()

        dashboard_id = service.get_dashboard(dashboard).id
        print(dashboard_id)

        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Dashboard",
                        web_app=types.WebAppInfo(url=f'https://lakeofcolors.com?dashboard_id={dashboard_id}'),
                    )
                ]
            ]
        )

        await message.answer("see dashboard", reply_markup=markup)

    elif state.state == "create_dashboard":
        with new_session() as session:
            project = session.query(Project).filter_by(name=project_name).first()

        service = DashboardService()
        name = message.text.split(' ')[0]
        service.create_dashboard(name, project.id)

        state.change_state('init')
        kb = state.get_keyboard()
        await message.reply(f'Project {name} has been created!', reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
