from fastapi import FastAPI
from Models.models import FileInfo
from utils import stage_files, get_fileattributes, process_and_insert
from mongo import insert_data, get_top_10_recently_updated, collection
from Schema.schemas import list_serial, individual_serializer
import json
from typing import List



app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is the root of your endpoint."}



@app.post("/processfiles/")
async def process_files() -> str:
    files = await stage_files()
    rules = []
    if files:
        for file in files:
            fileinfo = await get_fileattributes(file)
            rules.append(fileinfo)
            # return rules
        await process_and_insert(rules)
        return (f"{len(rules)} files have been processed successfully.")
        # return("The following Rules have been processed successfully:\n " + str(rules))
    return ("There are currently no staged files to process.")

@app.get("/getrecentfiles/")
async def get_files():
    data = await get_top_10_recently_updated()
    return data

@app.post("/insertdata/")
async def insert(fileData: List[FileInfo]):
    for file in fileData:
        data = file.model_dump()
        await insert_data(data)
    return print("Data inserted successfully into the database.")


@app.get("/getdata/")
async def get_data():
    FileParams = list_serial(collection.find())
    return FileParams