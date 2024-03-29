import pydantic


class FirstLabModel(pydantic.BaseModel):
    k: float = pydantic.Field(default=1, description="Коэффициент усиления k")
    t: float = pydantic.Field(default=1, description="Постоянная времени t")
    xi: float = pydantic.Field(default=0.5, description="Коэффициент демпфирования xi")

    @pydantic.field_validator("xi")
    @classmethod
    def check_limits_xi(cls, value: float) -> float:
        assert 0 <= value <= 1, ValueError("Значение не может быть меньше 0")
        return value

    @pydantic.field_validator(
        "t",
        "k"
    )
    @classmethod
    def check_limits(cls, value: float) -> float:
        assert 0 <= value, ValueError("Значение не может быть меньше 0")
        return value
