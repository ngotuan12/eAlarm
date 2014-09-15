SELECT a.code device_code,a.name device_name,a.address,a.area_id,b.code area_code,b.name area_name,
    CASE WHEN a.status = '0' THEN 'Không hoạt động'
    WHEN a.status = '1' THEN 'Tốt'
    WHEN a.status = '2' THEN 'Đang xảy ra lỗi'
    ELSE 'unknown' END  status
FROM device a,area b
WHERE a.area_id = b.id
<%p_device%>
<%p_area%>
<%p_device_status%>
ORDER BY area_code,device_code,device_name