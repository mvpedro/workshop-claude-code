
  
  create view "workshop_demo"."main"."stg_customers__dbt_tmp" as (
    with source as (
    select * from "workshop_demo"."main"."raw_customers"
)
select
    id as customer_id,
    nome as customer_name,
    lower(trim(email)) as email,
    telefone as phone,
    case
        when lower(segmento) = 'ouro' then 'gold'
        when lower(segmento) = 'prata' then 'silver'
        else 'bronze'
    end as segment,
    ativo = 1 as is_active,
    cast(data_cadastro as date) as signup_date
from source
  );
