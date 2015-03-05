/**
 * Socket provider to control hardware
 * @author: TuanNA
 * @copyright: Ngo Anh Tuan <ngo.tuan12@gmail.com>
 * @company: LienViet co.,ltd
 */

var net = require('net'), fs = require('fs');
var util = require("util");
var gjson = require("./json_sans_eval.js");
var connDB = require("./DemoAppServer.js").connDB;
var clients = [];
var gateways = {};
var datas = [
             {"T":35,"TA":32,"TB":12,"TC":30,"H":54,"S0":1,"S1":1,"S2":1,"It":817,"Ia":58,"Ib":418,"Ic":113,"Ut":289,"Ua":253,"Ub":261,"Uc":196,"Cost":1,"Cosa":1,"Cosb":1,"Cosc":1},
             {"T":30,"TA":28,"TB":11,"TC":25,"H":53,"S0":1,"S1":1,"S2":1,"It":800,"Ia":55,"Ib":410,"Ic":110,"Ut":285,"Ua":247,"Ub":258,"Uc":194,"Cost":1,"Cosa":1,"Cosb":1,"Cosc":1},
             {"T":25,"TA":24,"TB":10,"TC":27,"H":51,"S0":1,"S1":1,"S2":1,"It":770,"Ia":50,"Ib":408,"Ic":110,"Ut":280,"Ua":245,"Ub":252,"Uc":190,"Cost":1,"Cosa":1,"Cosb":1,"Cosc":1}
             ];
var server_ip = '10.10.0.17:6666';
var ip = '10.10.0.17';
var socket = {};
var delay_time = 2000;


function log(strLog)
{
	var dt = new Date();
	// logFile.write(dt.toString()+": "+strLog+"\n");
	console.log(strLog);
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
	//send to connected device
	for(var i=0;i<clients.length;i++)
	{
		if(clients[i].device_id === socket.gatewayinfo.id)
		{
			clients[i].send(response);
		}
	}
}



var WebSocketServer = require('ws').Server;
var wss = new WebSocketServer({
	port : 8383
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
		conn.send('Announce ok!');
		// websockets.push(conn);
	}
	// connect device
	function connectDevice(conn, device_id,MAC)
	{
		log("connect device: " + device_id);
		conn.device_id = device_id;
		conn.send('Connected to ' + MAC);
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




function updateDeviceInfor(socket, device_id, infors)
{
	var strSQL = "SELECT a.id infor_id,b.* FROM device_infor a,device_properties b ";
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
									if (property.code === key)
									{
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
							
						/*// send to websocket connect
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
						}*/
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

var tid;
function updateData()
{
	var index =  Math.floor(Math.random() * (2 - 0)) + 0;
	var data = datas[index];
	updateDeviceInfor(socket,5,data);
	//tid = setInterval(updateData(),delay_time);
}

function init()
{
	var strSQL = "update device set status ='0' ,connected_server = null";
	connDB.query(strSQL);
	socket.status = '1';
	setInterval(updateData,3000);
}

init();
