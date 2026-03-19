with source as (
    select * from {{ source('raw', 'raw_orders') }}
)
select
    id as order_id,
    cliente_id as customer_id,
    case status_code
        when 1 then 'pending'
        when 2 then 'processing'
        when 3 then 'shipped'
        when 4 then 'delivered'
        when 5 then 'cancelled'
    end as status,
    valor_total_centavos as total_cents,
    {{ cents_to_reais('valor_total_centavos') }} as total_reais,
    cast(data_pedido as date) as order_date,
    notas as notes
from source
