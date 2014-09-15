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
var gjson = require("./json_sans_eval.js");
var gateways = {};
var dispatchers = [];
var monitors = [];
var server;
var gateway;
var properties;
//var server_ip = '10.10.0.17';
var server_ip = '0.0.0.0';
var clients = [];
var connDB = require("./AppServer.js").connDB;

var logFile = fs.createWriteStream('./log/ErrorLog.txt');
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
function sendGatewayCommand(response, socket)
{
	var strResponse = JSON.stringify(response);
	if (socket.gatewayinfo.type === "1")
	{
		strResponse = String.fromCharCode(0x01) + strResponse + String.fromCharCode(0x0A) + String.fromCharCode(0x0D);
	} else if (socket.gatewayinfo.type === "2" || socket.gatewayinfo.type === "3")
	{
		strResponse = strResponse + "\n";
	}
	if (socket !== null)
	{
		socket.write(strResponse);
	}
	log("response:" + strResponse);
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
 * @since 03/03/2014
 * @version 1.0
 */
function updateDeviceInfor(socket, device_id, infors)
{
	// var strSQL = "UPDATE device_infor SET value = ? WHERE device_id = ? and
	// device_pro_id = (SELECT id FROM device_properties WHERE code = ? )";
	var strSQL = "SELECT b.* FROM device_infor a,device_properties b ";
	strSQL += "WHERE a.device_pro_id = b.id " + "AND a.device_id = ? ";
	strSQL += "AND a.`status` = '1' ";
	var transaction_detail = [];
	log("Device id: " + device_id);
	connDB
			.query(
					strSQL,
					[ device_id ],
					function(err, rows)
					{
						if (err)
						{
							log(err);
							return;
						}
						var strDescription = "";
						var strStatus = "1";
						strSQL = "UPDATE device_infor SET value = ? WHERE device_id = ? and device_pro_id = (SELECT id FROM device_properties WHERE code = ? )";
						var properties = rows;
						var i;
						for (var key in infors)
						{
							if (infors.hasOwnProperty(key))
							{
								var value = infors[key];
								log(key + ":" + value);
								connDB.query(strSQL, [ value, device_id, key ]);
								// check alarm
								for (i = 0; i < properties.length; i++)
								{
									var property = properties[i];
									if (property.code === key && property.require === "1")
									{
										var issue_description = "";
										if (value >= property.max_alarm)
										{
											strDescription += property.name + " quá cao" + " <br> ";
											transaction_detail.push({
												"description" : property.name + " quá cao",
												"value" : value,
												"device_pro_id" : property.id
											});
										} else if (value <= property.min_alarm)
										{
											strDescription += property.name + " quá thấp" + " <br> ";
											transaction_detail.push({
												"description" : property.name + " quá thấp",
												"value" : value,
												"device_pro_id" : property.id
											});
										}
										break;
									}
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
						}
							
						// send to websocket connect
						var response = {};
						response.infors = infors;
						response.device_status = strStatus;
						response.device_id = device_id;
						for (i = 0; i < clients.length; i++)
						{
							if (clients[i] !== null && clients[i].device_id === response.device_id)
							{
								util.log("Send mesage to client " + i);
								sendWebsocketMessage(clients[i],
										"update_device_properties", response);
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
function checkMac(request, socket)
{
	log(request.body.G_MAC);
	var strSQL = "SELECT id,mac_add,connected_server,`status`,`type` FROM device WHERE mac_add = ? ";
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
							socket.gatewayinfo = rows[0];

							log("---------connect-success-------------");
							// check last transaction
							if (typeof gateways[gatewaydata.id] !== 'undefined' && typeof gateways[gatewaydata.id].last_connect !== 'undefined')
							{
								log("last connect :" + gateways[gatewaydata.id].last_connect);
								if (gateways[gatewaydata.id].tid !== null)
								{
									log("clear timeout");
									clearTimeout(gateways[gatewaydata.id].tid);
								}
								socket.device_status = gateways[gatewaydata.id].device_status;
								socket.current_transaction_id = gateways[gatewaydata.id].current_transaction_id;
							} else
							{
								// update connected server
								updateDevice(socket, gatewaydata.id, '0',
										server_ip, "Bắt đầu kết nối!", []);

							}
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
	var strSQL = "SELECT * FROM device_properties ";
	connDB.query(strSQL, function(err, rows, fields)
	{
		if (err)
		{
			throw err;
		}
		properties = rows;
		strSQL = "UPDATE device SET status = '0' WHERE connected_server = ? ";
		connDB.query(strSQL, [ server_ip ], function(err, rows, fields)
		{
			if (err)
			{
				log(err);
				return;
			}
		});
	});
}
/**
 * @param gateway_id
 * @since: 15/09/2014
 */
function timeOutFromServer(gateway_id)
{
	gateways[gateway_id] = null;
	if (gateways[gateway_id].tid !== null)
	{
		clearTimeout(gateways[gateway_id].tid);
		updateDevice(null, gateway_id, '0', '', "Mất kết nối với server.", [ {
			"description" : "Mất kết nỗi với server",
			"value" : null,
			"device_pro_id" : null
		} ]);
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
			var tid = setTimeout(timeOutFromServer(socket.gatewayinfo.id),
					delay_time);
			gateways[socket.gatewayinfo.id] = {
				last_connect : new Date(),
				tid : tid,
				current_transaction_id : socket.current_transaction_id,
				device_status : socket.device_status
			};
		}
	}
	socket.isConnect = false;
	socket.end();
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
	port : 8080
});
wss.on('connection', function(conn)
{
	log('connected');
	clients.push(conn);
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
			var request = gjson.jsonParse(str);
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
					connectDevice(conn, request.device_id);
					break;
				case "send_command":
					var gwRequest = request.body;
					var device_id = request.device_id;
					var isOK = false;
					for (var i = 0; i < gateways.length; i++)
					{
						var gateway = gateways[i];
						if (gateway.gatewayinfo.id === device_id)
						{
							sendGatewayCommand(gwRequest, gateway);
							isOK = true;
							break;
						}
					}
					var response = {};
					response.isOK = isOK;
					sendWebsocketMessage(conn, "send_command_response",
							response);
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
		// websockets.push(conn);
	}
	// connect device
	function connectDevice(conn, deviceID)
	{
		log("connect device: " + deviceID);
		conn.device_id = deviceID;
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
					checkMac(request, socket);
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
					sendGatewayCommand(gwRequest, socket);
					break;
				case "send_data":
					log("--------------------");
					log("----process-data----");
					updateDeviceInfor(socket, socket.gatewayinfo.id,
							request.body);
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
							request.body);
					sendGatewayCommand(response, socket);
					break;
			}
		} catch (e)
		{
			log(e.stack);
			// socket.write(e.stack);
		}
	});
});
/**
 * @author TuanNA
 * @since: 15/09/2014
 */
function start()
{
	// listen socket
	socketServer.listen(8888, server_ip);
	// listen websocket
	log('socket server start on port 8888');
	log('websocket server start on port 8080');
}

//-----------------------------------------
//EXPORT
//-----------------------------------------
exports.start = start;

