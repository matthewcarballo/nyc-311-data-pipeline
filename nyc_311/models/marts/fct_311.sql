with staged as (
    select * from {{ ref('stg_311') }}
),

final as (
    select
        unique_key,
        complaint_type,
        descriptor,
        agency_name,
        borough,
        city,
        incident_zip,
        status,
        created_at,
        closed_at,
        CASE
            WHEN closed_at IS NOT NULL AND created_at IS NOT NULL
            THEN EXTRACT(EPOCH FROM (closed_at - created_at)) / 3600
            ELSE NULL
        END as hours_to_close,
        CASE
            WHEN status = 'Closed' THEN true
            ELSE false
        END as is_closed
    from staged
)

select * from final