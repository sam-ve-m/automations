from src.core.static.pipeline.base.join_many_collections_pipeline import JoinCollections


class GetFilteredIds(JoinCollections):
    filter_only_for_id = {'$project': {'constraint': '$object.constraint'}}
    group_quote_types_ids = {'$group': {
        '_id': '$constraint',
        'tickers': {'$push': '$_id'}
    }}

    @classmethod
    async def get_pipeline(cls, collections: list, filter_query: dict):
        pipeline = [
            cls.filter_constraints_in_original_collection,
            cls.mark_objects_in_original_collection,
            *(cls.append_collection(collection) for collection in collections),
            cls.union_collections,
            cls.filter_matches(filter_query),
            cls.filter_only_for_id,
            cls.group_quote_types_ids,
        ]
        return pipeline
