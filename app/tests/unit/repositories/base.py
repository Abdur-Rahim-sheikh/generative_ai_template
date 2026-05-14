from uuid import uuid4


class BaseRepositoryCommonTests:
    async def test_save_assigns_id(self, repo, sample_entity):
        sample_entity.id = None
        await repo.save(sample_entity)
        assert sample_entity.id is not None

    async def test_save_ignores_existing_id(self, repo, sample_entity):
        existing_id = uuid4()
        sample_entity.id = existing_id
        await repo.save(sample_entity)
        assert sample_entity.id is not None and sample_entity.id != existing_id

    async def test_get_returns_saved_entity(self, repo, sample_entity):
        saved = await repo.save(sample_entity)
        fetched = await repo.get(saved.id)
        assert fetched == saved

    async def test_delete_removes_entity(self, repo, sample_entity):
        saved = await repo.save(sample_entity)
        await repo.delete(saved.id)
        fetched = await repo.get(saved.id)
        assert fetched is None
