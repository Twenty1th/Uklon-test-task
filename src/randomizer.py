import asyncio
import logging

from application.randomizer.randomizer import Randomizer, send_data
from logger import setup_logger
from settings import CONFIG


async def main():
    randomizer = Randomizer()
    while True:
        try:
            await send_data(randomizer.generate_random_driver_info())
            await asyncio.sleep(CONFIG.randomizer.requests_delay)

        except asyncio.CancelledError:
            break

        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    setup_logger()
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())

    except KeyboardInterrupt:
        loop.close()

    finally:
        loop.close()
        logging.info("Gracefully shutdown complete.")
