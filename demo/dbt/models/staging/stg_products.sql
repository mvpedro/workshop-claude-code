with source as (
    select * from {{ source('raw', 'raw_products') }}
)
select
    id as product_id,
    nome as product_name,
    descricao as description,
    preco_centavos as price_cents,
    {{ cents_to_reais('preco_centavos') }} as price_reais,
    estoque as stock,
    lower(trim(categoria)) as category,
    upper(sku) as sku
from source
