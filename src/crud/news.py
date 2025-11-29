from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.models.news import News
from typing import Optional

def get_news_list(
    db: Session,
    keyword: Optional[str] = None,
    page: Optional[int] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None
) -> tuple[int, list[News]]:
    query = db.query(News)
    
    if keyword:
        query = query.filter(
            or_(
                News.title.like(f"%{keyword}%"),
                News.description.like(f"%{keyword}%")
            )
        )
    
    query = query.order_by(News.created_at.desc())
    
    total = query.count()
    
    if page is not None and page < 1:
        page = 1
    if limit is not None:
        limit = max(1, min(limit, 100))
    if offset is not None and offset < 0:
        offset = 0
    
    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)
    elif page is not None and limit is not None:
        offset_calc = (page - 1) * limit
        query = query.offset(offset_calc).limit(limit)
    elif limit is not None:
        query = query.limit(limit)
    elif offset is not None:
        query = query.offset(offset)
    
    news_list = query.all()
    return total, news_list

def get_news_detail(db: Session, news_id: int) -> Optional[News]:
    return db.query(News).filter(News.id == news_id).first()