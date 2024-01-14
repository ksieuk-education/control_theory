import typing

import lib.methods.first_lab as methods_first_lab

LAB_1_METHODS: dict[str, typing.Any] = {
    "Первая часть": (methods_first_lab.FirstLabModel, methods_first_lab.laba1_calculate),
    "Вторая часть": (methods_first_lab.FirstLabModel, methods_first_lab.laba1_2_calculate),
}

LAB_1_GRAPHS_1 = {
    "Пропорциональное (усилительное) звено w1": 1,
    "Интегрирующее звено (интегратора) w2": 2,
    "Апериодического звено первого порядка w3": 3,
    "Передаточная функция идеального дифференцирующего звена w4": 4,
    "Передаточная функция колебательного звена w5": 5,
}
LAB_1_GRAPHS_2 = {
    "Увеличение коэффициента усиления вдвое": 1,
    "Увеличение коэффициента вдвое": 2,
    "Уменьшение коэффициента в два раза": 3,
    "Коэффициент демпфирования ξ = 0": 4,
    "Коэффициент демпфирования ξ = 1": 5,
}

FIELD_DEFAULT_TYPE = str | int | float | None
