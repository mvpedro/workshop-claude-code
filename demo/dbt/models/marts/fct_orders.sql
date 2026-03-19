with orders as (
    select * from {{ ref('stg_orders') }}
),
customers as (
    select * from {{ ref('int_customer_orders') }}
),
order_items as (
    select
        oi.pedido_id as order_id,
        oi.produto_id as product_id,
        oi.quantidade as quantity,
        oi.preco_unitario_centavos as unit_price_cents
    from {{ source('raw', 'raw_order_items') }} oi
),
product_perf as (
    select * from {{ ref('int_product_performance') }}
)
select
    o.order_id,
    o.customer_id,
    c.customer_name,
    c.segment as customer_segment,
    o.status,
    o.total_cents,
    o.total_reais,
    o.order_date,
    o.notes,
    c.order_count as customer_total_orders,
    c.total_spent_reais as customer_ltv_reais,
    count(oi.product_id) as item_count
from orders o
left join customers c on o.customer_id = c.customer_id
left join order_items oi on o.order_id = oi.order_id
group by
    o.order_id, o.customer_id, c.customer_name, c.segment,
    o.status, o.total_cents, o.total_reais, o.order_date, o.notes,
    c.order_count, c.total_spent_reais
