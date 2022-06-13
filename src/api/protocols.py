from typing import List

# from src.user.models import (
#     StatsAddV12,
# )

class UserServiceProtocol:
    async def push_answers(self, counts: int) -> None:
        raise NotImplementedError

    # def get_last_answer(self, id_answer) -> List[StatsAddV12]:
    #     raise NotImplementedError

