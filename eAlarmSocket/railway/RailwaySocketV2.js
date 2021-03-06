/**
 * Socket provider to control hardware
 * @author: TuanNA
 * @copyright: Ngo Anh Tuan <ngo.tuan12@gmail.com>
 * @company: LienViet co.,ltd
 */
//Delay time between 2 transaction milliseconds
var delay_time = 30000;

var net = require('net'), fs = require('fs');
var util = require("util");
var gjson = require("../json_sans_eval.js");
var gateways = {};
var dispatchers = [];
var monitors = [];
var server;
var gateway;
var properties;
var server_ip = '10.10.0.17:6000';
var ip = '10.10.0.17';
//var ip = '0.0.0.0';
var clients = [];
var connDB = require("../util/RailwayAppServer.js").connDB;

var logFile = fs.createWriteStream('.././log/RailwayErrorLogV2.txt');
//-----------------------------------------
//FUNCTION
//-----------------------------------------
/**
 * @author TuanNA
 * @param strLog
 */
function log(strLog)
{
	var dt = new Date();
	// logFile.write(dt.toString()+": "+strLog+"\n");
	console.log(strLog);
}

function updateActionStatus(device_id)
{
}

/**
 * @author TuanNA
 * @since 03/03/2014
 * @version 1.0
 */
function sendWebsocketMessage(conn, handle, response)
{
	response.handle = handle;
	conn.send(JSON.stringify(response));
}
function sendGatewayCommand(cmd, socket)
{
	var strResponse = JSON.stringify(cmd);
	//set cmd_id
	if(cmd.type==="request")
	{
		var strSQL = "INSERT INTO cmd(name,type,content) " + "VALUES(?,?,?)";
		
		connDB.query(strSQL, [ cmd.cmd,cmd.type,strResponse ], function(err, rows, fields)
		{
			if (err)
			{
				log(err);
				return;
			}
			cmd.cmd_id = rows.insertId;
			
			strResponse = JSON.stringify(cmd);
			
			log("type gateway:" + socket.gatewayinfo.type);
			if (socket.gatewayinfo.type === "1"||socket.gatewayinfo.type === "4")
			{
				strResponse = String.fromCharCode(0x01) + strResponse + String.fromCharCode(0x0A) + String.fromCharCode(0x0D);
				log("response:" + strResponse);
			} else if (socket.gatewayinfo.type === "2" || socket.gatewayinfo.type === "3")
			{
				strResponse = strResponse + "\n";
			}
			if (socket !== null)
			{
				socket.write(strResponse);
			}
			
			//send to connected device
			for(var i=0;i<clients.length;i++)
			{
				if(clients[i].device_id === socket.gatewayinfo.id)
				{
					clients[i].send(strResponse);
				}
			}
		});
	}
	else
	{
		log("type gateway:" + socket.gatewayinfo.type);
		if (socket.gatewayinfo.type === "1"||socket.gatewayinfo.type === "4")
		{
			strResponse = String.fromCharCode(0x01) + strResponse + String.fromCharCode(0x0A) + String.fromCharCode(0x0D);
			log("response:" + strResponse);
		} else if (socket.gatewayinfo.type === "2" || socket.gatewayinfo.type === "3")
		{
			strResponse = strResponse + "\n";
		}
		if (socket !== null)
		{
			socket.write(strResponse);
		}
		
		//send to connected device
		for(var i=0;i<clients.length;i++)
		{
			if(clients[i].device_id === socket.gatewayinfo.id)
			{
				clients[i].send(strResponse);
			}
		}
	}
}
/**
 * @author: TuanNA
 * @since: 28/08/2014
 */
function insertDeviceTransaction(socket, current_transaction_id, device_id,
		device_status, description, transaction_detail)
{
	var strSQL = "";
	// close old transaction
	if (current_transaction_id !== null)
	{
		strSQL = "UPDATE device_transaction SET end_date = now() " + "WHERE id = ? ";
		connDB.query(strSQL, [ current_transaction_id ], function(err, rows,
				fields)
		{
			if (err)
			{
				log(err);
				return;
			}
		});
	} else
	{
		strSQL = "UPDATE device_transaction SET end_date = now() " + "WHERE device_id = ? AND end_date IS NULL ";
		connDB.query(strSQL, [ device_id ], function(err, rows, fields)
		{
			if (err)
			{
				log(err);
				return;
			}
		});
	}
	// insert new transaction
	strSQL = "INSERT INTO device_transaction(device_id,device_status,description) " + "VALUES(?,?,?)";
	connDB
			.query(
					strSQL,
					[ device_id, device_status, description ],
					function(err, rows, fields)
					{
						if (err)
						{
							log(err);
							return;
						}
						var current_transaction_id = rows.insertId;
						if (socket !== null)
						{
							socket.current_transaction_id = rows.insertId;
							socket.device_status = device_status;
						}
						// Insert transaction
						for (var i = 0; i < transaction_detail.length; i++)
						{
							var detail = transaction_detail[i];
							strSQL = "INSERT INTO device_transaction_detail(device_transaction_id,device_pro_id,value,description) " + "VALUES(?,?,?,?) ";
							connDB.query(strSQL, [ current_transaction_id,
									detail.device_pro_id, detail.value,
									detail.description ]);
						}
					});
}
/**
 * @param socket
 * @param device_id
 * @param status
 * @param strServerIP
 * @param strDescription
 * @param transaction_detail
 * @since 15/09/2014
 */
function updateDevice(socket, device_id, status, strServerIP, strDescription,
		transaction_detail)
{
	var param = [];
	var strSQL = "UPDATE device " + " SET status = ? ";
	param.push(status);
	if (strServerIP !== null)
	{
		strSQL += ",connected_server = ? ";
		param.push(strServerIP);
	}
	if (strDescription !== null)
	{
		strSQL += ",description = ? ";
		param.push(strDescription);
	}
	strSQL += " WHERE id = ? ";
	param.push(device_id);
	connDB.query(strSQL, param, function(err)
	{
		if (err)
		{
			log(err);
			return;
		}
		insertDeviceTransaction(socket, socket.current_transaction_id,
				device_id, status, strDescription, transaction_detail);
	});
}

/**
 * @author TuanNA
 * @param device_id
 * @param action_status
 */
function updateDeviceActionStatus(device_id,action_status)
{
	var strSQL = "UPDATE device " + " SET action_status = ? " + " WHERE id = ? ";
	connDB.query(strSQL, [action_status,device_id]);
}
/**
 * @author TuanNA
 * @since 19/09/2014
 * @description: <p>Kiem tra cam bien phu</p> 
 *		<p>Neu bi mat cam bien chinh khong hoat dong dem thoi gian hoat dong cam bien phu</p>
 */
function checkMirrorSensor(infor_id,device_id,parent_code,parent_value,mirror_code,mirror_value)
{
	//get current transaction
	var strSQL = "SELECT id FROM sensor_transaction a WHERE infor_id = ? AND end_date IS NULL ";
	connDB
	.query(
			strSQL,
			[ infor_id ],
			function(err, rows)
			{
				var transaction_id;
				if (rows.length !== 0)
				{
					transaction_id = rows[0].id;
				}
				var strSQL = "";
				//neu cam bien chinh khong hoat dong
				if(parent_value === 0 && mirror_value !==0)
				{
					if(typeof transaction_id ==='undefined')
					{
						log("insert sensor transaction");
						strSQL = "INSERT INTO sensor_transaction(infor_id,value) VALUES(?,?) ";
						connDB.query(strSQL,[infor_id,mirror_value]);
					}
				}
				//neu da hoac dang hoat dong binh thuong
				else
				{
					//check transaction neu co thi ket thuc
					if(typeof transaction_id !=='undefined')
					{
						strSQL = "UPDATE sensor_transaction SET end_date = now() WHERE infor_id = ? AND end_date IS NULL ";
						connDB.query(strSQL,[infor_id]);
					}
				}
			});
}
/**
 * @author TuanNA
 * @since 03/03/2014
 * @version 1.0
 */
function updateDeviceInfor(socket, device_id, infors,type)
{	
	var m_types = [];
	switch(type)
	{
		case "on_change":
			m_types.push('2');
			m_types.push('5');
			m_types.push('1');
			m_types.push('3');
			m_types.push('4');
			break;
		case "send_data":
			m_types.push('1');
			m_types.push('3');
			m_types.push('4');
			break;
		case "get_test":
			m_types.push('6');
			m_types.push('3');
			m_types.push('4');
			m_types.push('1');
			break;
	}
	var strActionStatus = socket.gatewayinfo.action_status;
	var strSQL = "SELECT a.id infor_id,b.* FROM device_infor a,device_properties b ";
	strSQL += "WHERE a.device_pro_id = b.id " + "AND a.device_id = ? AND b.p_type = '2' ";
	strSQL += "AND a.`status` = '1' ";
	strSQL += "AND m_type in( ";
	for(var i=0;i < m_types.length;i++)
	{
		strSQL += "?,";
	}
	strSQL += "'0') ";
	var transaction_detail = [];
	log("Device id: " + device_id);
	connDB
			.query(
					strSQL,
					[ device_id ].concat(m_types),
					function(err, rows)
					{
						if (err)
						{
							log(err);
							return;
						}
						var strDescription = "";
						var strStatus = "1";
						strSQL = "UPDATE device_infor SET value = ? WHERE device_id = ? and device_pro_id = (SELECT id FROM device_properties WHERE code = ? AND p_type = '2' )";
						var properties = rows;
						var i;
						
						for (i = 0; i < properties.length; i++)
						{
							var property = properties[i];
							var key = property.code;
							var value = 0;
							if (infors.hasOwnProperty(key))
							{
								value = infors[key];
							}
							
							log(key + ":" + value);
							connDB.query(strSQL, [ value, device_id, key ]);
							// check alarm
							if(property.m_type === "3")
							{
								continue;
							}
							if(property.m_type === "4")
							{
								continue;
							}
							//neu la cam bien chinh
							if(property.require === "1")
							{
								var issue_description = "";
								if (value >= property.max_alarm)
								{
									strDescription += property.name + " cao(" +value +"); ";
									transaction_detail.push({
										"description" : property.name + " cao",
										"value" : value,
										"device_pro_id" : property.id
									});
								} else if (value <= property.min_alarm)
								{
									strDescription += property.name + " thấp(" +value +"); ";
									transaction_detail.push({
										"description" : property.name + " thấp",
										"value" : value,
										"device_pro_id" : property.id
									});
								}
							}
							//neu la cam bien phu
							else if(property.require === "0")
							{
								log("check parent");
								var parent_property;
								//parent property
								for(var j=0;j<properties.length;j++)
								{
									if(properties[j].id === property.parent_id)
									{
										parent_property = properties[j];
										break;
									}
								}
								//check sensor
								if(typeof parent_property !=='undefined')
								{
									log("check cam bien phu");
									var parent_value = infors[parent_property.code];
									var parent_code = parent_property.code;
									checkMirrorSensor(property.infor_id,device_id,parent_code,parent_value,key,value);
								}
							}
						}
						// update device status
						if (strDescription !== "")
						{
							strStatus = "2";
						}
						if (socket.device_status !== strStatus)
						{
							updateDevice(socket, device_id, strStatus,
									server_ip, strDescription,
									transaction_detail);
							log('status change '+ '{"handle":"on_status_change","device_id":"'+socket.gatewayinfo.id+'","status":"'+strStatus+'"}');
							for(var m=0;m<clients.length;m++)
							{
								if(clients[m].monitor)
								{
									clients[m].send('{"handle":"on_status_change","device_id":"'+socket.gatewayinfo.id+'","status":"'+strStatus+'"}');
								}
								
							}
						}
					});
}


/**
 * @param gmac
 * @returns
 */
function findGatewayByGMac(gmac)
{
	for (var i = 0; i < gateways.length; i++)
	{
		if (gateways[i].gatewayinfo.mac_add === gmac)
		{
			return gateways[i];
		}
	}
	return null;
}



/**
 * 
 * @param request
 * @param socket
 */
function announce(request, socket)
{
	log(request.body.G_MAC);
	var strSQL = "SELECT id,mac_add,connected_server,`status`,`type`,`action_status` FROM device WHERE mac_add = ? ";
	connDB
			.query(
					strSQL,
					[ request.body.G_MAC ],
					function(err, rows, fields)
					{
						if (err)
						{
							log(err);
							socket.isok = false;
							return;
						}
						// Neu chua khoi tao du lieu
						if (rows.length !== 0)
						{
							socket.isok = true;
							var gatewaydata = rows[0];
							// updateDeviceCommandLog(gatewaydata.id,JSON.stringify(request),"1");
							socket.gatewayinfo = gatewaydata;

							log("---------connect-success-------------");
							// check last transaction
							if (typeof gateways[gatewaydata.id] !== 'undefined' && gateways[gatewaydata.id] !== null)
							{
//								&& typeof gateways[gatewaydata.id].last_connect !== 'undefined'
								log("last connect :" + gateways[gatewaydata.id].last_connect);
								{
									log("clear timeout");
									clearTimeout(gateways[gatewaydata.id].tid);
								}
								socket.device_status = gateways[gatewaydata.id].device_status;
								socket.current_transaction_id = gateways[gatewaydata.id].current_transaction_id;
								socket.railway_session = gateways[gatewaydata.id].railway_session;
							}
//							else
//							{
//								// update connected server
//								updateDevice(socket, gatewaydata.id, '0',
//										server_ip, "Bắt đầu kết nối!", []);
//
//							}
							gateways[gatewaydata.id] = socket;
							// response
							var response = {
								"type" : "response",
								"cmd" : "announce",
								"body" : {
									"result" : "ok"
								}
							};
							sendGatewayCommand(response, socket);
							socket.isConnect = true;
							// updateGatewayStatus(socket,true);
							for(var i=0;i<clients.length;i++)
							{
								if(clients[i].device_id === socket.gatewayinfo.id)
								{
									clients[i].send(JSON.stringify(request));
								}
							}
						} else
						{
							log("---------connect-failed-------------");
							socket.end();
						}
					});
}
/**
 * @param device_id
 * @param command
 * @param type
 */
function updateDeviceCommandLog(device_id, command, type)
{
	connDB
			.query(
					"INSERT INTO device_command_log SET device_id = ?,command = ?,type = ? ",
					[ device_id, command, type ], function(err)
					{
						if (err)
						{
							log(err);
							return;
						}
					});
}


/**
 * @param str
 */
function sendToMonitor(str)
{
	for (var i = 1; i < monitors.length; i++)
	{
		sendGatewayCommand(str, monitors[i]);
	}
}

/**
 * 
 */
function init_properties()
{
	var strSQL = "SELECT * FROM device_properties WHERE p_type = '2' ";
	connDB.query(strSQL, function(err, rows, fields)
	{
		if (err)
		{
			throw err;
		}
		properties = rows;
		//update device transaction
		strSQL = "UPDATE device_transaction SET end_date = now() WHERE end_date IS NULL AND device_id IN ( ";
		strSQL += "SELECT id FROM device WHERE connected_server = ? )";
		connDB.query(strSQL, [ server_ip ], function(err, rows, fields)
		{
			if (err)
			{
				log(err);
				return;
			}
			//update device
			strSQL = "UPDATE device SET status = '0',action_status = '0' WHERE connected_server = ? ";
			connDB.query(strSQL, [ server_ip ], function(err, rows, fields)
			{
				if (err)
				{
					log(err);
					return;
				}
			});
		});
	});
}
/**
 * @param gateway_id
 * @since: 15/09/2014
 */
function timeOutFromServer(gateway_id)
{
	if (typeof gateways[gateway_id].tid !=='undefined')
	{
		clearTimeout(gateways[gateway_id].tid);
		updateDevice({"current_transaction_id":gateways[gateway_id].current_transaction_id}, gateway_id, '0', '', "Mất kết nối với server.", [ {
			"description" : "Mất kết nỗi với server",
			"value" : null,
			"device_pro_id" : null
		} ]);
		updateDeviceActionStatus(gateway_id,'0');
		for(var m=0;m<clients.length;m++)
		{
			if(clients[m].monitor)
			{
				clients[m].send('{"handle":"on_status_change","device_id":"'+gateway_id+'","status":"0"}');
				clients[m].send('{"handle":"on_railway_change","device_id":"'+gateway_id+'","action_status":"0"}');
			}
			
		}
		//gateways[gateway_id] = null;
		delete gateways[gateway_id];
	}

}
/**
 * @update 09/09/2014
 * @param socket
 */
function onClose(socket)
{
	log('disconnected');
	if (socket.isConnect)
	{
		if (socket.gatewayinfo !== null)
		{
			log('gateway_id' + socket.gatewayinfo.id);
			var tid = setTimeout(timeOutFromServer,
					delay_time,socket.gatewayinfo.id);
			gateways[socket.gatewayinfo.id] = {
				last_connect : new Date(),
				tid : tid,
				current_transaction_id : socket.current_transaction_id,
				device_status : socket.device_status,
				railway_session: socket.railway_session
			};
		}
	}
	socket.isConnect = false;
	socket.end();
}

/**
 * @param device_id
 * @param railway_session
 */
function createRailwaySession(socket,device_id,railway_session)
{
	var strSQL = "INSERT INTO railway_session(`device_id`,`start_date`,`end_date`,`status`) " +
			" VALUES(?,?,?,?)";
	var infors = railway_session.infors;
	connDB.query(strSQL, [ device_id,railway_session.start_date,railway_session.end_date,railway_session.action_status ], function(err, rows, fields)
	{
		if (err)
		{
			log(err);
			return;
		}
		var railway_session_id = rows.insertId;
		//update device
		for (var key in infors)
		{
			if (infors.hasOwnProperty(key))
			{
				strSQL = "INSERT INTO railway_session_detail(`r_id`,`infor_id`,`value`,`issue_date`,`status`) " +
						" VALUES( ?,(SELECT a.id FROM device_infor a,device_properties b WHERE "+ 
						"a.device_id = ? "+
						"AND a.device_pro_id = b.id "+
						"AND b.code = ? ),? ,now() , ? ) ";
				connDB.query(strSQL, [ railway_session_id,device_id ,key , infors[key],railway_session.action_status ]);
			}
		}
		socket.railway_session.is_inprogress = false;
	});
}

/**
 * @param socket
 * @param infors
 */
function updateOnchangeAction(socket,infors)
{
	var action_status = socket.gatewayinfo.action_status;
	log("Action status: " + socket.gatewayinfo.action_status);
	log("Info:"+ JSON.stringify(infors));
	log("X1: " + infors.X1);
	log("X6: " + infors.X6);
	if((infors.X1 > 0 || infors.X2 >0) && infors.X3 === 0 && infors.X4 === 0 && infors.X5 === 0 && infors.X6 === 0)
	{
		action_status = "1";
		socket.railway_session = {};
		socket.railway_session.action_status = action_status;
		socket.railway_session.start_date = new Date();
		socket.railway_session.infors = 
			{
				"X1":0,"X2":0,"X3":0,"X4":0,"X5":0,"X6":0,
				"I1":0,"I2":0,"I3":0,"I4":0,"I5":0,"I6":0, "I7":0,"I8":0
			};
		socket.railway_session.is_inprogress = true;
	}
	else if(infors.X1 === 0 && infors.X2 === 0 && infors.X3 === 0 && infors.X4 === 0 && (infors.X5 > 0 || infors.X6 > 0))
	{
		action_status = "2";
		socket.railway_session = {};
		socket.railway_session.action_status = action_status;
		socket.railway_session.start_date = new Date();
		socket.railway_session.infors = 
			{
				"X1":0,"X2":0,"X3":0,"X4":0,"X5":0,"X6":0,
				"I1":0,"I2":0,"I3":0,"I4":0,"I5":0,"I6":0, "I7":0,"I8":0
			};
		socket.railway_session.is_inprogress = true;
	}
	else if(infors.X1 === 0 && infors.X2 === 0 && infors.X3 === 0 && infors.X4 === 0 && infors.X5 === 0 && infors.X6 === 0 && 
			infors.I1 === 0 && infors.I2 === 0 && infors.I3 === 0 && infors.I4 === 0 && infors.I5 === 0 && infors.I6 === 0 && infors.I7 === 0 && infors.I8 === 0)
	{
		if(typeof socket.railway_session!=='undefined'&& socket.railway_session !== null && socket.railway_session.is_inprogress === true)
		{
			socket.railway_session.end_date = new Date();
			createRailwaySession(socket,socket.gatewayinfo.id,socket.railway_session);
		}
		action_status = "0";
	}
	else if(infors.X1 === 0 && infors.X2 === 0 && infors.X3 === 0 && infors.X4 === 0 && infors.X5 === 0 && infors.X6 === 0 && 
			(infors.I1 > 0 || infors.I2 > 0 || infors.I3 > 0 || infors.I4 > 0 || infors.I7 > 0 || infors.I8 > 0))
	{
		action_status = "3";
	}
	else if(infors.X1 === 0 && infors.X2 === 0 && infors.X3 === 0 && infors.X4 === 0 && infors.X5 === 0 && infors.X6 === 0 && 
			(infors.I5 > 0 || infors.I6 > 0))
	{
		action_status = "4";
	}
	
	if(typeof socket.railway_session!=='undefined'&& socket.railway_session !== null && socket.railway_session.is_inprogress === true)
	{
		if(infors.X1 > socket.railway_session.infors.X1 )
		{
			socket.railway_session.infors.X1 = infors.X1;
		}
		if(infors.X2 > socket.railway_session.infors.X2)
		{
			socket.railway_session.infors.X2 = infors.X2;
		}
		if(infors.X3 > socket.railway_session.infors.X3)
		{
			socket.railway_session.infors.X3 = infors.X3;
		}
		if(infors.X4 > socket.railway_session.infors.X4)
		{
			socket.railway_session.infors.X4 = infors.X4;
		}
		if(infors.X5 > socket.railway_session.infors.X5)
		{
			socket.railway_session.infors.X5 = infors.X5;
		}
		if(infors.X6 > socket.railway_session.infors.X6)
		{
			socket.railway_session.infors.X6 = infors.X6;
		}
		
		if(infors.I1 > socket.railway_session.infors.I1)
		{
			socket.railway_session.infors.I1 = infors.I1;
		}
		if(infors.I2 > socket.railway_session.infors.I2)
		{
			socket.railway_session.infors.I2 = infors.I2;
		}
		if(infors.I3 > socket.railway_session.infors.I3)
		{
			socket.railway_session.infors.I3 = infors.I3;
		}
		if(infors.I4 > socket.railway_session.infors.I4)
		{
			socket.railway_session.infors.I4 = infors.I4;
		}
		if(infors.I5 > socket.railway_session.infors.I5)
		{
			socket.railway_session.infors.I5 = infors.I5;
		}
		if(infors.I6 > socket.railway_session.infors.I6)
		{
			socket.railway_session.infors.I6 = infors.I6;
		}
		if(infors.I7 > socket.railway_session.infors.I7)
		{
			socket.railway_session.infors.I7 = infors.I7;
		}
		if(infors.I8 > socket.railway_session.infors.I8)
		{
			socket.railway_session.infors.I8 = infors.I8;
		}
	}
//	//kiem tra chuong den
//	if(action_status === "1")
//	{
//		if((infors.X1 > 0 || infors.X2 >0 || infors.X3 > 0 && infors.X4 > 0)&& infors.X5 === 0 && infors.X6 === 0)
//		{
//			railway_session
//		}
//	}
//	else if(action_status === "2")
//	{
//		if(infors.X1 === 0 && infors.X2 === 0 && (infors.X3 > 0 || infors.X4 > 0 || infors.X5 > 0 || infors.X6 > 0))
//		{
//			
//		}
//	}
	log("Current action status: " + action_status);
	//send change rail way status to monitors
	if(action_status !== socket.gatewayinfo.action_status)
	{
		//update action status
		var strSQL = "UPDATE device SET action_status = ? WHERE id = ? "; 
		connDB.query(strSQL, [action_status,socket.gatewayinfo.id], function(err)
		{
			if (err)
			{
				log(err);
				return;
			}
		});
		socket.gatewayinfo.action_status = action_status;
		
		for(var i=0;i<clients.length;i++)
		{
			if(clients[i].monitor)
			{
				clients[i].send('{"handle":"on_railway_change","device_id":"'+socket.gatewayinfo.id+'","action_status":"'+action_status+'"}');
			}
			
		}
	}
}

//-----------------------------------------
//END FUNCTION
//-----------------------------------------
// -----------------------------------------
// init_properties
// -----------------------------------------
init_properties();
// -----------------------------------------
// Create websocket
// Websocket load data online
// -----------------------------------------
var WebSocketServer = require('ws').Server;
var wss = new WebSocketServer({
	port : 7000
});
wss.on('connection', function(conn)
{
	log('connected');
	clients.push(conn);
	conn.on("timeout", function()
	{
		conn.close();
		log("timeout");
	});

	conn.on("error", function(excep)
	{
		conn.close();
		log(excep);
	});
	
	conn.on('close', function()
	{
		log('disconnected');
		for (var i = 0; i < clients.length; i++)
		{
			if (clients[i] === conn)
			{
				clients.splice(i, 1);
				break;
			}
		}
	});
	conn.on('message', function(str)
	{
		try
		{
			var request;
			try
			{
				request = gjson.jsonParse(str);
			}
			catch (e)
			{
				if(conn.isAnnounce)
				{
					conn.send("command is not correct!");
				}
				else
				{
					conn.close();
					return;
				}
			}
			log(str);
			log(request.handle);
			// check announce
			if (!conn.isAnnounce && request.handle !== "announce")
			{
				conn.send("Session not annouce!");
				conn.close();
				return;
			}
			// switch function
			switch (request.handle)
			{
				case "announce":
					announce(conn);
					break;
				case "connect_device":
					connectDevice(conn, request.device_id,request.MAC);
					break;
				case "send_cmd":
					send_cmd(conn,request.device_id,request.body);
					break;
				case "monitor":
					conn.monitor = true;
					conn.send('{"handle":"monitor","msg":"OK"}');
					break;
				default:
					break;
			}
			// log("Received "+str);
			// conn.sendText(str.toUpperCase()+"!!!");
		} catch (e)
		{
			log(e.stack);
			conn.send(e.stack);
			conn.close();
		}
		// console.log('received: %s', message);
	});
	// announce
	function announce(conn)
	{
		conn.isAnnounce = true;
		conn.send('{"handle":"announce","msg":"OK"}');
		// websockets.push(conn);
	}
	// connect device
	function connectDevice(conn, device_id,MAC)
	{
		log("connect device: " + device_id);
		conn.device_id = device_id;
		conn.send('{"handle":"connect_device","msg":"Connected to ' + MAC +'"}');
	}
	
	function send_cmd(conn,device_id,body)
	{
		conn.send('Send cmd ');
		conn.send("body: " + JSON.stringify(body));
		var isSend = false;
		if(typeof gateways[device_id.toString()] !== 'undefined' )
		{
			log("gateway_id: " + gateways[device_id].gatewayinfo.id);
			sendGatewayCommand(body, gateways[device_id]);
			isSend = true;
		}
		
//		for (var i = 0; i < gateways.length; i++)
//		{
//			var gateway = gateways[i];
//			log("gateway_id: " + gateway.gatewayinfo.id);
//			if (gateway.gatewayinfo.id === device_id)
//			{
//				sendGatewayCommand(body, gateway);
//				isSend = true;
//				break;
//			}
//		}
		if(!isSend)
		{
			
			conn.send('Device is not connect! ');
		}
	}
	// ws.send('something');
});
// -----------------------------------------
// create socket server
// -----------------------------------------
var socketServer = net.createServer(function(socket)
{
	socket.checkConnect = false;
	log('connected');
	socket.setTimeout(150000);
	socket.isGetServer = false;
	socket.setNoDelay(true);
	// client.setTimeout(150000);
	socket.setEncoding("utf8");
	socket.setKeepAlive(true);

	socket.addListener("close", function(had_error)
	{
		onClose(socket);
	});
	socket.on("end", function()
	{
		onClose(socket);
	});
	socket.addListener("timeout", function()
	{
		onClose(socket);
		log("timeout");
	});

	socket.addListener("error", function(excep)
	{
		onClose(socket);
		log(excep);
	});
	socket.addListener('data', function(data)
	{
		try
		{
			log(typeof data);
			var str = data.toString();
			var strReuest = str.substring(1, str.length - 2);
			log(strReuest);
			var request = gjson.jsonParse(strReuest);
			log("cmd: " + request.cmd);
			if (!socket.isConnect && request.cmd !== "announce")
			{
				socket.end();
				return;
			}
			switch (request.cmd)
			{
				case "announce":
					log('-------------announce--------------');
					announce(request, socket);
					break;
				case "get_time":
					log("--------------------");
					log("get_time: " + data);
					log("--------------------");
					var date = new Date();
					var gwRequest = {
						"type" : "response",
						"cmd" : "get_time",
						"body" : {
							"Year" : date.getFullYear(),
							"Month" : date.getMonth() + 1,
							"Day" : date.getDate(),
							"Hour" : date.getHours(),
							"Minutes" : date.getMinutes(),
							"Seconds" : date.getSeconds()
						}
					};
					log("send response get time");
					sendGatewayCommand(gwRequest, socket);
					break;
				case "send_data":
					log("--------------------");
					log("----process-data----");
					updateDeviceInfor(socket, socket.gatewayinfo.id,
							request.body,"send_data");
					log("----end-process-data----");
					break;
				case "send_gw_request":
					var g_mac = request.G_MAC;
					var gateway = findGatewayByGMac(g_mac);
					if (gateway === null)
					{
						sendGatewayCommand({
							"message" : "gateway not found!"
						}, socket);
					} else
					{
						sendGatewayCommand(request.body, gateway);
						socket.on_gateway = g_mac;
						socket.on_cmd = request.body.cmd;
					}
					break;
				case "alarm":
					var response = {
						"type" : "response",
						"cmd" : " alarm",
						"body" : {
							"result" : "ok"
						}
					};
					updateDeviceInfor(socket, socket.gatewayinfo.id,
							request.body,"alarm");
					sendGatewayCommand(response, socket);
					break;
				case "get_test":
					log("--------------------");
					log("----process-data----");
					updateDeviceInfor(socket, socket.gatewayinfo.id,
							request.body,"get_test");
					log("----end-process-data----");
					break;
				case "on_change":
					log("--------------------");
					log("----process-data----");
					updateDeviceInfor(socket, socket.gatewayinfo.id,
							request.body,"on_change");
					log("----end-process-data----");
					//check sensor
					updateOnchangeAction(socket,request.body);
					break;
			}
			if(typeof socket.gatewayinfo !== 'undefined')
			{
				request.device_id = socket.gatewayinfo.id;
			}
			for(var i=0;i<clients.length;i++)
			{
				if(typeof clients[i] !== 'undefined'&& typeof socket.gatewayinfo !== 'undefined'  && clients[i].device_id === socket.gatewayinfo.id)
				{
					clients[i].send(JSON.stringify(request));
				}
			}
		}
		catch (e)
		{
			log(e.stack);
			socket.end();
			// socket.write(e.stack);
		}
	});
});
function alive()
{
	log("ALIVE");
	connDB.query("SELECT NOW() ");
}
/**
 * @author TuanNA
 * @since: 15/09/2014
 */
function start()
{
	setInterval(alive,300000);
	// listen socket
	socketServer.listen(6000, ip);
	// listen websocket
	log('socket server start on port 6000');
	log('websocket server start on port 7000');
}


//-----------------------------------------
//EXPORT
//-----------------------------------------
exports.start = start;

