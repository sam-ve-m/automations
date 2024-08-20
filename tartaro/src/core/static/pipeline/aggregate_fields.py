from src.core.static.pipeline.base.join_many_collections_pipeline import JoinCollections


class AggregateFields(JoinCollections):
    evidence_constraints = {'$addFields': {'constraint': '$object.constraint'}}
    clean_matches_fields = {'$project': {
        'object.constraint': 0,
        'object.origin': 0,
        'object.outsider': 0,
        'object.street_events': 0,
    }}
    wrap_keys_in_a_object = {'$addFields': {'object': {'$objectToArray': '$object'}}}
    destruct_fields_tickers = {'$unwind': '$object'}
    format_ticker_fields = {'$project': {
            'quote_type': '$constraint',
            'constraint': {'$concat': ['$constraint', ':', '$object.k']},
            'ticker_value': [{'k': '$_id', 'v': '$object.v'}],
            'field': '$object.k',
            '_id': 0
    }}
    wrap_fields_in_a_object = {'$addFields': {'ticker_value': {'$arrayToObject': '$ticker_value'}}}
    group_quote_types_fields = {'$group': {
        '_id': '$constraint',
        'quote_type': {'$first': '$quote_type'},
        'field': {'$first': '$field'},
        'tickers': {'$push': '$ticker_value'}
    }}
    format_quote_type_fields_for_group = {'$project': {
        '_id': '$quote_type',
        'object': [{
            'k': '$field',
            'v': '$tickers'
        }]
    }}
    wrap_types_in_a_object = {'$addFields': {'object': {'$arrayToObject': '$object'}}}
    group_quote_types = {'$group': {
        '_id': '$_id',
        'fields': {'$mergeObjects': '$object'}
    }}

    @classmethod
    async def get_pipeline(cls, collections: list, filter_query: dict):
        pipeline = [
            cls.filter_constraints_in_original_collection,
            cls.mark_objects_in_original_collection,
            *(cls.append_collection(collection) for collection in collections),
            cls.union_collections,
            cls.filter_matches(filter_query),
            cls.evidence_constraints,
            cls.clean_matches_fields,
            cls.wrap_keys_in_a_object,
            cls.destruct_fields_tickers,
            cls.format_ticker_fields,
            cls.wrap_fields_in_a_object,
            cls.group_quote_types_fields,
            cls.format_quote_type_fields_for_group,
            cls.wrap_types_in_a_object,
            cls.group_quote_types,
        ]
        return pipeline
