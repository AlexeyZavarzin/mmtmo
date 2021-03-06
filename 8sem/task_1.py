from math import factorial, exp


def get_r(_alpha, _beta):
    eps = .00000001
    _r = 1
    while ((_alpha / _beta) ** _r / factorial(_r - 1)) * exp(_alpha / _beta) > eps:
        _r += 1
    return _r


def product(_k, _s, _beta):
    prod = 1
    for m in range(1, _s + 1):
        prod *= (_k + m * _beta)
    return prod


def get_p_0(_k, _alpha, _beta, _r):
    res_1 = sum([_alpha ** n / factorial(n) for n in range(0, _k + 1)])
    res_2 = _alpha ** _k / factorial(_k)
    res_3 = sum([_alpha ** s / product(_k, s, _beta) for s in range(1, _r + 1)])
    res = 1 / (res_1 + res_2 * res_3)
    return res


def get_p_n(_n, _alpha, _p_0):
    return (_alpha ** _n / factorial(_n)) * _p_0


def get_p_ks(_k, _s, _alpha, _beta, _p_0):
    res = (_alpha ** (_k + _s)) / (factorial(_k) * product(_k, _s, _beta))
    return res * _p_0


if __name__ == '__main__':
    lambda_ = 2
    mu = .5
    v = 1 / 3

    k = 3

    alpha = lambda_ / mu
    beta = v / mu

    r = get_r(alpha, beta)

    # а) долю времени, когда все ЭВМ свободны от проведения расчетов
    p_0 = get_p_0(k, alpha, beta, r)
    print("Доля времени, когда все ЭВМ свободны от проведения расчетов:", p_0)

    # б) долю времени, когда одна из ЭВМ будет занята расчетом, а другие свободны
    n = 1
    p_n = get_p_n(n, alpha, p_0)
    print("Доля времени, когда одна из ЭВМ будет занята расчетом, а другие свободны:", p_n)

    # в) вероятность того, что все ЭВМ будут работать одновременно, и не поступило новых данных для проведения расчетов
    p_k = get_p_n(k, alpha, p_0)
    print("Вероятность того, что все ЭВМ будут работать одновременно, "
          "и не поступило новых данных для проведения расчетов:", p_k)

    # г) вероятность отказа поступившим заказам на проведение метеорологических расчетов
    b = sum([s * get_p_ks(k, s, alpha, beta, p_0) for s in range(1, r + 1)])
    p_otk = b * (beta / alpha)
    print("Вероятность отказа поступившим заказам на проведение метеорологических расчетов:", p_otk)

    # д) среднее число заказов, находящихся в вычислительном центре и ожидающих проведения метеорологических расчетов
    h = sum([n * get_p_n(n, alpha, p_0) for n in range(1, k + 1)]) + \
        k * sum([get_p_ks(k, s, alpha, beta, p_0) for s in range(1, r + 1)])
    print("Среднее число заказов, ожидающих проведения метеорологических расчетов:", b)
    print("Среднее число заказов, находящихся в вычислительном центре:", b + h)

    # е) долю ЭВМ, простаивающих в вычислительном центре
    g = k - h
    k_g = g / k
    print("Доля ЭВМ, простаивающих в вычислительном центре:", k_g)

    # Определить число ЭВМ, необходимое,
    # чтобы вероятность отказа поступившим заказам на проведение метеорологических расчетов не превышала 0,1
    required_prob = .1
    while p_otk >= required_prob:
        k += 1
        p_0 = get_p_0(k, alpha, beta, r)
        b = sum([s * get_p_ks(k, s, alpha, beta, p_0) for s in range(1, r + 1)])
        p_otk = b * (beta / alpha)
        print(f"---вероятность отказа равна {p_otk} при {k} ЭВМ")

    print("Чтобы вероятность отказа поступившим заказам на проведение метеорологических расчетов не превышала 0,1, "
          f"необходимо {k} ЭВМ.")
