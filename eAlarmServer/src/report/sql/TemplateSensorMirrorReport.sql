SELECT c.code device_code,c.name device_name,DATE_FORMAT(a.start_date,'%d/%m/%Y %H:%i:%s') start_date,
CASE WHEN a.end_date is null THEN 'Chưa kết thúc'
     ELSE DATE_FORMAT(a.end_date,'%d/%m/%Y %H:%i:%s') END end_date,
CASE WHEN a.end_date is null THEN ''
     ELSE TIMESTAMPDIFF(SECOND,a.start_date,a.end_date) END total_time,
     a.description
FROM  sensor_transaction a,device_infor b, device c,device_properties d
where a.infor_id = b.id 
AND b.device_id = c.id
AND b.device_pro_id = d.id
AND d.code = 'Vac2'
<%p_device%>
<%p_area%>
<%p_device_status%>
<%p_property%>
<%p_from_date%>
<%p_to_date%>
ORDER BY c.id,device_name,b.id,a.start_date