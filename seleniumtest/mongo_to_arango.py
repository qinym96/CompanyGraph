from pymongo import MongoClient
from arango import ArangoClient

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client['Gree6']

arango_client = ArangoClient(protocol='http', host='localhost', port=8529)
arango_db = arango_client.db('test_db', username='root', password='')




def main():
    entity = arango_db.create_collection('entity')
    # person = arango_db.create_collection('person')

    entity = arango_db['entity']
    entity.insert_many(mongo_db['CompanyItem'].find({}, {"_id": 0}))
    entity.insert_many(mongo_db['PersonItem'].find({}, {"_id": 0}))

    # person = arango_db['person']
    # person.insert_many(mongo_db['ExecutiveItem'].find({},{"_id":0}))

    graph =arango_db.create_graph('graph2')
    edge = graph.create_edge_definition(
        edge_collection='relation',
        from_vertex_collections=['entity'],
        to_vertex_collections=['entity']
    )

    # relation = arango_db.create_collection('relation')
    relation = arango_db['relation']
    for i in mongo_db['RelationItem'].find({}):
        r = {"_from": entity.name + '/' + i["from_key"], "_to": entity.name + '/' + i["to_key"], "name" : i["name"]}
        print(r)
        relation.insert(r)

    # result = graph.traverse(
    #     # start_vertex='students/01',
    #     direction='outbound',
    #     strategy='breadthfirst'
    # )


if __name__ == '__main__':
    main()