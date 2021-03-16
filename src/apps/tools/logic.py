from pydantic import validate_arguments


@validate_arguments
def calculate_pert(p: float, o: float, m: float) -> tuple:
    """
    Формула расчета: EAD = (P + 4M + O) / 6
    P - «пессимистичная оценка»
    O - «оптимистичная оценка»
    M - «наиболее вероятная оценка»
    SD - отклонение (P - O) / 6
    RANGE - EAD -+ SD
    """
    ead_val = (p + 4 * o + m) / 6
    sd = (p - o) / 6

    return ead_val, sd, ead_val-sd, ead_val+sd
