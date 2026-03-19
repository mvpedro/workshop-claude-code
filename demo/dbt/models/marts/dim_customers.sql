with customer_orders as (
    select * from {{ ref('int_customer_orders') }}
)
select
    customer_id,
    customer_name,
    email,
    segment,
    is_active,
    signup_date,
    order_count,
    total_spent_cents,
    total_spent_reais,
    first_order_date,
    last_order_date,
    case
        when total_spent_cents >= 100000 then 'gold'
        when total_spent_cents >= 50000 then 'silver'
        else 'bronze'
    end as calculated_segment
from customer_orders
