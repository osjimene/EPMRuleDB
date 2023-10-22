import streamlit as st
import requests
from typing import List
from Models.models import FileInfo
import json
import os
import pandas as pd


def process_files():
    response = requests.post("http://localhost:8000/processfiles/")
    if response.status_code == 200:
        return response.json()
    else:
        return "There are currently no staged files to process."


def get_recent_files():
    response = requests.get("http://localhost:8000/getrecentfiles/")
    if response.status_code == 200:
        return response.json()
    else:
        return "Unable to retrieve recent files."


def insert_data(fileData: List[FileInfo]):
    response = requests.post("http://localhost:8000/insertdata/", json=fileData)
    if response.status_code == 200:
        return "Data inserted successfully into the database."
    else:
        return "Unable to insert data."


def get_data():
    response = requests.get("http://localhost:8000/getdata/")
    if response.status_code == 200:
        return response.json()
    else:
        return "Unable to retrieve data."


def main():
    st.title("EPM Rule Analyzer")

    menu = ["Upload Files", "Data Analysis", "Rule Creator"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Upload Files":
        st.header("Upload Files")
        fileData = st.file_uploader("Choose Files to Upload",type="exe", accept_multiple_files=True)
        #if os.path.join(os.getcwd(), 'Tmp') does not exist, create it
        if not os.path.exists(os.path.join(os.getcwd(), 'Tmp')):
            os.makedirs(os.path.join(os.getcwd(), 'Tmp'))
        if fileData is not None:
            for file in fileData:
                with open(os.path.join(os.getcwd(), 'Tmp', file.name), "wb") as buffer:
                    buffer.write(file.read())          
            if st.button("Process Files"):
                result = process_files()
                st.write(result)

    elif choice == "Data Analysis":
        st.header("Data Analysis")
        # st.write(get_data())
        data = get_data()
        df = pd.json_normalize(data)
        #drop the id and FilePath columns
        df = df.drop(columns=['id', 'FilePath'])
        #Filter any duplicate hashes
        df = df.drop_duplicates(subset=['FileHash'])
        #explode the certificates column
        df = df.explode('Certificates')
        st.write(df)
    
    elif choice == "Rule Creator":
        st.header("Rule Creator (In Testing)")
        #Present the user with a dropdown menu of Filenames
        data = get_data()
        df = pd.json_normalize(data)
        df = df.drop(columns=['id', 'FilePath'])
        #Filter any duplicate hashes
        df = df.drop_duplicates(subset=['FileHash'])
        filenames = df['FileName'].tolist()
        filenames.insert(0, "Select a Filename")
        filename = st.selectbox("Select a Filename", filenames)
        if filename is not "Select a Filename":
            #using the selected filename, filter the dataframe to only show the selected filename
            df = df[df['FileName'] == filename]
            #give me a widget that would let the user select multiple columns of the metadata
            columns = df.columns.tolist()
            columns.insert(0, "Select a Column")
            column = st.multiselect("Select Columns", columns)
            #Based on the selected columns, return the values for these columns in json format, return the full object with the nonselected items as null
            if column:
                df = df[column]
                st.write(df)


        

if __name__ == "__main__":
    main()