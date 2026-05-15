from typing import Protocol


class IQueue(Protocol):
    async def publish(self, message):
        pass
