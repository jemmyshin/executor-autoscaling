from jina import requests, Executor
from jina.logging.logger import JinaLogger
from docarray import DocumentArray
import time
import asyncio


class AutoscalingExecutor(Executor):
    def __init__(self, init_time, process_time, **kwargs):
        super().__init__()
        self.logger = JinaLogger(self.__class__.__name__)

        self.logger.info(f"We are going to initialize executor ...")

        self.init_time = init_time
        self.process_time = process_time
        self._count = 0

        time.sleep(self.init_time)

        self.logger.info(f"initialize executor done!")

    @requests(on='/agenerate')
    async def agenerate(self, docs: 'DocumentArray', parameters=None, **kwargs):
        process_time = parameters.get('process_time', None)
        count = self._count
        self._count += 1
        await self._sleep(process_time or self.process_time)
        self.logger.info(f"async mode -- process done for count {count}, cost: {process_time or self.process_time}")

    async def _sleep(self, second):
        await asyncio.sleep(second)
        return

    @requests(on='/generate')
    def generate(self, docs: 'DocumentArray', parameters=None, **kwargs):
        process_time = parameters.get('process_time', None)
        count = self._count
        self._count += 1
        time.sleep(process_time or self.process_time)
        self.logger.info(f"sync mode -- process done for count {count}, cost: {process_time or self.process_time}")

    @requests(on='/mock')
    def mock(self, docs: 'DocumentArray', **kwargs):
        self.logger.info(f"we are in mocking error mode ...")
        raise ValueError("no hurry, this is a mock error")
