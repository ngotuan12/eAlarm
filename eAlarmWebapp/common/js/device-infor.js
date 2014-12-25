var plot;
var data = [], totalPoints = 100;
var updateInterval = 2000;
var currentDeviceID;
var currentDeviceInforID;
var InforIndex = 0;
var device_infor;
var device;
var tid;
function onGetDeviceInfor(device_id) {
	currentDeviceID = device_id;
	var csrftoken = $.cookie('csrftoken');
	var posting = $.post("/device-infor", {
		'csrfmiddlewaretoken' : csrftoken,
		'device_id' : device_id,
	});
	posting.done(function(data) 
	{
		InforIndex = 0;
		device_infor = data.device_infor;
		device = data.device;
		resetChart(data.device_infor[InforIndex].properties.min,data.device_infor[InforIndex].properties.max);
		updateData(data.device_infor[InforIndex].value);
		currentDeviceInforID = data.device_infor[InforIndex].id;
		updateDevice();
		updateDeviceProperties(data.device_infor);
		abortTimer();
		tid = setTimeout(mycode, updateInterval);
	});
}

function getCurrentDeviceInfor()
{
	var csrftoken = $.cookie('csrftoken');
	var posting = $.post("/device-infor", {
		'csrfmiddlewaretoken' : csrftoken,
		'device_id' : currentDeviceID,
	});
	posting.done(function(data) {
		if(data.device.status!==device.status)
		{
			device = data.device;
			updateDevice();
		}
		updateDeviceProperties(data.device_infor);
		updateData(data.device_infor[InforIndex].value);
	});
}
function updateDevice()
{
	//update device name
	var deviceName = $('#device-name');
	
	deviceName.html("<a href=\"#\">"+device.code+" </a> - "+device.address);
	var deviceMac = $('#device-mac');
	deviceMac.html("MAC: "+device.mac_add);
	var deviceServer = $('#device-server');
	deviceServer.html("Connected server: "+nvl(device.connected_server,"Chưa kết nối"));
	var deviceStatus = $('#device-status');
	//device status on table
	var deviceStatusTable = $('#device-status-'+device.id);
	var deviceIssue = $('#device-issue');
	if(device.status==="1")
	{
		deviceIssue.html("");
		deviceStatus.attr("src","/images/ic_green.png");
		deviceStatusTable.attr("src","images/ic_green.png");
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
function updateDeviceProperties(infors)
{
	//update device information
	var deviceInfor = $('#device-infor');
	deviceInfor.empty();
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
}

function addProperty(device,row, infor,parent)
{
	var column = $('<div>');
	column.attr("id",infor.id);
	column.attr("class", "col-sm-3");
	if(device.status =="0")
	{
		column.html("<p>" + infor.properties.name
				+ "</p> <h4 style=\"color: gray\">" + "__ " + "</h4>");
	}
	else
	{
		if(infor.properties.require === '0' && parent.value !== 0)
		{
			column.html("<p>" + infor.properties.name
			+ "</p> <h4 style=\"color: gray\">" + "__ " + "</h4>");
		}
		else
		{
			if (infor.value == 0)
			{
				column.html("<p>" + infor.properties.name
						+ "</p> <h5 style=\"color: red\">" + "Mất " + infor.properties.name + "</h5>");
			}
			else if(infor.value < infor.properties.min_alarm ||  infor.value > infor.properties.max_alarm)
			{
				column.html("<p>" + infor.properties.name
						+ "</p> <h4 style=\"color: red\">" + infor.value + infor.properties.symbol +"</h4>");
			}
			else
			{
				column.html("<p>" + infor.properties.name
						+ "</p> <h4 style=\"color: green\">" + infor.value + infor.properties.symbol +"</h4>");
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
		resetChart(device_infor[InforIndex].properties.min,device_infor[InforIndex].properties.max)
		
	});
	column.appendTo(row);
}

function mycode() {
	getCurrentDeviceInfor();
	if(device.status !=="0")
		updateChart();
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