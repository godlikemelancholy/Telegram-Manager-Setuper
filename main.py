import tg
import os
import shutil
import loguru
import asyncio
import random

async def main():
    sessions = os.listdir('sessions/new')
    with open('names.txt') as f:
        names = f.readlines()

    for session in sessions:
        try:
            acc = tg.Telegram(f'sessions/new/{session}')
            photo = 'photo/' + random.choice(os.listdir('photo'))

            changed = False
            while not changed:
                username = names.pop(random.randint(0, len(names) - 1))
                try:
                    result = await acc.set_username(username)
                    if result:
                        logger.debug(f'Username changed: {username.rstrip()}')
                        changed = True
                except Exception as e:
                    if 'Account banned' in str(e):
                        shutil.move(f'sessions/new/{session}', f'sessions/invalid/{session}')
                        break

            if not changed:
                continue


            await acc.set_privacy()
            logger.debug(f'Privacy settings changed!')

            await acc.kill_sessions(logger)

            await acc.set_avatar(photo)
            logger.debug(f'Avatar changed!')

            await acc.set_2fa('12345678')
            logger.debug(f'2FA password changed!')

            logger.success(session + '   -> Done!')
        except Exception as e:
            logger.error(e)
        finally:
            await asyncio.sleep(2)

if __name__ == '__main__':
    logger = loguru.logger
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
