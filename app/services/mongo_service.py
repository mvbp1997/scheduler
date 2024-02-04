from pymongo import MongoClient
from flask import json
from nanoid import generate


class MongoService:
    def __init__(self, data):
        self.client = MongoClient("mongodb://localhost:5000/")
        self.data = data

        database = data["database"]
        collection = data["collection"]
        cursor = self.client[database]
        self.collection = cursor[collection]

    # return all documents in collection
    def read_all(self, filter={}):
        documents = self.collection.find(filter)
        return [
            {item: data[item] for item in data if item != "_id"} for data in documents
        ]

    # read and return a single document in collection
    def read(self, id: str):
        filter = {"id": id}
        document = self.collection.find_one(filter)
        return {item: document[item] for item in document if item != "_id"}

    # write one document to collection
    def write(self, data):
        new_document = data
        new_document["id"] = generate()

        response = self.collection.insert_one(new_document)
        return {"Status": "Success", "id": new_document["id"]}

    # update one document in collection
    def update(self, id: str, data):
        if id is None or id == "" or data == {}:
            raise Exception("Must provide ID and data (to be updated)")

        filter = {"id": id}
        updated_data = {"$set": data}
        response = self.collection.update_one(filter, updated_data)
        return {
            "Status": (
                "Successfully Updated"
                if response.modified_count > 0
                else "Nothing was updated."
            )
        }

    # delete one document in collection
    def delete(self, id: str):
        if id is None or id == "":
            raise Exception("Must provide ID and data (to be updated)")

        filter = {"id": id}
        response = self.collection.delete_one(filter)
        return {
            "Status": (
                "Successfully Deleted"
                if response.deleted_count > 0
                else "Document not found."
            )
        }


# if __name__ == "__main__":
#     mongo_obj = MongoService(
#         {
#             "database": "TestDb",
#             "collection": "people",
#         }
#     )
#     # print(json.dumps(mongo_obj.write({"Document": {"id": "abcd"}}), indent=4))
#     # print(json.dumps(mongo_obj.write({"Document": {"id": "1234"}}), indent=4))

#     print(json.dumps(mongo_obj.update("abcd", {"name": "Mark"}), indent=4))
#     print(json.dumps(mongo_obj.read("abcd"), indent=4))
