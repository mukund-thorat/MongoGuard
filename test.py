from pydantic import BaseModel

from mongoguard import MongoGuard

mongoguard = MongoGuard(
    mongo_url="mongodb+srv://mukund_thorat:D6YNumGyvpksMyv4@linkup.xzel6kw.mongodb.net/?retryWrites=true&w=majority&appName=LinkUp",
    db_name="LinkUp",
    collection_name="institutes"
)

class InstituteModel(BaseModel):
    name: str
    role_id: int
    description: str


print(mongoguard.fetch_collection(InstituteModel))
