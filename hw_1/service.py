import random
import string as st
import currency as c, planets as pl

class Service:

    all_symbols = st.ascii_letters + st.digits
    exchange_rates = c.exchange_rates
    planets = pl.planets



    @classmethod
    def generates_a_password(cls, length) -> str:
        """
        Генерирует случайный пароль
        :param length: длинна int
        :return: str
        """
        result = ''
        for elem in range(0, int(length), 1):
            result += random.choice(cls.all_symbols)
        return result


    @classmethod
    def calculates_force_of_attraction(cls, name_planet, height) :
        """
        Вычисляет силу притяжения там согласно закону всемирного тяготения
        :param name_planet: название планеты
        :param height: высота над ее поверхностью
        :return: str, float
        """
        g = 6.674e-11

        if name_planet not in cls.planets:
            return False

        planet = cls.planets[name_planet]
        mass_planet = planet['mass']
        radius_planet = planet['radius']

        # Вычисляем ускорение свободного падения
        r = radius_planet + float(height)  # Расстояние от центра планеты
        gravity_m_s2 = g * mass_planet / r ** 2 # Сила притяжения

        return {"gravity_m_s2": gravity_m_s2}


    @classmethod
    def calculates_speeding_fine(cls, speed, limit):
        """
        Вычисляет размер штрафа исходя из принятых параметров
        :param speed: текущая скорость
        :param limit: разрешенная скорость
        :return: str, int
        """
        result = float(speed) - float(limit)

        if result < 10:
            return f'При скорости {speed} нет штрафа.'

        elif 10 <= result < 20:
            return f'При скорости {speed} штраф 500 рублей.'

        elif 20 <= result < 40:
            return 'штраф 1500 рублей.'

        elif result >= 40:
            return f'При скорости {speed} штраф {50 * result} рублей.'


    @classmethod
    def calculates_exchange_rates(cls, from_currency, to_currency, amount, commission_rate):
        """
        Вычисляет по заданным валютам и их параметрам итоговую сумму курса валют
        :param from_currency: валюта
        :param to_currency: валюта
        :param amount: количество float
        :param commission_rate: размер комиссии float
        :return: str, float
        """
        conversion_rate = cls.exchange_rates[from_currency][to_currency]
        converted_amount = float(amount) * conversion_rate

        commission = converted_amount * float(commission_rate)
        final_amount = converted_amount - commission

        return {"amount": round(final_amount, 2)}