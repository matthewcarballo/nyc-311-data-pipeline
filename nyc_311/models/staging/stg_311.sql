with source as (
    select * from raw_311
),

cleaned as (
    select
        unique_key,
        agency,
        agency_name,
        complaint_type,
        descriptor,
        incident_zip,
        city,
        status,
        initcap(lower(borough)) as borough,
        latitude::numeric as latitude,
        longitude::numeric as longitude,
        nullif(created_date, 'NaN')::timestamp as created_at,
        nullif(closed_date, 'NaN')::timestamp as closed_at
    from source
    where unique_key is not null
)

select * from cleaned