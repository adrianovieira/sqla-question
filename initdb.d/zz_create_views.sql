---- Create materialezed view and its index
---- REFRESH MATERIALIZED VIEW analysis.mv_survey_periodo_origin_status;
CREATE MATERIALIZED VIEW IF NOT EXISTS analysis.mview_surveys_loaded_at_status AS
    SELECT to_char(created_at, 'YYYY-MM-DD HH24:MI:SS')::TIMESTAMP AS loaded_at, 
        (CASE response_status_id
            WHEN 1 THEN 'valid'
            WHEN 2 THEN 'invalid'
            WHEN 3 THEN 'incomplete'
            WHEN 4 THEN 'pending'
            WHEN 5 THEN 'open'
            WHEN 6 THEN 'viewed'
        END) AS status,
        count(id) 
        FROM analysis.surveys 
        GROUP BY loaded_at, status;

CREATE INDEX ON analysis.mview_surveys_loaded_at_status (loaded_at, status);
