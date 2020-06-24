from bson import ObjectId


def to_object_id(entity_id):
    return ObjectId(entity_id)
