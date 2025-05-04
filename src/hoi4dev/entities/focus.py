from pydantic import BaseModel, Field

class NationalFocus(BaseModel):
    id: int = Field(..., description="The ID of the focus. Usually in the format of `<TREE>.<ID>`, where `<TREE>` is the tree name and `<ID>` is a positive integer.")
    px: int = Field(default=None, description="The absolute x coordinate of the focus.")
    py: int = Field(default=None, description="The absolute y coordinate of the focus.")
    pw: int = Field(default=None, description="The width of the subtree of the focus.")
    name: str = Field(..., description="The name of the focus.")
    icon: str = Field(..., description="The filepath to the icon of the focus.")
    scale: float = Field(default=1.0, description="The scale of the focus icon.")
    parent: str = Field(default=None, description="The ID of the parent focus (used for focus positioning only).")
    priority: int = Field(default=0, description="The priority of the focus. Higher values are processed first.")
    dx: int = Field(default=0, description="The x offset of the focus relative to its auto-positioned coordinate.")
    dy: int = Field(default=0, description="The y offset of the focus relative to its auto-positioned coordinate.")
    dw: int = Field(default=None, description="The extra width of the focus subtree.")
    dc: int = Field(default=None, description="The x offset of all its children relative to this focus.")
    path: str = Field(default=None, description="The filepath to the focus folder.")