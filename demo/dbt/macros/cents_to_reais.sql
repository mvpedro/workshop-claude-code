{% macro cents_to_reais(column_name) %}
    round(cast({{ column_name }} as float) / 100, 2)
{% endmacro %}
