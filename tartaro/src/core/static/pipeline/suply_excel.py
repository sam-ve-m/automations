from src.core.static.pipeline.base.join_many_collections_pipeline import JoinCollections


class SupplyExcel(JoinCollections):
    unwrap_tickers = {'$replaceRoot': {'newRoot': '$object'}}
    clean_aggregation_fields = {'$project': {
        'outsider': 0,
        'origin': 0,
        'constraint': 0
    }}
    unwrap_keys = {'$project': {'keys': {'$objectToArray': '$$ROOT'}}}
    destruct_keys = {'$unwind': '$keys'}
    group_keys = {'$group': {'_id': '$keys.k'}}

    @classmethod
    async def get_pipeline(cls, collections: list, filter_query: dict):
        pipeline = [
            cls.filter_constraints_in_original_collection,
            cls.mark_objects_in_original_collection,
            *(cls.append_collection(collection) for collection in collections),
            cls.union_collections,
            cls.filter_matches(filter_query),
            cls.unwrap_tickers,
            cls.clean_aggregation_fields
        ]
        return pipeline

    @classmethod
    async def get_distinct_keys_pipeline(cls):
        pipeline = [
            cls.unwrap_keys,
            cls.destruct_keys,
            cls.group_keys,
        ]
        return pipeline
