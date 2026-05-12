from uuid import uuid4


class RepositoryContractTests:
    async def test_save_assigns_id(self, repo, sample_entity):
        """Entity without id gets one assigned on save."""
        sample_entity.id = None
        await repo.save(sample_entity)
        assert sample_entity.id is not None

    async def test_save_ignores_existing_id(self, repo, sample_entity):
        """Save must not overwrite an existing id."""
        existing_id = uuid4()
        sample_entity.id = existing_id
        await repo.save(sample_entity)
        assert sample_entity.id == existing_id

    async def test_get_returns_saved_entity(self, repo, sample_entity):
        saved = await repo.save(sample_entity)
        fetched = await repo.get(saved.id)
        assert fetched == saved

    async def test_delete_removes_entity(self, repo, sample_entity):
        saved = await repo.save(sample_entity)
        await repo.delete(saved.id)
        fetched = await repo.get(saved.id)
        assert fetched is None
