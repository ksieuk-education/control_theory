import pydantic


class FirstLabModel(pydantic.BaseModel):
    k: float = pydantic.Field(default=1, description="Коэффициент усиления k")
    t: float = pydantic.Field(default=1, description="Постоянная времени t")
    xi: float = pydantic.Field(default=0.5, description="xi")

    @pydantic.field_validator(
        "k",
        "t",
        "xi",
    )
    @classmethod
    def check_limits(cls, value: float) -> float:
        assert 0 <= value <= 1, ValueError("Значение не может быть меньше 0")
        return value
