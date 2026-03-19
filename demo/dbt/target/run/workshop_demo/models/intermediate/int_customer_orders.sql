
  
  create view "workshop_demo"."main"."int_customer_orders__dbt_tmp" as (
    with customers as (
    select * from "workshop_demo"."main"."stg_customers"
),
orders as (
    select * from "workshop_demo"."main"."stg_orders"
    where status != 'cancelled'
)
select
    c.customer_id,
    c.customer_name,
    c.email,
    c.segment,
    c.is_active,
    c.signup_date,
    count(o.order_id) as order_count,
    coalesce(sum(o.total_cents), 0) as total_spent_cents,
    
    round(cast(coalesce(sum(o.total_cents), 0) as float) / 100, 2)
 as total_spent_reais,
    min(o.order_date) as first_order_date,
    max(o.order_date) as last_order_date
from customers c
left join orders o on c.customer_id = o.customer_id
group by c.customer_id, c.customer_name, c.email, c.segment, c.is_active, c.signup_date
  );
