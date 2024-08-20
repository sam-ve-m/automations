from abc import ABC, abstractmethod


class JoinCollections(ABC):
    filter_constraints_in_original_collection = {'$project': {
        '_id': 1,
        'constraint': {'$concat': [
            '$region', ':', '$quote_type', ':', '$quote_specification'
        ]},
    }}
    mark_objects_in_original_collection = {'$addFields': {'origin': 1}}
    union_collections = {'$group': {
        '_id': '$_id',
        'object': {'$mergeObjects': '$$ROOT'}
    }}

    @staticmethod
    def append_collection(collection: str) -> dict:
        return {'$unionWith': {
            'coll': collection,
            'pipeline': [{'$addFields': {'outsider': 1}}]
        }}

    @staticmethod
    def filter_matches(filter_query: dict):
        filter_query.update({
            f'object.{field}': {'$exists': True}
            for field in ['origin', 'outsider']
        })
        return {'$match': filter_query}

    @classmethod
    @abstractmethod
    def get_pipeline(cls, collections: list, filter_query: dict):
        pass
