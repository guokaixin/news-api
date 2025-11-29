from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from src.config.database import get_db
from src.crud.news import get_news_list, get_news_detail
from src.schemas.news import NewsListResponse, NewsResponse

router = APIRouter(prefix="/api/v1", tags=["新闻接口"])

@router.get("/news", response_model=NewsListResponse, summary="获取新闻列表")
def list_news(
    keyword: Optional[str] = Query(None, description="标题/描述过滤关键词"),
    page: Optional[int] = Query(None, ge=1, description="页码"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="每页条数"),
    offset: Optional[int] = Query(None, ge=0, description="偏移量"),
    db: Session = Depends(get_db)
):
    """
    新闻列表接口
    """
    total, news_list = get_news_list(
        db=db,
        keyword=keyword,
        page=page,
        limit=limit,
        offset=offset
    )
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "offset": offset,
        "data": news_list
    }

@router.get("/news/{news_id}", response_model=NewsResponse, summary="获取新闻详情")
def detail_news(
    news_id: int,
    db: Session = Depends(get_db)
):
    """
    新闻详情接口
    """
    news = get_news_detail(db=db, news_id=news_id)
    if not news:
        raise HTTPException(status_code=404, detail=f"新闻 ID {news_id} 不存在")
    return news