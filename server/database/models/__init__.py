import pydantic


class BaseModel(pydantic.BaseModel):
    def dict(self, *args, **kwargs):
        exclude = set()
        for name, field in self.__fields__.items():
            if not field.field_info.extra.get("export", True):
                exclude.add(name)

        kwargs["exclude"] = (kwargs["exclude"] if kwargs.get("exclude") else set()) | exclude
        return super().dict(*args, **kwargs)

    class Config:
        arbitrary_types_allowed = True
