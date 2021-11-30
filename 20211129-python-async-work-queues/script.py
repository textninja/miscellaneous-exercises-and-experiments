import asyncio as aio
import aiosqlite
from mkworker import mkworker

async def main():

  WORKERS = [
    mkworker(2, "1: ", lambda: WORK_QUEUES[1].put_nowait(WORKERS[1])),
    mkworker(4, "2: ", lambda: WORK_QUEUES[2].put_nowait(WORKERS[2])),
    mkworker(1, "3: ", lambda: WORK_QUEUES[3].put_nowait(WORKERS[3])),
    mkworker(3, "4: ", lambda: stop_iteration_if_queues_are_empty(WORK_QUEUES))]

  WORK_QUEUES = [
    aio.Queue(),
    aio.Queue(),
    aio.Queue(),
    aio.Queue()]

  for i in range(2):
    WORK_QUEUES[0].put_nowait(WORKERS[0])

  try:
    await aio.gather(
      queue_process_loop(WORK_QUEUES[0])(),
      queue_process_loop(WORK_QUEUES[1])(),
      queue_process_loop(WORK_QUEUES[2])(),
      queue_process_loop(WORK_QUEUES[3])())
  except RuntimeError:
    print("Done!")

def queue_process_loop(work_queue):
  async def _():
    while True:
      job = await work_queue.get()
      await job()
  return _

def stop_iteration_if_queues_are_empty(queues):
  if all(queue.empty() for queue in queues):
    raise StopIteration()

aio.run(main())