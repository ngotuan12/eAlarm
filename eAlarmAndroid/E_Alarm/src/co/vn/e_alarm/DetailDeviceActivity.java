package co.vn.e_alarm;

import java.util.ArrayList;
import java.util.Iterator;
import org.achartengine.GraphicalView;
import org.holoeverywhere.widget.AdapterView;
import org.holoeverywhere.widget.AdapterView.OnItemSelectedListener;
import org.holoeverywhere.widget.Spinner;
import org.holoeverywhere.widget.Toast;
import org.json.JSONException;
import org.json.JSONObject;
import com.jjoe64.graphview.GraphViewSeries;
import com.jjoe64.graphview.LineGraphView;
import com.jjoe64.graphview.GraphView.GraphViewData;
import co.vn.e_alarm.adapter.CustomGridViewAdapter;
import co.vn.e_alarm.bean.ObjAccount;
import co.vn.e_alarm.bean.ObjStation;
import co.vn.e_alarm.bean.ObjProperties;
import co.vn.e_alarm.customwiget.CustomGridView;
import co.vn.e_alarm.db.DBStation;
import co.vn.e_alarm.network.NetworkUtility;
import co.vn.e_alarm.network.RestConnector;
import co.vn.e_alarm.utils.Utils;
import de.tavendo.autobahn.WebSocket;
import de.tavendo.autobahn.WebSocketConnection;
import de.tavendo.autobahn.WebSocketConnectionHandler;
import de.tavendo.autobahn.WebSocketException;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ArrayAdapter;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

@SuppressLint("ValidFragment")
public class DetailDeviceActivity extends Activity implements
		OnItemSelectedListener, OnClickListener
{
	ImageView imgAlarm;
	String TAG = "StationFragment";
	TextView tvAlarm, tvName, tvAddress,  tvMacAddress,
			tvServerConnect,tvFullName;
	ObjStation listStation ;
	int pos = 0;
	int mPostion = 0;
	boolean check = false;
	static boolean isCheckMove = false;
	GraphicalView mChart;
	LinearLayout layoutGraph, layout_header, chartContainer, layout_properties,
			layout_statusDevices, layout_main, layout_child_properties,
			layout_call, layout_call_main, layout_email, layout_account;
	CustomGridView layoutStatus;
	static boolean isCheck = false;
	private GraphViewSeries series;
	int status = 0, type = 0;
	ImageButton imgFullChart;
	ArrayList<ObjProperties> listProperties;
	ArrayList<ObjProperties> listType1Properties;
	ArrayList<ObjProperties> listType2Properties;
	ArrayList<ObjProperties> listValueUpdate, listValueProperties;
	ArrayList<String> listNameProperties;
	ArrayList<Integer> listMinValue, listMaxValue;
	CustomGridViewAdapter customGridAdapter;
	double value = 0d, valueMin = 0d, valueMax = 0d;
	double lastValue = 0d;
	private Runnable  mTimer2, mTime3;
	private  Handler mHandler = new Handler();
	Spinner spGraph;
	LineGraphView graphView;
	ArrayList<TextView> tvProperties;
	ObjAccount objAccount;
	private WebSocket mConnection;
	@Override
	protected void onCreate(Bundle savedInstanceState)
	{
		super.onCreate(savedInstanceState);
		setContentView(R.layout.new_layout);
		connectWebSocket();
		initStation();
		spGraph.setOnItemSelectedListener(this);
		layout_call.setOnClickListener(this);
		imgFullChart.setOnClickListener(this);
		layout_call_main.setOnClickListener(this);
		layout_email.setOnClickListener(this);
		layout_account.setOnClickListener(this);
	}
	

	

	/**
	 * declare variable StationFragment
	 */
	public void initStation()
	{

		imgAlarm = (ImageView)findViewById(R.id.imgAlarm);
		layout_header = (LinearLayout) findViewById(R.id.layout_header);
		tvName = (TextView) findViewById(R.id.tvNameStation);
		tvAddress = (TextView) findViewById(R.id.tvAddress);
		//layout description
		tvMacAddress = (TextView) findViewById(R.id.tvMacAddress);
		tvServerConnect = (TextView) findViewById(R.id.tvServerConnect);
//		tvNameManager = (TextView) findViewById(R.id.tvNameManager);
		//chart
		chartContainer = (LinearLayout) findViewById(R.id.container);
		layoutGraph = (LinearLayout) findViewById(R.id.chart_container);
		layout_main = (LinearLayout) findViewById(R.id.layout_main);
		layout_call_main = (LinearLayout) findViewById(R.id.layout_call_main);
		layout_email = (LinearLayout) findViewById(R.id.layout_email);
		layout_account = (LinearLayout) findViewById(R.id.layout_account);
//		tvNameManager = (TextView) findViewById(R.id.tvNameManager);
		layout_child_properties = (LinearLayout) findViewById(R.id.layout_child_properties);
		layout_statusDevices = (LinearLayout) findViewById(R.id.layout_statusDevices);
		layout_properties = (LinearLayout) findViewById(R.id.layout_properties);
		spGraph = (Spinner) findViewById(R.id.spGraph);
		imgFullChart = (ImageButton) findViewById(R.id.imgFullChart);
		layout_call = (LinearLayout) findViewById(R.id.layout_direct);
		layoutStatus = (CustomGridView) findViewById(R.id.layoutStatus);
		listProperties = new ArrayList<ObjProperties>();
		listType1Properties = new ArrayList<ObjProperties>();
		listType2Properties = new ArrayList<ObjProperties>();
		listValueProperties = new ArrayList<ObjProperties>();
		listNameProperties = new ArrayList<String>();
		listMinValue = new ArrayList<Integer>();
		listMaxValue = new ArrayList<Integer>();
		listStation=(ObjStation) getIntent().getExtras().getSerializable("DATA");
		

		setData();
	}

	/**
	 * @author HoaiNhoi
	 * @since
	 * @modify: TuanNA Set data to layout
	 */
	public void setData()
	{
		DBStation mdb = new DBStation(this);
		objAccount = mdb.getInfoAccount();
		if (objAccount != null)
		{
//			 tvNameManager.setText(objAccount.getFullName());
		}

		if (listStation != null)
		{
			status = listStation.getStatus();
			tvMacAddress.setText("Địa Chỉ Mac: " + listStation.getMacAddress());
			tvServerConnect
					.setText("Server Connect: " + listStation.getServerConnect());
			if (status == 1)
			{
				layout_header.setBackgroundResource(R.color.green);
				layout_main.setVisibility(View.VISIBLE);
			}
			else if (status == 2)
			{
				layout_header.setBackgroundResource(R.color.red2);
				layout_main.setVisibility(View.VISIBLE);
			}
			else if (status == 3)
			{
				layout_header.setBackgroundResource(R.color.color_warning);
				layout_main.setVisibility(View.VISIBLE);
			}
			else
			{
				layout_header.setBackgroundResource(R.color.color_warning);
				layout_main.setVisibility(View.INVISIBLE);
			}
			listProperties = listStation.getListPropertiesStation();
			// update value
			tvProperties = new ArrayList<TextView>();
			updateDeviceSensor(listProperties);
			if (listProperties.size() > 0)
			{
				for (int i = 0; i < listProperties.size(); i++)
				{
					type = listProperties.get(i).getTypeProperties();
					if (type == 1)
					{
						listNameProperties.add(listProperties.get(i)
								.getNameProperties());
						listMaxValue.add(listProperties.get(i)
								.getMaxValue());
						listMinValue.add(listProperties.get(i)
								.getMinValue());
						listType1Properties.add(listProperties.get(i));
						value = listType1Properties.get(0).getValueProperties();
					}
					else
					{
						listType2Properties.add(listProperties.get(i));
					}
				}
				ArrayAdapter<String> adapterNameProperties = new ArrayAdapter<String>(
						this, R.layout.row_name_properties, listNameProperties);
				spGraph.setAdapter(adapterNameProperties);
				adapterNameProperties
						.setDropDownViewResource(R.layout.simple_spinner_dropdown_item);

				if (listType2Properties.size() > 0)
				{
					customGridAdapter = new CustomGridViewAdapter(this,
							R.layout.row_status_station, listType2Properties);
					customGridAdapter.notifyDataSetChanged();
					layoutStatus.invalidate();
					layoutStatus.setAdapter(customGridAdapter);
					layout_statusDevices.setVisibility(View.VISIBLE);
				}

			}
			if (graphView == null)
			{
				drawGraph();
			}
			tvName.setText(listStation.getCode());
			tvAddress.setText(listStation.getAddress());
		}
	}

	

	/**
	 * draw graph
	 * 
	 * @param position
	 *            : postion properties device
	 */
	public void drawGraph()
	{

		if (graphView != null)
		{
			graphView.removeSeries(series);
		}

		series = new GraphViewSeries(new GraphViewData[] {
				new GraphViewData(1, value), new GraphViewData(2, value),
				new GraphViewData(3, value), new GraphViewData(4, value)
		});

		graphView = new LineGraphView(this, "Trạng thái thiết bị");
		((LineGraphView) graphView).setDrawBackground(true);
		graphView.setManualYAxisBounds(valueMax, valueMin);
		graphView.addSeries(series); // data
		graphView.setViewPort(1, 4);
		graphView.setScalable(true);
		chartContainer.addView(graphView);
		try
		{
			mTimer2 = new Runnable()
			{
				@Override
				public void run()
				{
					lastValue += 1d;

					series.appendData(new GraphViewData(lastValue, value),
							true, 10);
					mHandler.postDelayed(this, 1000);

				}
			};
			mHandler.postDelayed(mTimer2, 1000);

		}
		catch (Exception e)
		{
			e.printStackTrace();
		}

	}

	



	private void removeThread()
	{
		lastValue = 0d;
		mHandler.removeCallbacks(mTimer2);
	}

	@Override
	public void onPause()
	{
		Log.d(TAG, "onpause");
		if (!isCheckMove)
		{
			removeThread();
		}

		super.onPause();

	}

	

	@Override
	public void onResume()
	{
		isCheckMove = false;
		super.onResume();

	}

	


	@Override
	public void onDestroy()
	{
		lastValue = 0d;
		if(mConnection!=null)
		{
			mConnection.disconnect();
			mConnection = null;
		}
		Log.d(TAG, "Destroy");
		super.onDestroy();

	}

	@Override
	public void onItemSelected(AdapterView<?> parent, View view, int position,
			long id)
	{
		value = listType1Properties.get(position).getValueProperties();
		mHandler.removeCallbacks(mTimer2);
		chartContainer.removeCallbacks(mTime3);
		mPostion = position;
		valueMin = listMinValue.get(position);
		valueMax = listMaxValue.get(position);
		if (graphView != null)
		{
			mTime3 = new Runnable()
			{

				@Override
				public void run()
				{
					lastValue = 0d;
					chartContainer.removeView(graphView);
					drawGraph();
				}
			};
			chartContainer.post(mTime3);
		}

	}

	@Override
	public void onNothingSelected(AdapterView<?> parent)
	{

	}

	/**
	 * update value properties
	 */
	public void updateSensorValue(ObjProperties property)
	{
		String strValue = property.getNameProperties() + ": "
				+ property.getValueProperties() + " "
				+ property.getSymbolProperties();
		TextView text = new TextView(this);
		text.setText("" + strValue);
		tvProperties.add(text);
		if (property.getValueProperties() > property.getValueMaxProperties()
				|| property.getValueProperties() < property
						.getValueMinProperties())
		{
			text.setTextColor(Color.RED);
		}
		else
		{
			text.setTextColor(Color.WHITE);
		}

		text.setPadding(10, 0, 0, 0);
		layout_properties.addView(text);
		layout_properties.setVisibility(View.VISIBLE);
	}

	@Override
	public void onClick(View arg0)
	{

		MainActivity.isCheckHomePress = true;
		isCheckMove = true;
		switch (arg0.getId())
		{
		case R.id.layout_call_main:
		case R.id.layout_call:
			Utils.CallManager(this, "");
			break;
		case R.id.layout_email:
			Utils.ShowSMS(this);

			break;

		
		case R.id.layout_account:
			
			 if(objAccount!=null){ Utils.ShowInfo(this,objAccount); }
			 
			

			break;

		default:
			break;
		}

	}

	private void connectWebSocket()
	{
		final String wsuri =RestConnector.IP_SOCKET;
		try
		{
			mConnection = new WebSocketConnection();
			
			mConnection.connect(wsuri, new WebSocketConnectionHandler()
			{
				@Override
				public void onOpen()
				{
					try
					{

						JSONObject jsonObject = new JSONObject();
						jsonObject.put("handle", "announce");
						jsonObject
								.put("sesion_key",NetworkUtility.SESSIONKEY);
						mConnection.sendTextMessage(jsonObject.toString());
						sendMessage();
					}
					catch (Exception e)
					{
						e.printStackTrace();
					}
				}

				@Override
				public void onTextMessage(String strResponse)
				{

					try
					{
						//Toast.makeText(DetailDeviceActivity.this, ""+strResponse, Toast.LENGTH_SHORT).show();
						Log.e(TAG, "response: " + strResponse);
						JSONObject response = new JSONObject(strResponse);
						onSocketResponse(response);
						

					}
					catch (Exception e)
					{
						e.printStackTrace();
						Toast.makeText(getBaseContext(), e.getMessage(), Toast.LENGTH_SHORT)
								.show();
					}
				}

				@Override
				public void onClose(int code, String reason)
				{
					Toast.makeText(getBaseContext(), "connect lost", Toast.LENGTH_SHORT)
							.show();
					//disconnect
					if(mConnection!=null)
					{
						mConnection.disconnect();
						mConnection = null;
					}
					//reconnect
					connectWebSocket();
				}

			});
		}
		catch (WebSocketException e)
		{

			Log.e(TAG, e.toString());
		}
	}

	private void sendMessage()
	{
		try
		{
			JSONObject jsonObject = new JSONObject();
			jsonObject.put("device_id",listStation.getId());
			jsonObject.put("handle", "connect_device");
			mConnection.sendTextMessage(jsonObject.toString());
		}
		catch (JSONException e)
		{
			e.printStackTrace();
		}
	}

	/**
	 * @author TuanNA
	 * @since 04/03/2014
	 * @version: 1.0
	 * @company: smart-connect
	 * @param:
	 * 
	 */
	private void updateDeviceSensor(ArrayList<ObjProperties> properties)
	{
		tvProperties = new ArrayList<TextView>();
		for (int i = 0; i < properties.size(); i++)
		{
			ObjProperties property = properties.get(i);
			updateSensorValue(property);
			// updateValue(i, listP)
		}
	}

	/**
	 * @author TuanNA
	 * @since 04/03/2014
	 * @version: 1.0
	 * @company: smart-connect
	 * @param:
	 * 
	 */
	private void clearSensorUIValue()
	{
		((LinearLayout) layout_properties).removeAllViews();
		layout_properties.invalidate();
		layout_properties.postInvalidate();
		layout_properties.refreshDrawableState();
		layout_properties.setVisibility(View.GONE);
	}

	/**
	 * @author TuanNA
	 * @since 04/03/2014
	 * @version: 1.0
	 * @company: smart-connect
	 * @param: response
	 */
	private void onSocketResponse(JSONObject response) throws Exception
	{
		String strHandle = response.getString("handle");
		if (strHandle.equals("update_device_properties"))
		{
			JSONObject properties = response.getJSONObject("infors");
			Iterator<?> keys = properties.keys();
			
			//update properties
			while (keys.hasNext())
			{
				String code = keys.next().toString();
				Double newValue = properties.getDouble(code);
				//update properties
				for(int i=0;i<listProperties.size();i++)
				{
					ObjProperties property = listProperties.get(i);
					if(property.getCodeProperties().equals(code))
					{
						//set value
						property.setValueProperties(newValue);
						break;
					}
				}
			}
			//clear UI
			clearSensorUIValue();
			//update UI
			updateDeviceSensor(listProperties);
			//
			value =  listProperties.get(mPostion).getValueProperties();
			
		}
	}
}
