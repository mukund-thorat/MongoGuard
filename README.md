<p style="text-align: center;">
  <img src="https://raw.githubusercontent.com/mukund-thorat/MongoGuard/472509e283a7065a3bd3830b540cdd3121ca2711/res/mongoguard.svg" alt="Medusa Logo" width="120"/>
</p>

<h1 style="text-align: center;">MongoGuard</h1>

> A lightweight, optimistic, and efficient CRUD layer for MongoDB — built with safety, validation, built-in logging, and error handling, all designed for simplicity and reliability.

---
## 📌 Features
- ✅ Automatic error handling
- 🧩 Integrated logging for all operations
- 🔒 Full Pydantic model support
- 🔁 Type-safe input and output using Pydantic BaseModels

## 📦 Installation
```bash
pip install mongoguard
```

### Example
```python
from mongoguard import MongoGuard
from pydantic import BaseModel

mg = MongoGuard(
    mongo_url="mongodb://localhost:27017/",
    db_name="Example",
    collection_name="User"
)

class UserModel(BaseModel):
    id: int
    name: str
    email: str
    password: str

mg.fetch_collection(out_model=UserModel)
```

## ❤️ Contributing & Community
Created and maintained by **[Mukund Thorat](https://mukundthorat.framer.ai/)**.<br>
We welcome contributors to help improve MongoGuard! If you are interested in contributing or collaborating, please contact me via email: [mukundthorat.official@gmail.com](mailto:mukundthorat.official@gmail.com)

## 🔐 License
This project is licensed under the terms of the [MIT license](./LICENSE).