SELECT a.code device_code,a.name device_name,b.id transaction,DATE_FORMAT(b.start_date,'%d/%m/%Y %H:%i:%s') start_date,
CASE WHEN b.end_date is null THEN 'Chưa kết thúc'
     ELSE DATE_FORMAT(b.end_date,'%d/%m/%Y %H:%i:%s') END end_date,
CASE WHEN b.end_date is null THEN ''
     ELSE TIMESTAMPDIFF(SECOND,b.start_date,b.end_date) END total_time,
c.description,concat(c.value,e.symbol) value,d.code,d.name,
CASE WHEN b.device_status = '0' THEN 'Không hoạt động'
    WHEN b.device_status = '1' THEN 'Tốt'
    WHEN b.device_status = '2' THEN 'Xảy ra lỗi'
ELSE 'unknown' END  device_status
FROM device a,device_transaction b,device_transaction_detail c,area d,device_properties e
WHERE a.id = b.device_id
AND c.device_transaction_id = b.id
AND a.area_id = d.id
AND c.device_pro_id = e.id
<%p_device%>
<%p_area%>
<%p_device_status%>
<%p_property%>
<%p_from_date%>
<%p_to_date%>
ORDER BY d.id,device_name,b.id,b.start_date