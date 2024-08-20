class CountCollectionKeys:
    count_keys_pipeline = [
        {'$project': {
            'array_of_key_value': {'$objectToArray': '$$ROOT'}
        }},
        {'$unwind': '$array_of_key_value'},
        {'$project': {
            'key': '$array_of_key_value.k',
            'covered_item':  {"$convert": {
              "input": "$_id",
              "to": "string"
            }}
        }},
        {'$group': {
            '_id': '$key',
            'covered_items': {'$addToSet': '$covered_item'}
        }}
    ]
