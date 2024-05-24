from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import String, and_, inspect, or_
from sqlalchemy.orm import Session


from models.data import Data
from view_model.data_vm import DataCreateVM, DataFilterVM 
from typing import List



def create_data( db: Session, data:DataCreateVM):
        db_data = Data( 
                        image_url = data.image_url,
                        title = data.title,
                        article_url = data.article_url,
                        highlight = data.highlight,
                        time_publish = data.time_publish,
                        category = data.category,
                        date_published = data.date_published,
                        publisher_name = data.publisher_name,
                        detail_content = data.detail_content
    )
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data

def get_data (db: Session):
        return  db.query(Data)
def search_data(db: Session, query: str):
    search_term = f"%{query}%"
    columns = [column.name for column in inspect(Data).columns]
    filters = []
    for column in columns:
        col_attr = getattr(Data, column)
        
        if isinstance(col_attr.type, String):
            filters.append(col_attr.like(search_term))
   
    results = db.query(Data).filter(or_(*filters)).all()
    return results

def filter_data(db: Session, query_params: dict):
    filters = []
    for column_name, value in query_params.items():
        column = getattr(Data, column_name, None)
        if value is not None and column is not None:
            filters.append(column == value)
    
    print("filters:", filters)
    
    # Apply the filters with AND logic to the query
    results = db.query(Data).filter(and_(*filters)).all()
    
    print("results:", results)
    return results