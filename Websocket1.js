/*
 * node-ws - pure Javascript WebSockets server
 * Copyright Bradley Wright <brad@intranation.com>
 */
 
// Use strict compilation rules - we're not animals
var net = require('net'),fs = require('fs');;
var util = require("util") ;
var gjson = require("./json_sans_eval.js");
var gateways = new Array;
var dispatchers = new Array;
var monitors = new Array;
var server;
var gateway;
var properties;
var server_ip = '10.10.0.17';
var clients = [];
connDB = require("./AppServer.js").connDB;

var logFile = fs.createWriteStream('/App/NodeJS/log/ErrorLog.txt');
function log(strLog)
{
	var dt = new Date();
	//logFile.write(dt.toString()+": "+strLog+"\n");
	console.log(strLog);
}
//-----------------------------------------
//init_properties
//-----------------------------------------
init_properties();
//-----------------------------------------
//Create websocket
//Websocket load data online
//-----------------------------------------
var WebSocketServer = require('ws').Server
, wss = new WebSocketServer({port: 8080});
wss.on('connection', function(conn) {
	clients.push(conn);
	conn.on('close', function() {
	    console.log('disconnected');
	    for(var i=0;i<clients.length;i++)
	    {
	    	if(clients[i]==conn)
    		{
	    		clients.splice(i,1);
	    		break;
    		}
	    }
	});
	conn.on('message', function(str) {
	  try
		{
			var request = gjson.jsonParse(str);
			//check announce
			if(!conn.isAnnounce&&request.handle!="announce")
			{
				conn.send("Session not annouce!");
				conn.close();
				return;
			}
			//switch function
			switch(request.handle)
			{
				case "announce":
					announce(conn);
					break;
				case "connect_device":
					connectDevice(conn,request.device_id);
					break;
				case "send_command":
					var gwRequest = request.body;
					var device_id = request.device_id;
					var isOK = false;
					for(var i=0;i<gateways.length;i++)
					{
						var gateway = gateways[i];
						if(gateway.gatewayinfo.id == device_id)
						{
							sendGatewayCommand(gwRequest,gateway);
							isOK = true;
							break;
						}
					}
					var response = new Object;
					response.isOK = isOK;
					sendWebsocketMessage(conn,"send_command_response",response);
					break;
				default:
					break;
			}
//			log("Received "+str);
			//conn.sendText(str.toUpperCase()+"!!!");
		}
		catch(e)
		{
			log(e.stack);
			conn.sendText(e.stack);
			conn.close();
		}
//      console.log('received: %s', message);
  });
	// announce
	function announce(conn) {
		conn.isAnnounce = true;
		// websockets.push(conn);
	}
	// connect device
	function connectDevice(conn, deviceID) {
		log("connect device: " + deviceID);
		conn.device_id = deviceID;
	}
//  ws.send('something');
});
// -----------------------------------------
//create socket server
//-----------------------------------------
var socketServer = net.createServer(function (socket) {
	socket.checkConnect = false;
	log('connected');
 	socket.setTimeout(150000);
 	socket.isGetServer = false;
 	socket.setNoDelay(true);
	//client.setTimeout(150000);
	socket.setEncoding("utf8");
	socket.setKeepAlive(true);
 	
	socket.addListener("close", function (had_error) {
		onClose(socket);
  	});
	socket.on("end", function () {
		onClose(socket);
  	});
	socket.addListener("timeout", function () {
		onClose(socket);
		log("timeout");	
	});

	socket.addListener("error", function (excep) {
		onClose(socket);
		log(excep);
	});
	socket.addListener('data', function (data) {
		try
		{
			log(typeof data);
	    	var str = data.toString();
	    	var strReuest = str.substring(1,str.length-2);
			log(strReuest);
	    	var request = gjson.jsonParse(strReuest);
	    	log("cmd: "+request.cmd);
	    	if(!socket.isConnect&&request.cmd!="announce")
			{
				socket.end();
				return;
			}
			switch(request.cmd)
			{
				case "announce":
					log('-------------announce--------------');
					checkMac(request,socket);					
					break;
				case "get_time":
					log("--------------------");
					log("get_time: "+data);
					log("--------------------");
					var date = new Date();
					var gwRequest ={"type": "response", "cmd": "get_time","body" : {"Year":date.getFullYear(),"Month":date.getMonth()+1,"Day":date.getDate(),"Hour":date.getHours(), "Minutes":date.getMinutes(),"Seconds":date.getSeconds()}};
					sendGatewayCommand(gwRequest,socket);
					break;
				case "send_data":
					log("--------------------");
					log("----process-data----");
					updateDeviceInfor(socket,socket.gatewayinfo.id,request.body);
					log("----end-process-data----");
					break;
				case "send_gw_request":
					var g_mac = request.G_MAC;
					var gateway = findGatewayByGMac(g_mac);
					if(gateway==null)
					{
						sendGatewayCommand({"message":"gateway not found!"},socket);
					}
					else
					{
						sendGatewayCommand(request.body,gateway);
						socket.on_gateway = g_mac;
						socket.on_cmd = request.body.cmd;
					}
	    			break;
				case "alarm":
					var response = {"type":"response","cmd":" alarm","body":{"result":"ok"}};
					updateDeviceInfor(socket,socket.gatewayinfo.id,request.body);
					sendGatewayCommand(response,socket);
					break;
	    		default:
	    			if(request.type == "response")
					{
					
					}
//					if(socket.gatewayinfo.type == "1"&& request.type == "response")
//					{
//						request.mac_add = socket.gatewayinfo.mac_add; 
//						for(var i=0;i<dispatchers.length;i++)
//						{
//							if(dispatchers[i].on_gateway == socket.gatewayinfo.mac_add&&
//							dispatchers[i].on_cmd == request.cmd)
//							{
//								log('response to dispatcher '+dispatchers[i].gatewayinfo.mac_add+JSON.stringify(request));
//								//response to dispatcher wait response
//								sendGatewayCommand(request,dispatchers[i]);
//								
//							}
//						}
//					}
	    			break;
	    		
				//sendToMonitor(str);
			}
		}
		catch(e)
		{
			log(e.stack);
//			socket.write(e.stack);
		}
    });
});
/**
*@author TuanNA
*@since 03/03/2014
*@version 1.0
*/
function updateDeviceInfor(socket,device_id,infors)
{
//	var strSQL = "UPDATE device_infor SET value = ? WHERE device_id = ? and device_pro_id = (SELECT id FROM device_properties WHERE code = ? )";
	var strSQL = "SELECT b.* FROM device_infor a,device_properties b "
				+ "WHERE a.device_pro_id = b.id " + "AND a.device_id = ? "
				+ "AND a.`status` = '1' ";
	var transaction_detail = []
	log("Device id: "+device_id);
	connDB.query(strSQL,[device_id], function(err,rows) 
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
		
		for(var key in infors) 
		{
			var value = infors[key];
			log(key+":"+value);
			connDB.query(strSQL,[value,device_id,key], function(err) 
			{
				if (err) 
				{
					log(err);
					return;
				}
			});	
			//check alarm
			for(var i=0;i<properties.length;i++)
			{
				var property = properties[i];
				if(property["code"]==key&&property["require"]=="1")
				{
					var issue_description = "";
					if(value>=property["max_alarm"])
					{
						strDescription += property["name"] + " quá cao" +" <br> ";
//						issue_description = property["name"] + " quá cao";
						transaction_detail.push({"description":property["name"] + " quá cao","value":value,"device_pro_id":property["id"]});
					}
					else if(value<=property["min_alarm"])
					{
						strDescription += property["name"] + " quá thấp"+" <br> ";
//						issue_description = property["name"] + " quá thấp";
						transaction_detail.push({"description":property["name"] + " quá thấp","value":value,"device_pro_id":property["id"]});
					}
//					if(issue_description!="")
//					{
//						var strSqlIssue = "INSERT INTO device_issue SET value = ?,description = ?,device_id = ?, device_pro_id = ?, reason_id = 1, status = '1' ";
//						connDB.query(strSqlIssue,[value,issue_description,device_id,property.id], function(err) 
//						{
//							if (err) 
//							{
//								log(err);
//								return;
//							}
//						});
//					}
					break;
				}
			}
		}
		//update device status
		if(strDescription != "")
			strStatus = "2";
		if(socket.device_status!=strStatus)
			updateDevice(socket,device_id, strStatus, server_ip, strDescription,transaction_detail);
		//send to websocket connect
		var response = new Object;
		response.infors = infors;
		response.device_status = strStatus;
		response.device_id = device_id;
		for(var i=0;i<clients.length;i++)
		{
			if(clients[i]!=null&&clients[i].device_id==response.device_id)
			{
				util.log("Send mesage to client "+i);
				sendWebsocketMessage(clients[i],"update_device_properties",response);
			}
		}
//		wss.broadcast = function(response) 
//		{
//			for(var i in this.clients)
//			{
//				if(clients[i].device_id==response.device_id)
//				{
//					util.log("Send mesage to client "+i);
//					sendWebsocketMessage(clients[i],"update_device_properties",response);
//				}
//			}
////		        this.clients[i].send(data);
//		};
//		webSocketServer.connections.forEach(function (connection) {
//			
//		});
//		for(var i=0;i<webSocketServer.connections.length;i++)
//		{
//			//websocket
//			var websocket = webSocketServer.connections[i];
//			if(websocket.device_id==device_id)
//			{
//				//response
//				var response = new Object;
//				response.infors = infors;
//				response.device_status = strStatus;
//				//send message
//				sendWebsocketMessage(websocket,"update_device_properties",response);
//			}
//		}
	});
	
}
/**
*@author TuanNA
*@since 03/03/2014
*@version 1.0
*/
function sendWebsocketMessage(conn,handle,response)
{
	response.handle = handle;
	conn.send(JSON.stringify(response));
}
/**
*
*
*/
function findGatewayByGMac(gmac)
{
	for(var i=0;i<gateways.length;i++)
	{
		if(gateways[i].gatewayinfo.mac_add == gmac)
		{
			return gateways[i];
		}
	}
	return null;
}
/**
 * 
 * @param socket
 */
function onClose(socket)
{
	log('disconnected');
	if(socket.isConnect)
	{
		if(socket.gatewayinfo!=null)
		{
			log('gateway_id'+socket.gatewayinfo.id);
			updateDevice(socket,socket.gatewayinfo.id,'0','',"Mất kết nối với server.",[]);
//			var strSQL = "update device_infor set value = 0 where device_id = ?";
//			connDB.query(strSQL,[socket.gatewayinfo.id], function(err) 
//			{
//				if (err) 
//				{
//					log(err);
//					return;
//				}
//			});
		}
		if(socket.gatewayinfo.type == "1")
		{
			//remove gateway
			for(var i=0;i<gateways.length;i++)
			{
				if(gateways[i].gatewayinfo.id==socket.gatewayinfo.id)
				{
					gateways.splice(i,1);
					
					break;
				}
				
			}
		}
		else if(socket.gatewayinfo.type == "2")
		{
			//remove monitor
			for(var i=0;i<monitors.length;i++)
			{
				if(monitors[i].gatewayinfo.id==socket.gatewayinfo.id)
				{
					monitors.splice(i,1);
					break;
				}
			}
		}
		else if(socket.gatewayinfo.type == "3")
		{
			//remove monitor
			for(var i=0;i<dispatchers.length;i++)
			{
				if(dispatchers[i].gatewayinfo.id==socket.gatewayinfo.id)
				{
					dispatchers.splice(i,1);
					break;
				}
			}
		}
	}
	socket.isConnect = false;
	socket.end();
}
function updateDevice(socket,device_id,status,strServerIP,strDescription,transaction_detail)
{
	var param = [];
	var strSQL = "UPDATE device "+
				" SET status = ? "; 
	param.push(status);
	if(strServerIP!=null)
	{
		strSQL += ",connected_server = ? ";
		param.push(strServerIP);
	}
	if(strDescription!=null)
	{
		strSQL += ",description = ? ";
		param.push(strDescription);
	}		
	strSQL += " WHERE id = ? ";
	param.push(device_id);
	connDB.query(strSQL,param, function(err) 
	{
		if (err) 
		{
			log(err);
			return;
		}
		insertDeviceTransaction(socket,socket.current_transaction_id,device_id,status,strDescription,transaction_detail);
	});
}

/**
 * 
 * @param request
 * @param socket
 */
function checkMac(request,socket) 
{
	log(request.body.G_MAC);
	var strSQL = "SELECT id,mac_add,connected_server,`status`,`type` FROM device WHERE mac_add = ? ";
	connDB.query(strSQL,[request.body.G_MAC], function(err, rows, fields) 
	{
		if (err) 
		{
			log(err);
			socket.isok = false;
			return;
		}
		//Neu chua khoi tao du lieu
		if(rows.length!=0)
		{
			socket.isok = true;
			var gatewaydata = rows[0];
			
			updateDeviceCommandLog(gatewaydata.id,JSON.stringify(request),"1");
			
			socket.gatewayinfo = rows[0];
			if(socket.gatewayinfo.type == "1")
			{
				gateways.push(socket);
			}
			else if(socket.gatewayinfo.type == "2")
			{
				monitors.push(socket);
			}
			else if(socket.gatewayinfo.type == "3")
			{
				dispatchers.push(socket);
			}
			log("---------connect-success-------------");
			//update connected server
			updateDevice(socket,gatewaydata.id,'0',server_ip,"Bắt đầu kết nối!",[]);
			//response
			var response = { "type":"response","cmd": "announce","body" : {"result": "ok"}};
			sendGatewayCommand(response,socket);
			socket.isConnect = true;
			//updateGatewayStatus(socket,true);
		}		
		else 
		{
			log("---------connect-failed-------------");
			socket.end();
		}
	});
}
function updateDeviceCommandLog(device_id,command,type)
{
	connDB.query("INSERT INTO device_command_log SET device_id = ?,command = ?,type = ? ",[device_id,command,type], function(err) 
	{
		if (err) 
		{
			log(err);
			return;
		}
	});
}
function sendGatewayCommand(response,socket)
{
	var strResponse = JSON.stringify(response);
	if(socket.gatewayinfo.type == "1")
	{
		strResponse = String.fromCharCode(0x01)+strResponse+String.fromCharCode(0x0A)+String.fromCharCode(0x0D);
	}
	else if(socket.gatewayinfo.type == "2"||socket.gatewayinfo.type == "3")
	{
		strResponse = strResponse+"\n";
	}
	if(socket!=null)
	{
		socket.write(strResponse);
	}
	updateDeviceCommandLog(socket.gatewayinfo.id,strResponse,"2");
	log("response:"+strResponse);
}

function sendToMonitor(str)
{
	for(var i=1;i<monitors.length;i++)
	{
		sendGatewayCommand(str,monitors[i]);
	}
}

/**
 * 
 */
function init_properties()
{
	var strSQL = "SELECT * FROM device_properties ";
	connDB.query(strSQL, function(err, rows, fields) {
		if (err)
			throw err;
		properties = rows;
	});
}
/*
 * @author: TuanNA
 * @since: 28/08/2014
 */
function insertDeviceTransaction(socket,current_transaction_id,device_id,device_status,description,transaction_detail)
{
	var strSQL =  ""
	//close old transaction
	if(current_transaction_id != null)
	{
		strSQL = "UPDATE device_transaction SET end_date = now() "
			+"WHERE id = ? ";
		connDB.query(strSQL,[current_transaction_id], function(err, rows, fields) {
			if (err)
			{
				log(err);
				return;
			}
		});
	}
	//insert new transaction
	strSQL = "INSERT INTO device_transaction(device_id,device_status,description) "
		+"VALUES(?,?,?)";
	connDB.query(strSQL,[device_id,device_status,description], function(err, rows, fields) 
	{
		if (err)
		{
			log(err);
			return;
		}
		socket.current_transaction_id = rows.insertId;
		socket.device_status = device_status;
		//Insert transaction
		for(var i=0;i<transaction_detail.length;i++)
		{
			var detail = transaction_detail[i];
			strSQL = "INSERT INTO device_transaction_detail(device_transaction_id,device_pro_id,value,description) "
				+"VALUES(?,?,?,?) ";
			connDB.query(strSQL,[socket.current_transaction_id,detail.device_pro_id,detail.value,detail.description], function(err, rows, fields) 
			{
				if (err)
				{
					log(err);
					return;
				}
			});
		}
	});
}

//listen socket
socketServer.listen(8888, "10.10.0.17");
//listen websocket
log('socket server start on port 8888');
log('websocket server start on port 8080');

