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

