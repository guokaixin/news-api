from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NewsBase(BaseModel):
    title: str = Field(..., max_length=255, description="新闻标题")
    description: str = Field(..., description="新闻描述")
    content: str = Field(..., description="新闻正文")

class NewsResponse(NewsBase):
    id: int = Field(..., description="新闻ID")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        orm_mode = True

class NewsListNonRESTResponse(BaseModel):
    code: int = Field(200, description="响应码，200 成功，其他失败")
    msg: str = Field("success", description="响应信息，成功或失败")
    data: dict = Field(..., description="数据体，包含分页+新闻列表")

class NewsDetailNonRESTResponse(BaseModel):
    code: int = Field(200, description="响应码")
    msg: str = Field("success", description="响应信息")
    data: Optional[NewsResponse] = Field(None, description="新闻详情数据")