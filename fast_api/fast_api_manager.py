import json
from dataclasses import dataclass
from fastapi import FastAPI
from fastapi.responses import Response
from bson import ObjectId, json_util
import uvicorn
from pydantic import BaseModel
from database import mongo_user_wrapper
from data.user import User

app = FastAPI(debug=True)


@dataclass
class GivenUser(BaseModel):
    first_name: str
    last_name: str


@app.post("/users")
def create_user(user: GivenUser) -> Response:
    created_user = User(**user.dict())
    new_user = mongo_user_wrapper.create(created_user)
    return Response(content=new_user.to_json())


@app.get("/users/{user_id}")
def get_user(user_id: str) -> Response:
    object_id = ObjectId(user_id)
    user = mongo_user_wrapper.get(object_id)
    return Response(content=user.to_json())


@app.put("/users/{user_id}")
def update_user(user: GivenUser, user_id: str) -> Response:
    object_id = ObjectId(user_id)
    created_user = User(**user.dict())
    created_user.uid = object_id
    update_res = mongo_user_wrapper.update(created_user)
    res_json = {"update_status": update_res.acknowledged, "updated_user": created_user.get_doc()}
    return Response(content=json.dumps(res_json, default=json_util.default))


@app.delete("/users/{user_id}")
def remove_user(user_id: str) -> Response:
    object_id = ObjectId(user_id)
    user_to_remove = mongo_user_wrapper.get(object_id)
    remove_res = mongo_user_wrapper.remove(object_id)
    res_json = {"remove_status": remove_res.acknowledged, "removed_user": user_to_remove.get_doc()}
    return Response(content=json.dumps(res_json, default=json_util.default))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port="8000")
