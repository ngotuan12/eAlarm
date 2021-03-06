var plot;
var data = [], totalPoints = 100;
var updateInterval = 9000;
var currentDeviceID;
var currentDeviceInforID;
var InforIndex = 0;
var device_infor;
var device;
var route;
var tid;
var table3;
var codes = ["X1","X2","X3","X4","X5","X6","I1","I2","I3","I4","I5","I6","I7","I8"];
function onGetDeviceInfor(device_id) {
	clearRailwayInfor();
	currentDeviceID = device_id;
	var csrftoken = $.cookie('csrftoken');
	var posting = $.post("/device-infor", {
		'csrfmiddlewaretoken' : csrftoken,
		'device_id' : device_id,
	});
	posting.done(function(data) 
	{
		$("#last-raiway").html("--");
		InforIndex = 0;
		device_infor = data.device_infor;
		device = data.device;
		route = data.route;
		currentDeviceInforID = data.device_infor[InforIndex].id;
		updateDevice();
		updateDeviceProperties(data);
		abortTimer();
		tid = setTimeout(mycode, updateInterval);
	});
}
function showRailwayHistory()
{
	
	var csrftoken = $.cookie('csrftoken');
	var posting = $.post("/ajax-railway-history", {
		'csrfmiddlewaretoken' : csrftoken,
		'device_id' : currentDeviceID,
	});
	
	posting.done(function(data) 
	{
		if(typeof table3 !== 'undefined')
			table3.fnDestroy();
		
		var tbody = $('#table3 tbody');
		tbody.empty();
		sessions = data.railway_sessions;
		//alert(JSON.stringify(data.railway_session));
		if (sessions.length==0)
		{
			var tbody_table4 = $('#table4 tbody');
			tbody_table4.empty();
		}
		for(var i=0;i<sessions.length;i++)
		{
			railway_session = sessions[i];
			//var row = $('<tr class="odd gradeX" id="'+ railway_session.id +'"></tr>');
			var row = $('<tr id="'+ railway_session.id + '"></tr>');
			
			//STT
			row.append($('<td>'+ (i+1).toString() +'</td>'));
			//Phien 
			if(railway_session.status==='2')
			{
				row.append($('<td> Chẵn</td>'));
			}	
			else if(railway_session.status==='1')
			{
				row.append($('<td> Lẻ</td>'));
			}
			else
				row.append($('<td> Unknown</td>'));
			//row.append($('<td>' + railway_session.id + '</td>'));
			//start date
			row.append($('<td>' + railway_session.start_date + '</td>'));
			//start date
			row.append($('<td>' + railway_session.end_date + '</td>'));
			//append to body
			tbody.append(row);
		}
		$('#table3 tbody tr').click(function(e)
		{
			railway_session_id = $(this).attr('id');
			$("#table3 tbody tr[id][id='"+ railway_session_id +"']").css('background-color','#8EE2BC');
			$("#table3 tbody tr[id][id!='"+ railway_session_id +"']").css('background-color','#fff');
			showRailwayDetailHistory(railway_session_id);
		});
		$('#table3 tbody tr').first().click();
		table3 = $('#table3').dataTable(
		{
			"bLengthChange": false,
			//"bFilter" : false,
			"bRetrieve": true,
			"bInfo":false,
			"bFilter":false,
			"sPaginationType" : "full_numbers",
			"iDisplayLength":10,
			"oLanguage":
			{
				"sLengthMenu":"Hiển thị _MENU_ bản ghi",
				"sInfo": "Hiển thị _START_ tới _END_ trong _TOTAL_ bản ghi",
				"oPaginate": 
				{
					"sFirst":      "<<",
					"sLast":       ">>",
					"sNext":       ">",
					"sPrevious":   "<"
				},
				"sSearch":"",
			}
		});
	});
}
function showRailwayDetailHistory(railway_session_id)
{
	$.fn.loading.show();
	var csrftoken = $.cookie('csrftoken');
	var posting = $.post("/ajax-railway-detail-history", {
		'csrfmiddlewaretoken' : csrftoken,
		'railway_session_id' : railway_session_id,
	});
	
	posting.done(function(data) 
	{
		var tbody = $('#table4 tbody');
		tbody.empty();
		railway_detail_sessions = data.railway_detail_sessions;
		//alert(JSON.stringify(data.railway_session));
		for(var i=0;i<railway_detail_sessions.length;i++)
		{
			railway_detail_session = railway_detail_sessions[i];
			var row = $('<tr></tr>');
			//STT
			//row.append($('<td>'+ (i+1).toString() +'</td>'));
			//infor_device 
			row.append($('<td>' + railway_detail_session.property.name + '</td>'));
			//value
			row.append($('<td>' + railway_detail_session.detail.value + '</td>'));
			//start date
			//row.append($('<td>' + railway_detail_session.detail.start_date + '</td>'));
			//end date
			//row.append($('<td>' + railway_detail_session.end_date + '</td>'));
			//status
			//row.append($('<td>' + railway_detail_session.detail.status + '</td>'));	
			if( railway_detail_session.detail.value > railway_detail_session.property.max_alarm || 
					railway_detail_session.detail.value < railway_detail_session.property.min_alarm)
			{
				//alert(railway_detail_session.property.max_alarm);
				row.css("color","red");
			}
			//append to body
			tbody.append(row);
		}
		$.fn.loading.hide();
	});
	//hide loading
	//$.fn.loading.hide();
}
function getCurrentDeviceInfor()
{
	var csrftoken = $.cookie('csrftoken');
	var posting = $.post("/device-infor", {
		'csrfmiddlewaretoken' : csrftoken,
		'device_id' : currentDeviceID,
	});
	posting.done(function(data) 
	{
		device = data.device;
		if(data.device.status!==device.status)
		{
			updateDevice();
		}
		updateDeviceProperties(data);
		//updateData(data.device_infor[InforIndex].value);
	});
}
function updateDevice()
{
	//update device name
	var deviceName = $('#device-name');
	deviceName.html("<a href=\"#\">"+route.name+" </a> - "+device.name);
	
	var deviceAddress = $('#device-address');
	deviceAddress.html(" "+device.address);
	
	var deviceStatus = $('#device-status');
	//device status on table
	var deviceStatusTable = $('#device-status-'+device.id);
	var deviceIssue = $('#device-issue');
	if(device.status==="1")
	{
		deviceIssue.html("");
		deviceStatus.attr("src","/images/ic_green.png");
		deviceStatusTable.attr("src","/images/ic_green.png");
	}
	else if(device.status==="2")
	{
		deviceIssue.html("Sự cố: <p style = \"padding-left: 5px;\">" + device.description+"</p>");
		deviceStatus.attr("src","/images/ic_red.png");
		deviceStatusTable.attr("src","/images/ic_red.png");
	}
	else if(device.status==="0")
	{
		deviceIssue.html("Sự cố: &nbsp; &nbsp; Mất kết nối");
		deviceStatus.attr("src","/images/ic_blue.png");
		deviceStatusTable.attr("src","/images/ic_blue.png");
	}
}
function updateDeviceProperties(response)
{
	data = response.device_infor
	//update device information
	var deviceInfor = $('#device-infor-1');
	deviceInfor.empty();
	var infors = data.filter(function (el){
		return el.properties.m_type === '1';
	});
	var infor = [];
	var i = 0;
	while( i < infors.length) 
	{
		var count = 0; //dem so column da insert vao row
		var row = $('<div>');
		row.attr("class", "row");
		while(count <4)
		{
			if( i === infors.length)
				break;
			infor = infors[i];
			//neu la cam bien phu
			if(infor.properties.require === '0')
			{
				//tim cha
				parent = infors.filter(function (el) 
				{
					return el.properties.id === infor.properties.parent
				})[0];
				addProperty(device,row,infor, parent);
			}
			else 
			{
				//add infor
				addProperty(device,row, infor);
			}
			count ++;
			i++;
		}
		row.appendTo(deviceInfor);
		if( i === infors.length)
			break;
	}
	
	deviceInfor = $('#device-infor-2');
	deviceInfor.empty();
	infors = data.filter(function (el){
		return el.properties.m_type === '3'||el.properties.m_type === '4';
	});
	infor = [];
	i = 0;
	while( i < infors.length) 
	{
		var count = 0; //dem so column da insert vao row
		var row = $('<div>');
		row.attr("class", "row");
		while(count <4)
		{
			if( i === infors.length)
				break;
			infor = infors[i];
			//neu la cam bien phu
			if(infor.properties.require === '0')
			{
				//tim cha
				parent = infors.filter(function (el) 
				{
					return el.properties.id === infor.properties.parent
				})[0];
				addProperty(device,row,infor, parent);
			}
			else 
			{
				//add infor
				addProperty(device,row, infor);
			}
			count ++;
			i++;
		}
		row.appendTo(deviceInfor);
		if( i === infors.length)
			break;
	}
	
	deviceInfor = $('#device-infor-3');
	deviceInfor.empty();
	infors = data.filter(function (el){
		return el.properties.m_type === '6';
	});
	infor = [];
	i = 0;
	while( i < infors.length) 
	{
		var count = 0; //dem so column da insert vao row
		var row = $('<div>');
		row.attr("class", "row");
		while(count <4)
		{
			if( i === infors.length)
				break;
			infor = infors[i];
			//neu la cam bien phu
			if(infor.properties.require === '0')
			{
				//tim cha
				parent = infors.filter(function (el) 
				{
					return el.properties.id === infor.properties.parent
				})[0];
				addProperty(device,row,infor, parent);
			}
			else 
			{
				//add infor
				addProperty(device,row, infor);
			}
			count ++;
			i++;
		}
		row.appendTo(deviceInfor);
		if( i === infors.length)
			break;
	}
	
//	if(device.action_status ==='1' ||device.action_status ==='2')
//	{
	if(device.status!=='0')
	{
		if(device.action_status ==='1' ||device.action_status ==='2' ||device.action_status ==='3' ||device.action_status ==='4')
		{
			infors = data.filter(function (el){
				return el.properties.m_type === '2'||el.properties.m_type === '5';
			});
			updateRailwayInfor(infors);
			$("#last-raiway").html("--");
		}
		else if(device.action_status === '0')
		{
			$("#last-raiway").html(response.last_railway.end_date);
			//alert(JSON.stringify(response.last_railway))
		}	
	}
	else
	{
		clearRailwayInfor();
	}
//	}
//	else
//		clearRailwayInfor();
}
function updateRailwayInfor(infors)
{
	var infor = infors[1];
	for(var i=0;i<infors.length;i++)
	{
		infor = infors[i];
		var strHtml = "";
		var strValue = infor.value + " " +infor.properties.symbol;
		if(infor.value < infor.properties.min_alarm ||  infor.value > infor.properties.max_alarm)
		{
			strHtml = "<p style=\"color: red\">" + strValue +"</p>";
		}
		else 
			strHtml = "<p style=\"color: green\">" + strValue +"</p>";
		if(infor.properties.code === "I1")
		{
			$('#RED1').html(strHtml);
		}
		else if(infor.properties.code === "I4")
		{
			$('#RED2').html(strHtml);
		}
		else if(infor.properties.code === "I2")
		{
			$('#RED3').html(strHtml);
		}
		else if(infor.properties.code === "I3")
		{
			$('#RED4').html(strHtml);
		}
		else if(infor.properties.code === "I5")
		{
			$('#YEL1').html(strHtml);
		}
		else if(infor.properties.code === "I6")
		{
			$('#YEL2').html(strHtml);
		}
		else if(infor.properties.code === "I7")
		{
			$('#RING1').html(strHtml);
		}
		else if(infor.properties.code === "I8")
		{
			$('#RING2').html(strHtml);
		}
		else if(infor.properties.code === "X1")
		{
			$('#CB1').html(strHtml);
		}
		else if(infor.properties.code === "X2")
		{
			$('#CB2').html(strHtml);
		}
		else if(infor.properties.code === "X3")
		{
			$('#CB3').html(strHtml);
		}
		else if(infor.properties.code === "X4")
		{
			$('#CB4').html(strHtml);
		}
		else if(infor.properties.code === "X5")
		{
			$('#CB5').html(strHtml);
		}
		else if(infor.properties.code === "X6")
		{
			$('#CB6').html(strHtml);
		}
	}
	
}
function clearRailwayInfor()
{
	$("#RED1").html("");
	$("#RED2").html("");
	$("#RED3").html("");
	$("#RED4").html("");
	$("#CB1").html("");
	$("#CB2").html("");
	$("#CB3").html("");
	$("#CB4").html("");
	$("#CB5").html("");
	$("#CB6").html("");
	$("#YEL1").html("");
	$("#YEL2").html("");
	$("#RING1").html("");
	$("#RING2").html("");
}
function addProperty(device,row, infor,parent)
{
	var column = $('<div>');
	column.attr("id",infor.id);
	column.attr("class", "col-sm-3");
	if(device.status =="0")
	{
		column.html("<p>" + infor.properties.name
				+ "</p> <p style=\"color: gray\">" + "__ " + "</p>");
	}
	else
	{
		if(infor.properties.require === '0' && parent.value !== 0)
		{
			column.html("<p>" + infor.properties.name
			+ "</p> <p style=\"color: gray\">" + "__ " + "</p>");
		}
		else
		{
			var strValue = infor.value + infor.properties.symbol;
			if (infor.properties.type == '1')
			{
				
				if (infor.value == 1)
				{
					strValue = "ON";
				}
				else if (infor.value == 0)
				{
					strValue = "OFF";
				}
					
			}
			if($.inArray(infor.properties.code, codes) > -1 && infor.value == 0)
			{
				column.html("<p>" + infor.properties.name
						+ "</p> <p style=\"color: gray\">" + "__ " + "</p>");
			}
//			else if (infor.properties.type == '1')
//			{
//				if (infor.value == 1)
//					column.html("<p>" + infor.properties.name
//							+ "</p> <p style=\"color: green\">" + "ON " + "</p>");
//				else if (infor.value == 0)
//					column.html("<p>" + infor.properties.name
//							+ "</p> <p style=\"color: red\">" + "OFF " + "</p>");
//			}
//			else if (infor.value == 0)
//			{
//				column.html("<p>" + infor.properties.name
//						+ "</p> <h5 style=\"color: red\">" + "Mất " + infor.properties.name + "</h5>");
//			}
			else if(infor.value <= infor.properties.min_alarm ||  infor.value >= infor.properties.max_alarm)
			{
				column.html("<p>" + infor.properties.name
						+ "</p> <p style=\"color: red\">" + strValue +"</p>");
			}
			else
			{
				column.html("<p>" + infor.properties.name
						+ "</p> <p style=\"color: green\">" + strValue +"</p>");
			}
		}
	}
	column.click(function(e){
		currentDeviceInforID = $(this).attr('id');
		for(var i=0;i<device_infor.length;i++)
		{
			if(device_infor[i].id.toString() == currentDeviceInforID.toString())
			{
				InforIndex = i;
				$("p#charTitle").html(device_infor[i].properties.name);
				break;
			}	
		}
		//resetChart(device_infor[InforIndex].properties.min,device_infor[InforIndex].properties.max)
		
	});
	column.appendTo(row);
}

function mycode() {
	getCurrentDeviceInfor();
	//if(device.status !=="0")
		//updateChart();
	// do some stuff...
	tid = setTimeout(mycode, updateInterval); // repeat myself
}
function abortTimer() { // to be called when you want to stop the timer
	clearTimeout(tid);
}


function getNewData(){
	data = []

	while (data.length < totalPoints) {

		var prev = data.length > 0 ? data[data.length - 1] : 50, y = 0;

		data.push(y);
	}

	// Zip the generated y values with the x values

	var res = [];
	for (var i = 0; i < data.length; ++i) {
		res.push([ i, data[i] ])
	}

	return res;
}
function updateData(value)
{
	data.splice(data.length-1,1);
	
	data.unshift(value); 
}

function getData()
{
	var res = [];
	for (var i = 0; i < data.length; ++i) {
		res.push([ i, data[i] ])
	}
	return res;
}
function getRandomData() {

	if (data.length > 0)
		data = data.slice(1);

	// Do a random walk
	
	while (data.length < totalPoints) {

		var prev = data.length > 0 ? data[data.length - 1] : 50, y = prev
				+ Math.random() * 10 - 5;

		if (y < 0) {
			y = 0;
		} else if (y > 100) {
			y = 100;
		}

		data.push(y);
	}

	// Zip the generated y values with the x values

	var res = [];
	for (var i = 0; i < data.length; ++i) {
		res.push([ i, data[i] ])
	}

	return res;
}

function resetChart(min,max)
{
	plot = $.plot("#placeholder", [ getNewData() ], {
		series: {
			shadowSize: 0	// Drawing is faster without shadows
		},
		yaxis: {
			min: min,
			max: max
		},
		xaxis: {
			show: false
		}
	});
	
}

function updateChart() {

	plot.setData([getData()]);
	// Since the axes don't change, we don't need to call plot.setupGrid()
	plot.draw();
}

function nvl(obj,strNull)
{
	if(obj)
		return obj.toString();
	else
		return strNull;
}

function onGetRailwayHistory(from_date,to_date)
{
	var csrftoken = $.cookie('csrftoken');
	
	var posting = $.post("/ajax-device-history", {
		'csrfmiddlewaretoken' : csrftoken,
		'device_id' : device_id,
		'from_date' : from_date,
		'to_date' : to_date,
	});
	posting.done(function(data) 
	{
		var tbody = $('#table7 tbody');
		tbody.empty();
		//
		var histories = data.histories;
		for(var i=0;i<histories.length;i++)
		{
			var history = histories[i];
			
			var row = $('<tr></tr>');
			//STT
			row.append($('<td>' + history.start_date + '</td>'));
			//value
			row.append($('<td>' + history.end_date + '</td>'));
			row.append($('<td>' + history.time + '</td>'));
			//value
			row.append($('<td>' + history.description + '</td>'));
			//append to body
			tbody.append(row);
		}
	});
}