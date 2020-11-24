# -*- coding: utf-8 -*-
"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Validadores de identificacion y otros

.. moduleauthor:: dgonzalez.jim@gmail.com

"""

NUM_PROVINCIAS = 24
SOCIEDAD_PRIVADA = 9
SIZE_CEDULA = 10
SIZE_RUC = 13

class ValidadorDocumento(object):
    """

    Clase validadora de Identificacion

    """
    
    def validar_cedula_leng(self, cedula):
         if cedula is None or len(cedula) == SIZE_CEDULA or len(cedula) == SIZE_RUC:
            return True
         else:
            return False

    def validar_ruc_leng(self, ruc):
         if ruc is None or len(ruc) == SIZE_RUC or len(ruc) == SIZE_CEDULA:
            return True
         else:
            return False    
        
    def validar_cedula_leng_destinatario(self, cedula):
         if cedula is None or len(cedula) == SIZE_CEDULA :
            return True
         else:
            return False

    def validar_ruc_leng_destinatario(self, ruc):
         if ruc is None or len(ruc) == SIZE_RUC :
            return True
         else:
            return False

    def validar_cedula(self, cedula):
        if cedula is None or len(cedula) != SIZE_CEDULA:
            return False
        
        prov = int(cedula[:2])
        if prov < 0 or prov >= NUM_PROVINCIAS:
            return False

        d = []
        for c in cedula:
            d.append( int(c) )
            
        par, impar = 0, 0

        for i in range(0, len(d)-1):
            if i % 2:
                par += d[i]
            else:
                m = d[i] * 2
                if m > 9:
                    d[i] = m - 9
                else:
                    d[i] = m
                impar += d[i]

        suma = par + impar
        
        d10 = int( str(suma + 10)[0] + "0" ) - suma 
        
        if d10 == 10:
            d10 = 0

        return d10 == d[9]

    def validar_ruc(self, ruc):
        if ruc is None or len(ruc) != SIZE_RUC:
            return False

        if self.validar_cedula(ruc[:SIZE_CEDULA]):
            return True
        
        prov = int(ruc[:2])
        if prov < 0 or prov >= NUM_PROVINCIAS:
            return False
        
        d = []
        for c in ruc:
            d.append( int(c) )

        suma = self.suma_factores(d[2], d)
        factor = suma % 11
        factor = 11 - factor
        
        if d[2] == SOCIEDAD_PRIVADA:
            digito_verificador = d[9]
        else:
            digito_verificador = d[8]

        return factor == digito_verificador
    
    def suma_factores(self, tipo, d):        
        if tipo == SOCIEDAD_PRIVADA:
            secuencia = [4, 3, 2, 7, 6, 5, 4, 3, 2]
        else:
            secuencia = [3, 2, 7, 6, 5, 4, 3, 2]
            
        i, suma = 0, 0
        for s in secuencia:
            subtotal = s * d[i]
            suma += subtotal
            i += 1

        return suma
    
doc_validator = ValidadorDocumento()
