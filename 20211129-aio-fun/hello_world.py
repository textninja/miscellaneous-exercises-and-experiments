import sys
import random
import asyncio as aio

async def main():
  for c in "Hello world!\n":
    await aio.sleep(max(0, random.normalvariate(0.1, 0.05)))    
    print(c, end="") ; sys.stdout.flush()


aio.run(main())