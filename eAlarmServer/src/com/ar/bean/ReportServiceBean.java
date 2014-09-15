package com.ar.bean;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Date;

import ReportTDK.Report;

import com.ar.util.AppProcessor;
import com.ar.util.AppServer;
import com.ar.util.ReadSQLFile;
import com.fss.sql.Database;
import com.fss.util.StringUtil;

public class ReportServiceBean extends AppProcessor
{

	public void doGet() throws Exception
	{

	}

	@Override
	public void doPost() throws Exception
	{
		String request_type = request.getString("Method");
		switch (request_type)
		{
			case "DeviceReport":
				response.put("FileOut", exportDeviceReport());
				break;
			case "DeviceDetailReport":
				response.put("FileOut", exportDeviceDetailReport());
				break;
			case "DeviceErrorReport":
				response.put("FileOut", exportDeviceErrorReport());
				break;
		}

	}

	/**
	 * @return
	 * @throws Exception
	 */
	private String exportDeviceReport() throws Exception
	{
		ResultSet rs = null;
		PreparedStatement pstm = null;
		try
		{
			// template path
			String excelTemplatePath = AppServer.getParam("ExcelTemplatePath");
			String templatePath = AppServer.getParam("TemplatePath");
			String strReportOut = AppServer.getParam("ReportOut");
			String strFileName = "TemplateDeviceReport";
			String strFileOut = strFileName
					+ StringUtil.format(new Date(), "yyyyMMddhhmmss");
			// String strFileOut = "dev_report";
			// read sql file
			String strSQL = new ReadSQLFile(templatePath + strFileName + ".sql")
					.getSQLQuery();
			// open connection
			open();
			// get parameter
			String strDeviceID = request.getString("device_id");
			String strDeviceSQL = "";
			String strAreaID = request.getString("area_id");
			String strAreaeSQL = "";
			String strDeviceStatus = request.getString("device_status");
			String strDeviceStatusSQL = "";
			// set sql parameter
			// device
			if (!strDeviceID.equals("ALL"))
			{
				strDeviceSQL = " AND a.id ='" + strDeviceID + "' ";
			}
			strSQL = strSQL.replaceAll("<%p_device%>", strDeviceSQL);
			// area
			if (!strAreaID.equals("ALL"))
			{
				strAreaeSQL = " AND b.id ='" + strAreaID + "' ";
			}
			strSQL = strSQL.replaceAll("<%p_area%>", strAreaeSQL);
			// device status
			if (!strDeviceStatus.equals("ALL"))
			{
				strDeviceStatusSQL = " AND a.status ='" + strDeviceStatus
						+ "' ";
			}
			strSQL = strSQL.replaceAll("<%p_device_status%>",
					strDeviceStatusSQL);
			// prepare statement
			pstm = mcnMain.prepareStatement(strSQL);
			// execute query
			rs = pstm.executeQuery();
			// create report
			Report report = new Report(rs, excelTemplatePath + strFileName
					+ ".xls", strReportOut + strFileOut + ".xls");
			report.setParameter("$Report_Date",
					StringUtil.format(new Date(), "yyyy-MM-dd"));
			report.setParameter("$Report_Time",
					StringUtil.format(new Date(), "HH:mm:ss"));
			// fill data
			report.fillDataToExcel();
			// create file
			// createRealFile(strFileOut);
			// return link
			return strFileOut + ".xls";
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
			throw ex;
		}
		finally
		{
			Database.closeObject(rs);
			Database.closeObject(pstm);
			close();
		}
	}
	/**
	 * @return
	 * @throws Exception
	 */
	private String exportDeviceErrorReport() throws Exception
	{
		ResultSet rs = null;
		PreparedStatement pstm = null;
		try
		{
			// template path
			String excelTemplatePath = AppServer.getParam("ExcelTemplatePath");
			String templatePath = AppServer.getParam("TemplatePath");
			String strReportOut = AppServer.getParam("ReportOut");
			String strFileName = "TemplateDeviceErrorReport";
			String strFileOut = strFileName
					+ StringUtil.format(new Date(), "yyyyMMddhhmmss");
			// String strFileOut = "dev_report";
			// read sql file
			String strSQL = new ReadSQLFile(templatePath + strFileName + ".sql")
					.getSQLQuery();
			// open connection
			open();
			// get parameter
			String strDeviceID = request.getString("device_id");
			String strDeviceSQL = "";
			String strAreaID = request.getString("area_id");
			String strAreaeSQL = "";
			String strDeviceStatus = request.getString("device_status");
			String strDeviceStatusSQL = "";
			String strPropertyID = request.getString("property_id");
			String strPropertySQL = "";
			String strFromDate = request.getString("from_date");
			String strFromDateSQL = "";
			String strToDate = request.getString("to_date");
			String strToDateSQL = "";
			// set sql parameter
			// device
			if (!strDeviceID.equals("ALL"))
			{
				strDeviceSQL = " AND a.id ='" + strDeviceID + "' ";
			}
			strSQL = strSQL.replaceAll("<%p_device%>", strDeviceSQL);
			// area
			if (!strAreaID.equals("ALL"))
			{
				strAreaeSQL = " AND d.id ='" + strAreaID + "' ";
			}
			strSQL = strSQL.replaceAll("<%p_area%>", strAreaeSQL);
			// device status
			if (!strDeviceStatus.equals("ALL"))
			{
				strDeviceStatusSQL = " AND b.device_status ='" + strDeviceStatus
						+ "' ";
			}
			strSQL = strSQL.replaceAll("<%p_device_status%>",
					strDeviceStatusSQL);
			// property_id
			if (!strPropertyID.equals("ALL"))
			{
				strPropertySQL = " AND c.device_pro_id = '"+strPropertyID+"' ";
			}
			strSQL = strSQL.replaceAll("<%p_property%>",
					strPropertySQL);
			// from_date
			if (!strFromDate.trim().equals(""))
			{
				strFromDateSQL = " AND b.start_date > str_to_date('"+strFromDate+"','%d/%m/%Y') ";
			}
			strSQL = strSQL.replaceAll("<%p_from_date%>",
					strFromDateSQL);
			// property_id
			if (!strToDate.trim().equals(""))
			{
				strToDateSQL = " AND b.end_date < str_to_date('"+strToDate+"','%d/%m/%Y') ";
			}
			strSQL = strSQL.replaceAll("<%p_to_date%>",
					strToDateSQL);
			// prepare statement
			pstm = mcnMain.prepareStatement(strSQL);
			// execute query
			rs = pstm.executeQuery();
			// create report
			Report report = new Report(rs, excelTemplatePath + strFileName
					+ ".xls", strReportOut + strFileOut + ".xls");
			report.setParameter("$Report_Date",
					StringUtil.format(new Date(), "yyyy-MM-dd"));
			report.setParameter("$Report_Time",
					StringUtil.format(new Date(), "HH:mm:ss"));
			// fill data
			report.fillDataToExcel();
			// create file
			// createRealFile(strFileOut);
			// return link
			return strFileOut + ".xls";
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
			throw ex;
		}
		finally
		{
			Database.closeObject(rs);
			Database.closeObject(pstm);
			close();
		}
	}
	/**
	 * @return
	 * @throws Exception
	 */
	private String exportDeviceDetailReport() throws Exception
	{
		ResultSet rs = null;
		PreparedStatement pstm = null;
		try
		{
			// template path
			String excelTemplatePath = AppServer.getParam("ExcelTemplatePath");
			String templatePath = AppServer.getParam("TemplatePath");
			String strReportOut = AppServer.getParam("ReportOut");
			String strFileName = "TemplateDeviceDetailReport";
			String strFileOut = strFileName
					+ StringUtil.format(new Date(), "yyyyMMddhhmmss");
			// String strFileOut = "dev_report";
			// read sql file
			String strSQL = new ReadSQLFile(templatePath + strFileName + ".sql")
					.getSQLQuery();
			// open connection
			open();
			// get parameter
			String strDeviceID = request.getString("device_id");
			String strDeviceSQL = "";
			String strAreaID = request.getString("area_id");
			String strAreaeSQL = "";
			String strDeviceStatus = request.getString("device_status");
			String strDeviceStatusSQL = "";
			String strFromDate = request.getString("from_date");
			String strFromDateSQL = "";
			String strToDate = request.getString("to_date");
			String strToDateSQL = "";
			// set sql parameter
			// device
			if (!strDeviceID.equals("ALL"))
			{
				strDeviceSQL = " AND a.id ='" + strDeviceID + "' ";
			}
			strSQL = strSQL.replaceAll("<%p_device%>", strDeviceSQL);
			// area
			if (!strAreaID.equals("ALL"))
			{
				strAreaeSQL = " AND a.area_id ='" + strAreaID + "' ";
			}
			strSQL = strSQL.replaceAll("<%p_area%>", strAreaeSQL);
			// device status
			if (!strDeviceStatus.equals("ALL"))
			{
				strDeviceStatusSQL = " AND b.device_status ='" + strDeviceStatus
						+ "' ";
			}
			strSQL = strSQL.replaceAll("<%p_device_status%>",
					strDeviceStatusSQL);
			// from_date
			if (!strFromDate.trim().equals(""))
			{
				strFromDateSQL = " AND b.start_date > str_to_date('"+strFromDate+"','%d/%m/%Y') ";
			}
			strSQL = strSQL.replaceAll("<%p_from_date%>",
					strFromDateSQL);
			// property_id
			if (!strToDate.trim().equals(""))
			{
				strToDateSQL = " AND b.end_date < str_to_date('"+strToDate+"','%d/%m/%Y') ";
			}
			strSQL = strSQL.replaceAll("<%p_to_date%>",
					strToDateSQL);
			// prepare statement
			pstm = mcnMain.prepareStatement(strSQL);
			// execute query
			rs = pstm.executeQuery();
			// create report
			Report report = new Report(rs, excelTemplatePath + strFileName
					+ ".xls", strReportOut + strFileOut + ".xls");
			report.setParameter("$Report_Date",
					StringUtil.format(new Date(), "yyyy-MM-dd"));
			report.setParameter("$Report_Time",
					StringUtil.format(new Date(), "HH:mm:ss"));
			// fill data
			report.fillDataToExcel();
			// create file
			// createRealFile(strFileOut);
			// return link
			return strFileOut + ".xls";
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
			throw ex;
		}
		finally
		{
			Database.closeObject(rs);
			Database.closeObject(pstm);
			close();
		}
	}
	@Override
	public void doDelete() throws Exception
	{
	}
}
