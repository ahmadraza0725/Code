from sqlmodel import SQLModel, create_engine, Session, Field
from fastapi import FastAPI , HTTPException
app = FastAPI()
class User(SQLModel, table=True):
    user_id: int = Field(primary_key=True)
    name: str
    email: str

class Animal(SQLModel, table=True):
    animal_id: int = Field(primary_key=True)
    name: str
    age: int
    type: str
    species: str

url = "postgresql://postgres:12345678@localhost:5432/CRUD"
engine = create_engine(url, echo=True) 
# db_params = {
#     'host': 'localhost',
#     'database': 'CRUD',
#     'user': 'postgres',
#     'password': 12345678,
#     'port': 5432 
# }


# engine = create_engine(
#     f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}", echo= True
# )

# sqlite_file_name = "seconddata.db"
# # check same thread for fastapi 
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# connect_args = {"check_same_thread": False}
# engine = create_engine(sqlite_url, echo=True) added connect args for fastapi 
# engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
def on_startup():
    SQLModel.metadata.create_all(engine)

app.add_event_handler("startup", on_startup)

# @app.lifespan("startup")
# def on_startup():
#     SQLModel.metadata.create_all(engine)
# @app.post("/create")
# def create_table(table_name ):
#     with Session(engine) as session:
#         session.add(table_name)
#         session.commit()
#         session.refresh(table_name)
#         return table_name


class BaseCRUD:
    def __init__(self, table_name):
        self.table_name = table_name

    def create(self, **kwargs):
        with Session(engine) as session:
            statement = self.table_name(**kwargs)
            session.add(statement)
            session.commit()
            print(f"{self.table_name} created successfully!")

    def read(self, table_id):
        with Session(engine) as session:
            statement = session.get(self.table_name, table_id)
            if statement is not None:
                print("Showing Existing ID :")
                print(statement)
            else:
                print(f"This ID doesn't exists in  {self.table_name}")
                
    def update(self,table_id,**kwargs):
        with Session(engine) as session:
            statement = session.get(self.table_name,table_id)
            for key ,value in kwargs.items():
                setattr(statement , key , value)
            session.commit()
            print("Updated successfully!")    
               
    def delete(self, table_id):
        with Session(engine) as session:
            statement = session.get(self.table_name, table_id)
            if statement is not None:
                session.delete(statement)
                session.commit()
                print("Deleted successfully!")
            else:
                print(f"This ID doesn't exist for {self.table_name}")
                
user_crud = BaseCRUD(User)
animal_crud = BaseCRUD(Animal)         
@app.post("/users/create/")
async def create_user(kwargs:User):
    with Session(engine) as session:
        user = user_crud.create(session, **kwargs)
        return user

@app.get("/users/read/{user_id}")
def read_user(user_id: int):
    with Session(engine) as session:
        user = user_crud.read(session, user_id)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/update/{user_id}")
def update_user(user_id: int, **kwargs):
    with Session(engine) as session:
        user = user_crud.update(session, user_id, **kwargs)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/delete/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = user_crud.delete(session, user_id)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")       
# @app.post("/users/create/")
# def create_user(name: str, email: str):
#     with Session(engine) as session:
#         user = user_crud.create(session, name=name, email=email)
#         return user

# @app.get("/users/read/{user_id}")
# def read_user(user_id: int):
#     with Session(engine) as session:
#         user = user_crud.read(session, user_id)
#         if user:
#             return user
#         else:
#             raise HTTPException(status_code=404, detail="User not found")

# @app.put("/users/update/{user_id}")
# def update_user(user_id: int, name: str, email: str):
#     with Session(engine) as session:
#         user = user_crud.update(session, user_id, name=name, email=email)
#         if user:
#             return user
#         else:
#             raise HTTPException(status_code=404, detail="User not found")

# @app.delete("/users/delete/{user_id}")
# def delete_user(user_id: int):
#     with Session(engine) as session:
#         user = user_crud.delete(session, user_id)
#         if user:
#             return user
#         else:
#             raise HTTPException(status_code=404, detail="User not found")

# # def main():
# #     user_crud = BaseCRUD(User)
# #     animal_crud = BaseCRUD(Animal)

# #     # user_crud.create(name="Johny", email="abc@gmail.com")
# #     # user_crud.delete(table_id=3)
# #     # user_crud.update(table_id=1, name="ony", email="ahmad@gmail.com")
# #     # user_crud.read(table_id=2)
# #     # animal_crud.create(name="thieses", age=5, type="Dog", species="Labrador")

# # if __name__ == "__main__":
# #     main()


# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
@app.post("/users/create/")
def create_user(**kwargs):
    with Session(engine) as session:
        user = user_crud.create(session, **kwargs)
        return user

@app.get("/users/read/{user_id}")
def read_user(user_id: int):
    with Session(engine) as session:
        user = user_crud.read(session, user_id)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/update/{user_id}")
def update_user(user_id: int, **kwargs):
    with Session(engine) as session:
        user = user_crud.update(session, user_id, **kwargs)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/delete/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = user_crud.delete(session, user_id)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
        
        
#animal apis

@app.post("/animals/create/")
def create_animal(name: str = None, age: int = None, type: str = None, species: str = None):
    with Session(engine) as session:
        animal_crud.create(session, name=name, age=age, type=type, species=species)
        return {"name": name, "age": age, "type": type, "species": species}

@app.get("/animals/read/{animal_id}")
def read_animal(animal_id: int):
    with Session(engine) as session:
        animal = animal_crud.read(session, animal_id)
        if animal:
            return animal
        else:
            raise HTTPException(status_code=404, detail="Animal not found")

@app.put("/animals/update/{animal_id}")
def update_animal(animal_id: int, **kwargs):
    with Session(engine) as session:
        animal = animal_crud.update(session, animal_id, **kwargs)
        if animal:
            return animal
        else:
            raise HTTPException(status_code=404, detail="Animal not found")

@app.delete("/animals/delete/{animal_id}")
def delete_animal(animal_id: int):
    with Session(engine) as session:
        animal = animal_crud.delete(session, animal_id)
        if animal:
            return animal
        else:
            raise HTTPException(status_code=404, detail="Animal not found")
        
        
        
# @app.post("/animals/create/")
# def create_animal(name: str = None, age: int = None, type: str = None, species: str = None):
#     with Session(engine) as session:
#         animal_crud.create(session, name=name, age=age, type=type, species=species)
#         return {"name": name, "age": age, "type": type, "species": species}
        