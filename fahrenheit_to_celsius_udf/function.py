# app/main.py

# def main(session):
#     from snowflake.snowpark.functions import col

#     # Create DataFrame with Celsius values
#     df = session.create_dataframe([[0], [20], [30]], schema=["celsius"])

#     # Convert to Fahrenheit
#     df = df.with_column("fahrenheit", (col("celsius") * 9 / 5) + 32)

#     return df

# fahrenheit_to_celsius_udf/function.py

def main(temp_f: float) -> float:
    return (temp_f - 32) * 5.0 / 9.0