from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class NewsBase(BaseModel):
    title: str = Field(..., max_length=255, description="新闻标题")
    description: str = Field(..., description="新闻描述")
    content: str = Field(..., description="新闻正文")

class NewsResponse(NewsBase):
    id: int = Field(..., description="新闻ID")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True

class NewsListResponse(BaseModel):
    total: int = Field(..., description="符合条件的总条数")
    page: Optional[int] = Field(None, description="当前页码")
    limit: Optional[int] = Field(None, description="每页条数")
    offset: Optional[int] = Field(None, description="偏移量")
    data: List[NewsResponse] = Field(..., description="新闻列表数据")