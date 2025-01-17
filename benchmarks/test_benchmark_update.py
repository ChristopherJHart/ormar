import random
import string
from typing import List

import pytest

from benchmarks.conftest import Author

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("num_models", [10, 20, 40])
async def test_updating_models_individually(
    aio_benchmark, num_models: int, authors_in_db: List[Author]
):
    starting_first_name = authors_in_db[0].name

    @aio_benchmark
    async def update(authors: List[Author]):
        for author in authors:
            a = await author.update(
                name="".join(random.sample(string.ascii_letters, 5))
            )

    update(authors_in_db)
    author = await Author.objects.get(id=authors_in_db[0].id)
    assert author.name != starting_first_name
