import sys
if sys.version_info >= (3, 13):
    import imghdr
    sys.modules['imghdr'] = imghdr

import asyncio

# ... the rest of the content in bot.py, ensuring to remove the duplicate __name__ == '__main__' block and to fix the async main function ...

async def main():
    async with app:
        # rest of the main function code
