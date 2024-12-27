-- 1. Revenue Analysis by Location
SELECT 
    facility_name,
    COUNT(order_id) as total_orders,
    SUM(subtotal)::numeric(10,2) as total_revenue,
    (SUM(subtotal) / COUNT(order_id))::numeric(10,2) as avg_order_value,
    (AVG(order_rating))::numeric(10,2) as avg_rating,
    (COUNT(CASE WHEN status = 'completed' THEN 1 END)::float / 
     COUNT(*)::float * 100)::numeric(10,2) as completion_rate
FROM sales
GROUP BY facility_name
ORDER BY total_revenue DESC;

-- 2. Weekly Performance Trends
SELECT 
    DATE_TRUNC('week', created_at::timestamp) as week,
    COUNT(order_id) as orders,
    SUM(subtotal)::numeric(10,2) as revenue,
    (AVG(prep_time_for_ofo_minutes))::numeric(10,2) as avg_prep_time,
    COUNT(CASE WHEN order_issue_count > 0 THEN 1 END) as orders_with_issues
FROM sales
GROUP BY DATE_TRUNC('week', created_at::timestamp)
ORDER BY week;

-- 3. Customer Issues Impact
SELECT 
    CASE WHEN order_issue_count > 0 THEN 'Has Issues' ELSE 'No Issues' END as issue_status,
    COUNT(order_id) as order_count,
    (AVG(subtotal))::numeric(10,2) as avg_order_value,
    (AVG(order_rating))::numeric(10,2) as avg_rating
FROM sales
GROUP BY 
    CASE WHEN order_issue_count > 0 THEN 'Has Issues' ELSE 'No Issues' END;
