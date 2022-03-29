## FLOID METRICS

#INCOME:

    https://floid-metrics.herokuapp.com/get_income

    Funcionalidad:

    Utilizando el método POST y usando como input un reporte de transacciones (reporte normal de Floid, en formato JSON) esta ruta calcula las siguientes cosas:

    1) Income de alta confianza -> tiene palabras que explicitan que es un ingreso
    2) Income de media confianza -> tiene palabras que dan a entender que es un ingreso pero no es seguro (en la mayoría de los casos si lo es)
                                -> tiene descripciones que se repiten al menos N meses seguidos (recurrencia)
    3) Income de nula confianza -> directamente se sabe que no es ingreso o no sabemos si es un ingreso o no
    4) Si es que la persona se considera "con ingreso -> Si es que tiene ingresos por X meses seguidos partiendo por el ultimo o penultimo mes

    Retorna el mismo objeto de JSON de input con un campo adicional en reporte["income"]["income_test_data"]. El detalle de esto se puede ver en el log de cambios (otro documento de texto en este repo)



#Income Santander:
    https://floid-metrics.herokuapp.com/get_income_santander
    
    Utilizando el metodo POST y como input un reporte de FLOID en formato JSON, se calculan las siguientes cosas:
    
    1) Income de alta confianza
    2) Si el cliente es valido o no segun el analisis de high income
    
    3) Income de media confianza
    4) Si el cliente es valido o no segun el analisis de medium income