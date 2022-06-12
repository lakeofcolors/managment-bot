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



API_TOKEN = os.getenv("TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['craftdashboard'])
async def craft_dashboard(message: types.Message):

    user_id = message.from_user.id
    state = StateMenuService(user_id=user_id)
    state.change_state('create_dashboard')
    await message.reply(f'Name is project:')

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
    await message.reply(f'Name is project:')



@dp.message_handler(commands=['createproject'])
async def create_project(message: types.Message):
    user_id = message.from_user.id
    service = ProjectService()
    name = message.text.split(' ')[1]
    project = service.create_project(name, user_id)
    state = StateMenuService(user_id)
    state.change_state('init')
    dashboard_id = 1
    #kb = state.get_keyboard()markup = types.InlineKeyboardMarkup(
    murkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Dashboard",
                    web_app=types.WebAppInfo(url=f'https://lakeofcolors.com?dashboard_id={dashboard_id}&user_id=1'),
                )
            ]
        ]
    )
    await message.answer(f'Project {name} has been created!', reply_markup=murkup)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user_id = message.from_user.id
    state = StateMenuService(user_id=user_id)
    state.change_state('init')
    kb = state.get_keyboard()

    await message.reply('Hi', reply_markup=kb)


@dp.message_handler(commands=['projects'])
async def projects(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    user_id = message.from_user.id
    service = ProjectService()
    projects = service.get_projects(user_id)
    state = StateMenuService(user_id=user_id)
    state.change_state('projects')
    kb = state.get_keyboard(projects=projects)
    state.change_state('choice')
    await message.reply(message.text, reply_markup=kb)

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
        name = message.text.split(' ')[0]
        service.create_project(name=name, user_id=user_id)

        state.change_state('init')
        kb = state.get_keyboard()
        await message.reply(f'Project {name} has been created!', reply_markup=kb)
    if state.state == "choice":
        project = message.text
        state.choices_project = project
        kb = state.get_keyboard()
        await message.reply(f'Choice dashboard', reply_markup=kb)

    if state.state == "create_dashboard":

        with new_session() as session:
            project = session.query(Project).filter_by(name=project_name).first()

        service = DashboardService()
        name = message.text.split(' ')[0]
        service.create_dashboard(name, project.id)

        state.change_state('init')
        kb = state.get_keyboard()
        await message.reply(f'Project {name} has been dashboard!', reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
