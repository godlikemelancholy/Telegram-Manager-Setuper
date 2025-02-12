from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon import functions
from telethon.tl.types import *
from telethon import types
import asyncio
import os


class Telegram:
    def __init__(self, key_file):
        with open(key_file) as kf:
            key = kf.read()
        self.__session = TelegramClient(StringSession(key), 17463049, "bd4bbac77f54cd096ede52dd2e8e2e50", system_version="4.16.30-vxCUSTOM")
        self.__peer = 777000

    async def kill_sessions(self, logger):
        await self.__session.connect()
        GetSessions = await self.__session(functions.account.GetAuthorizationsRequest())
        if len(GetSessions.authorizations) > 1:
            for ss in GetSessions.authorizations:
                SessionHash = ss.hash
                SessionIp = ss.ip
                try:
                    result = await self.__session(functions.account.ResetAuthorizationRequest(hash=SessionHash))
                    logger.debug("Session Killed     :\t" + str(SessionIp))
                except:
                    pass
        else:
            logger.debug("All sessions killed!")


    async def set_username(self, username):
        await self.__session.connect()
        try:
            await self.__session(functions.account.UpdateUsernameRequest(username.rstrip() + '_w3'))
            await self.__session(functions.account.UpdateProfileRequest(first_name=username.rstrip(), last_name=''))
            return True
        except Exception as e:
            if 'A wait' in str(e):
                raise Exception('Timeout')
            if 'deleted/' in str(e):
                raise Exception('Account banned')
            return False

    async def set_privacy(self):
        await self.__session.connect()
        await self.__session(
            functions.account.SetPrivacyRequest(
                key=types.InputPrivacyKeyChatInvite(),
                rules=[types.InputPrivacyValueDisallowAll()]
            )
        )
        await self.__session(
            functions.account.SetPrivacyRequest(
                key=types.InputPrivacyKeyPhoneNumber(),
                rules=[types.InputPrivacyValueDisallowAll()]
            )
        )
        await self.__session(
            functions.account.SetPrivacyRequest(
                key=types.InputPrivacyKeyStatusTimestamp(),
                rules=[types.InputPrivacyValueDisallowAll()]
            )
        )
        await self.__session(
            functions.account.SetPrivacyRequest(
                key=types.InputPrivacyKeyForwards(),
                rules=[types.InputPrivacyValueDisallowAll()]
            )
        )
        await self.__session(
            functions.account.SetPrivacyRequest(
                key=types.InputPrivacyKeyPhoneCall(),
                rules=[types.InputPrivacyValueDisallowAll()]
            )
        )
        await self.__session(
            functions.account.SetPrivacyRequest(
                key=types.InputPrivacyKeyPhoneCall(),
                rules=[types.InputPrivacyValueDisallowAll()]
            )
        )
        await self.__session(
            functions.account.SetPrivacyRequest(
                key=types.InputPrivacyKeyPhoneP2P(),
                rules=[types.InputPrivacyValueDisallowAll()]
            )
        )

    async def set_2fa(self, passwd):
        await self.__session.connect()
        try:
            await self.__session.edit_2fa(new_password=passwd)
        except:
            await self.__session.edit_2fa(current_password='1488', new_password=passwd)

    async def set_avatar(self, path):
        await self.__session.connect()
        await self.__session(
            functions.photos.DeletePhotosRequest(
                await self.__session.get_profile_photos('me')
            )
        )
        file = await self.__session.upload_file(path)
        await self.__session(
            functions.photos.UploadProfilePhotoRequest(file=file)
        )

