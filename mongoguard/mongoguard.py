# python
# File: `mongoguard/mongoguard.py`

from typing import Any

import pymongo
import logging

from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("db.log"),
        logging.StreamHandler()
    ]
)


class MongoGuard:
    """
    A class to manage MongoDB operations efficiently and safely.
    Features
    ----------
        1. Auto error handling
        2. Logging for operations
        3. In and Out Pydantic BaseModels only ( this allows data validation )
    ----------

    Note: Only create one instance of this class per connection
    """

    def __init__(self, mongo_url: str, db_name: str, collection_name: str):
        self.conn = pymongo.MongoClient(mongo_url)
        self.db = self.conn[db_name]
        self.collection = self.db[collection_name]

        logging.info(f"Connected to {db_name}/{collection_name}")

    def create_collection(self, collection_name: str) -> bool:
        try:
            if collection_name not in self.db.list_collection_names():
                self.db.create_collection(collection_name)
                logging.info(f"New Collection Created: {collection_name}")
                return True
            logging.warning(f"Collection already exists: {collection_name}")
            return False
        except Exception as e:
            logging.error(f"Collection creation failed: {e}")
            raise ValueError(f"Collection creation failed: {e}")

    def create_database(self, db_name: str) -> bool:
        try:
            if db_name not in self.conn.list_database_names():
                self.db = self.conn[db_name]
                logging.info(f"New Database Created and Selected: {db_name}")
                return True
            logging.warning(f"Database already exists: {db_name}")
            return False
        except Exception as e:
            logging.error(f"Database creation failed: {e}")
            raise ValueError(f"Database creation failed: {e}")

    def fetch_collection(self, out_model: BaseModel) -> list[BaseModel]:
        try:
            cursor = self.collection.find()
            result = []
            for entry in cursor:
                if "_id" in entry:
                    entry["_id"] = str(entry["_id"])
                result.append(out_model.model_validate(entry))
            logging.info(f"Fetched collection data, total records: {len(result)}")
            return result
        except Exception as e:
            logging.error(f"Data retrieval failed: {e}")
            raise Exception(f"Data retrieval failed: {e}")


    def fetch_entries(self, out_model: BaseModel, *args: Any, **kwargs: Any) -> list[BaseModel]:
        try:
            cursor = self.collection.find(*args, **kwargs)
            result = []
            for entry in cursor:
                if "_id" in entry:
                    entry["_id"] = str(entry["_id"])
                result.append(out_model.model_validate(entry))
            logging.info(f"Fetched data, total records: {len(result)}")
            return result
        except Exception as e:
            logging.error(f"Data retrieval failed: {e}")
            raise Exception(f"Data retrieval failed: {e}")


    def fetch_entry(self, out_model: BaseModel, *args: Any, **kwargs: Any) -> BaseModel | None:
        try:
            entry = self.collection.find_one(*args, **kwargs)
            if entry and "_id" in entry:
                entry["_id"] = str(entry["_id"])
            logging.info(f"Fetched single entry: {entry.get('_id') if entry else 'None'}")
            return out_model.model_validate(entry) if entry else None
        except Exception as e:
            logging.error(f"Data retrieval failed: {e}")
            raise Exception(f"Data retrieval failed: {e}")


    def insert_model(self, model: BaseModel) -> bool:
        try:
            result = self.collection.insert_one(model.model_dump())
            logging.info(f"Inserted Data: {result.inserted_id}")
            return result.acknowledged
        except Exception as e:
            logging.error(f"Data insertion failed: {e}")
            raise Exception(f"Data insertion failed: {e}")

    def insert_models(self, models: list[BaseModel]) -> bool:
        try:
            data = [model.model_dump() for model in models]
            result = self.collection.insert_many(data)
            logging.info(f"Inserted Data: {result.inserted_ids}")
            return result.acknowledged
        except Exception as e:
            logging.error(f"Data insertion failed: {e}")
            raise Exception(f"Data insertion failed: {e}")


    def update_entry(self, query: dict, update_data: dict) -> bool:
        try:
            result = self.collection.update_one(query, {'$set': update_data})
            logging.info(f"Updated {result.modified_count} entries matching {query}")
            return result.acknowledged
        except Exception as e:
            logging.error(f"Data update failed: {e}")
            raise Exception(f"Data update failed: {e}")


    def delete_entry(self, query: dict) -> bool:
        try:
            result = self.collection.delete_one(query)
            logging.info(f"Deleted {result.deleted_count} entries matching {query}")
            return result.acknowledged
        except Exception as e:
            logging.error(f"Data deletion failed: {e}")
            raise Exception(f"Data deletion failed: {e}")


    def delete_entries(self, query: dict) -> bool:
        try:
            result = self.collection.delete_many(query)
            logging.info(f"Deleted {result.deleted_count} entries matching {query}")
            return result.acknowledged
        except Exception as e:
            logging.error(f"Data deletion failed: {e}")
            raise Exception(f"Data deletion failed: {e}")

    def drop_collection(self) -> bool:
        try:
            self.collection.drop()
            logging.info(f"Dropped Collection")
            return True
        except Exception as e:
            logging.error(f"Collection drop failed: {e}")
            raise Exception(f"Collection drop failed: {e}")


    def drop_database(self) -> bool:
        try:
            self.conn.drop_database(self.db.name)
            logging.info(f"Dropped Database {self.db.name}")
            return True
        except Exception as e:
            logging.error(f"Database drop failed: {e}")
            raise Exception(f"Database drop failed: {e}")


    def close_connection(self):
        try:
            self.conn.close()
            logging.info(f"Closed MongoDB connection")
        except Exception as e:
            logging.error(f"Closing connection failed: {e}")
            raise Exception(f"Closing connection failed: {e}")


    def count_documents(self, query: dict = ()) -> int:
        try:
            count = self.collection.count_documents(query)
            logging.info(f"Counted {count} documents matching {query}")
            return count
        except Exception as e:
            logging.error(f"Counting documents failed: {e}")
            raise Exception(f"Counting documents failed: {e}")


    def aggregate(self, pipeline: list[dict]) -> list[dict]:
        try:
            cursor = self.collection.aggregate(pipeline)
            result = list(cursor)
            logging.info(f"Aggregated data, total records: {len(result)}")
            return result
        except Exception as e:
            logging.error(f"Aggregation failed: {e}")
            raise Exception(f"Aggregation failed: {e}")