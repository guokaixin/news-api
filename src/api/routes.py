from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from src.config.database import get_db
from src.models.news import News
from src.schemas.news import NewsListNonRESTResponse, NewsDetailNonRESTResponse

router_non_rest = APIRouter(tags=["新闻接口"])

@router_non_rest.get("/get_news_list", response_model=NewsListNonRESTResponse, summary="获取新闻列表")
def get_news_list_non_rest(
    keyword: Optional[str] = Query(None, description="标题/描述过滤关键词"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(10, ge=1, le=50, description="每页条数"),
    offset: Optional[int] = Query(None, ge=0, description="偏移量"),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(News)
        
        if keyword:
            query = query.filter(
                or_(
                    News.title.like(f"%{keyword}%"),
                    News.description.like(f"%{keyword}%")
                )
            )
        
        query = query.order_by(News.created_at.desc())
        
        total_count = query.count()
        
        if offset is not None:
            query = query.offset(offset).limit(limit)
            current_page = None
            skip_count = offset
        else:
            offset_calc = (page - 1) * limit
            query = query.offset(offset_calc).limit(limit)
            current_page = page
            skip_count = offset_calc
        
        news_list = query.all()
        news_list_serialized = [news.to_dict() for news in news_list]

        return {
            "code": 200,
            "msg": "获取新闻列表成功",
            "data": {
                "total_count": total_count,
                "current_page": current_page,
                "page_size": limit,
                "skip_count": skip_count,
                "news_list": news_list_serialized
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=200,
            detail={
                "code": 500,
                "msg": f"获取新闻列表失败：{str(e)}",
                "data": {}
            }
        )

@router_non_rest.get("/get_news_detail", response_model=NewsDetailNonRESTResponse, summary="获取新闻详情")
def get_news_detail_non_rest(
    news_id: int = Query(..., description="新闻ID，必填"),
    db: Session = Depends(get_db)
):
    try:
        news = db.query(News).filter(News.id == news_id).first()
        
        if not news:
            return {
                "code": 404,
                "msg": f"新闻ID {news_id} 不存在",
                "data": None
            }
        
        return {
            "code": 200,
            "msg": "获取新闻详情成功",
            "data": news
        }
    except Exception as e:
        raise HTTPException(
            status_code=200,
            detail={
                "code": 500,
                "msg": f"获取新闻详情失败：{str(e)}",
                "data": None
            }
        )