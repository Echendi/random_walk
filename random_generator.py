class CongruencialLineal:
    def __init__(self, a, c, m, seed):
        """
        Constructor de la clase CongruencialLineal.

        Args:
            a (int): Factor multiplicativo.
            c (int): Término aditivo.
            m (int): Módulo.
            seed (int): Semilla inicial.
        """
        self.a = a
        self.c = c
        self.m = m
        self.xn = seed

    def generate_xn(self):
        """
        Genera el próximo valor de la secuencia congruencial.

        Returns:
            int: Próximo valor en la secuencia.
        """
        self.xn = (self.a * self.xn + self.c) % self.m
        return self.xn

    def generate_number(self):
        """
        Genera un número pseudoaleatorio en el rango [0, 1).

        Returns:
            float: Número pseudoaleatorio.
        """
        return self.generate_xn() / (self.m - 1)
