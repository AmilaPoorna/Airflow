create or replace table AIRFLOW.L1_LANDING.profit_uk 
as ( 
  SELECT 
    sales_date, SUM(quantity_sold * unit_sell_price) as total_revenue,
    SUM(quantity_sold * unit_purchase_cost) as total_cost,
    SUM(quantity_sold * unit_sell_price) - SUM(quantity_sold * unit_purchase_cost) as total_profit
  FROM 
    AIRFLOW.L1_LANDING.sales_uk
  WHERE
    sales_date BETWEEN '{{ var.json.process_interval.start_date }}' AND '{{ var.json.process_interval.end_date }}'
  GROUP BY 
    sales_date
)