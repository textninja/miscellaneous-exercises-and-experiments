import asyncio as aio
import random

def mkworker(mean, logprefix="", next=lambda: 0):
  async def _():
    time_to_work = max(random.normalvariate(mean, mean*0.2), 0)
    print(f"{logprefix}Waiting {time_to_work}")
    await aio.sleep(time_to_work)
    next()
  return _