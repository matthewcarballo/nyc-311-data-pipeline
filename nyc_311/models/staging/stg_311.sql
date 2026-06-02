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
        INITCAP(LOWER(borough))   as borough,
        CAST(latitude AS NUMERIC) as latitude,
        CAST(longitude AS NUMERIC) as longitude,
        CASE 
            WHEN created_date = 'NaN' OR created_date IS NULL 
            THEN NULL
            ELSE created_date::timestamp
        END as created_at,
        CASE 
            WHEN closed_date = 'NaN' OR closed_date IS NULL 
            THEN NULL
            ELSE closed_date::timestamp
        END as closed_at
    from source
    where unique_key is not null
)

select * from cleaned