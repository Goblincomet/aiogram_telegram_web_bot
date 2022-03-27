from aiogram.dispatcher.filters.builtin import Regexp
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.default import get_default_markup
from bot.keyboards.inline import get_language_inline_markup
from loader import dp, _, i18n
from models import User
from services.users import edit_user_language


@dp.callback_query_handler(Regexp('^lang_(\w\w)$'))
async def change_language(callback_query: CallbackQuery, regexp: Regexp, session: AsyncSession, user: User):
    language = regexp.group(1)

    await edit_user_language(session, callback_query.from_user.id, language)
    i18n.set_user_locale(language)

    await callback_query.message.answer(_('Language changed successfully\n'
                                          'Press /help to find out how I can help you'),
                                        reply_markup=get_default_markup(user))
    await callback_query.message.delete()


@dp.message_handler(commands=['lang', 'settings'])
async def bot_start(message: Message):
    text = _('Choose your language')

    await message.answer(text, reply_markup=get_language_inline_markup())