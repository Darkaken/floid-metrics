Floid Metrics Update Log

---------------------------------------------

v.1.0

Route Changes:
  
  1. New route:
  
        URL: /get_income
        Method: POST
        HTTP HEADER (expected input): Floid Report JSON Object (structure as per JAN 2022)
        Expected Output: Floid Report JSON Object (structure as per JAN 2022)
        
        Expected Changes:
        
          report["income"]["income_test_data"] : 
          
            {
                "high_confidence_income": int,
                "ife_income": int,
                "low_confidence_income": int,
                "no_confidence_income": int
            }

v.1.1

  1. Route Update:

        URL: /get_income
        HTTP HEADER (expected input):
        Floid Report JSON Object (structure as per JAN 2022) AND:

            report["parametros"]: {

                "monto_minimo_tranzado": int,
                "not_income_words": list,
                "high_income_words": list,
                "medium_income_words": list,
                "rut_minimo": int,
                "consecutividad", int,
                "consecutividad_ingresos": int,
                "ultimo_mes_a_considerar": int
            }

        Expected Output: Floid Report JSON Object (structure as per JAN 2022)

        Expected Changes:

            report["income"]["income_test_data"]: {

                "has_income": bool,
                "monthly_high_confidence_income": int,
                "monthly_medium_confidence_income": int,
                "monthly_no_confidence_income": int
            }

  2. Route Enhancements:

        1. Basic Error Handling
        2. Unhandled Error Logging for future review and development (API 1.2 or 1.3)
        3. Proyect structure update

v1.2 Experimental

    1. New Route

        URL: /get_income_santander
        Method: POST
        HTTP HEADER (expected input): Floid Report JSON Object (structure as per JAN 2022)
        Expected Output: Floid Report JSON Object (structure as per JAN 2022) AND:

             report["parametros"]: {

                 "monto_minimo_tranzado": int,
                 "high_income_words": list,
                 "medium_income_words": list,
                 "ventana_high_income": int,
                 "ventana_medium_income": int

            }

        Expected Changes:

            report["income"]["income_test_data"] : {

                "high_income_analysis_income" : int,
                "high_income_analysis_client_status" : bool,
                "medium_income_analysis_income" : int,
                "medium_income_analysis_client_status" : bool
            }