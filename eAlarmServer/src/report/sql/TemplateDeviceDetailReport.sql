SELECT a.address,a.code device_code,a.NAME device_name, b.device_id,DATE_FORMAT(b. 
	start_date,'%d/%m/%Y %H:%i:%s') start_date, 
	CASE 
		WHEN b.end_date IS NULL 
		THEN 'Chưa kết thúc' 
		ELSE DATE_FORMAT(b.end_date,'%d/%m/%Y %H:%i:%s') 
	END end_date , 
	CASE WHEN b.end_date is null THEN 0
		ELSE TIMESTAMPDIFF(SECOND,b.start_date,b.end_date) END total_time,
	CASE 
		WHEN b.device_status = '0' 
		THEN 'Không hoạt động' 
		WHEN b.device_status = '1' 
		THEN 'Tốt' 
		WHEN b.device_status = '2' 
		THEN 'Xảy ra lỗi' 
		ELSE 'unknown' 
	END device_status, b.description 
FROM device a,device_transaction b 
WHERE a.id = b.device_id
<%p_device%> 
<%p_area%> 
<%p_device_status%> 
ORDER BY a.area_id,b.device_id,b.start_date