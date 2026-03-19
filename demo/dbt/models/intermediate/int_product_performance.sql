with products as (
    select * from {{ ref('stg_products') }}
),
order_items as (
    select
        oi.produto_id as product_id,
        oi.quantidade as quantity,
        oi.preco_unitario_centavos as unit_price_cents,
        o.order_id,
        o.status
    from {{ source('raw', 'raw_order_items') }} oi
    inner join {{ ref('stg_orders') }} o on oi.pedido_id = o.order_id
    where o.status != 'cancelled'
)
select
    p.product_id,
    p.product_name,
    p.category,
    p.price_cents,
    p.stock,
    count(distinct oi.order_id) as times_ordered,
    coalesce(sum(oi.quantity), 0) as total_units_sold,
    coalesce(sum(oi.quantity * oi.unit_price_cents), 0) as total_revenue_cents,
    {{ cents_to_reais('coalesce(sum(oi.quantity * oi.unit_price_cents), 0)') }} as total_revenue_reais
from products p
left join order_items oi on p.product_id = oi.product_id
group by p.product_id, p.product_name, p.category, p.price_cents, p.stock
