
  
  create view "workshop_demo"."main"."stg_products__dbt_tmp" as (
    with source as (
    select * from "workshop_demo"."main"."raw_products"
)
select
    id as product_id,
    nome as product_name,
    descricao as description,
    preco_centavos as price_cents,
    
    round(cast(preco_centavos as float) / 100, 2)
 as price_reais,
    estoque as stock,
    lower(trim(categoria)) as category,
    upper(sku) as sku
from source
  );
