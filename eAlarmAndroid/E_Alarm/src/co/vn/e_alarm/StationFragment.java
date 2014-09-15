package co.vn.e_alarm;

import java.util.ArrayList;
import java.util.Iterator;
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
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

@SuppressLint("ValidFragment")
public class StationFragment extends Fragment implements
		OnItemSelectedListener, OnClickListener
{
	ImageView imgAlarm;
	String TAG = "StationFragment";
	TextView tvAlarm, tvName, tvAddress,  tvMacAddress,
			tvServerConnect;
	static ArrayList<ObjStation> listStation = new ArrayList<ObjStation>();
	ObjStation obj;
	int pos = 0;
	int mPostion = 0;
	View mView;
	boolean check = false;
	static boolean isCheckMove = false;
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
	Activity ac;
	ObjAccount objAccount;
	private WebSocket mConnection = new WebSocketConnection();

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState)
	{
		connectWebSocket();
		View view = inflater.inflate(R.layout.new_layout, null);
		mView = view;
		initStation();
		spGraph.setOnItemSelectedListener(this);
		layout_call.setOnClickListener(this);
		imgFullChart.setOnClickListener(this);
		layout_call_main.setOnClickListener(this);
		layout_email.setOnClickListener(this);
		layout_account.setOnClickListener(this);
		return view;
	}

	/**
	 * set data station
	 * 
	 * @param objStation
	 */
	public static void setStationFragment(ArrayList<ObjStation> objStation)
	{

		listStation = objStation;
	}

	/**
	 * declare variable StationFragment
	 */
	public void initStation()
	{
		imgAlarm = (ImageView) mView.findViewById(R.id.imgAlarm);
		layout_header = (LinearLayout) mView.findViewById(R.id.layout_header);
		tvName = (TextView) mView.findViewById(R.id.tvNameStation);
		tvAddress = (TextView) mView.findViewById(R.id.tvAddress);
		tvMacAddress = (TextView) mView.findViewById(R.id.tvMacAddress);
		tvServerConnect = (TextView) mView.findViewById(R.id.tvServerConnect);
		chartContainer = (LinearLayout) mView.findViewById(R.id.container);
		layoutGraph = (LinearLayout) mView.findViewById(R.id.chart_container);
		layout_main = (LinearLayout) mView.findViewById(R.id.layout_main);
		layout_call_main = (LinearLayout) mView
				.findViewById(R.id.layout_call_main);
		layout_email = (LinearLayout) mView.findViewById(R.id.layout_email);
		layout_account = (LinearLayout) mView.findViewById(R.id.layout_account);
//		tvNameManager = (TextView) mView.findViewById(R.id.tvNameManager);
		layout_child_properties = (LinearLayout) mView
				.findViewById(R.id.layout_child_properties);
		layout_statusDevices = (LinearLayout) mView
				.findViewById(R.id.layout_statusDevices);
		layout_properties = (LinearLayout) mView
				.findViewById(R.id.layout_properties);
		spGraph = (Spinner) mView.findViewById(R.id.spGraph);
		imgFullChart = (ImageButton) mView.findViewById(R.id.imgFullChart);
		layout_call = (LinearLayout) mView.findViewById(R.id.layout_direct);
		layoutStatus = (CustomGridView) mView.findViewById(R.id.layoutStatus);
		listProperties = new ArrayList<ObjProperties>();
		listType1Properties = new ArrayList<ObjProperties>();
		listType2Properties = new ArrayList<ObjProperties>();
		listValueProperties = new ArrayList<ObjProperties>();
		listNameProperties = new ArrayList<String>();
		listMinValue = new ArrayList<Integer>();
		listMaxValue = new ArrayList<Integer>();
		if (isCheck)
		{
			pos = getArguments().getInt("POSITION");
		}
		if (listStation.size() > 0)
		{
			obj = listStation.get(pos);

		}

		setData();
	}

	/**
	 * @author HoaiNhoi
	 * @since
	 * @modify: TuanNA Set data to layout
	 */
	public void setData()
	{
		DBStation mdb = new DBStation(ac);
		objAccount = mdb.getInfoAccount();
		if (objAccount != null)
		{
			// tvNameManager.setText(objAccount.getFullName());
		}

		if (obj != null)
		{
			status = obj.getStatus();
			tvMacAddress.setText("Địa Chỉ Mac: " + obj.getMacAddress());
			tvServerConnect
					.setText("Server Connect: " + obj.getServerConnect());
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
			listProperties = obj.getListPropertiesStation();
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
						ac, R.layout.row_name_properties, listNameProperties);
				spGraph.setAdapter(adapterNameProperties);
				adapterNameProperties
						.setDropDownViewResource(R.layout.simple_spinner_dropdown_item);

				if (listType2Properties.size() > 0)
				{
					customGridAdapter = new CustomGridViewAdapter(ac,
							R.layout.row_status_station, listType2Properties);
					customGridAdapter.notifyDataSetChanged();
					layoutStatus.invalidate();
					layoutStatus.setAdapter(customGridAdapter);
					layout_statusDevices.setVisibility(View.VISIBLE);
				}

			}
			/*if (graphView == null)
			{
				drawGraph();
			}*/
			tvName.setText(obj.getCode());
			tvAddress.setText(obj.getAddress());

		}
	}

	/**
	 * Called when the fragment is first created.
	 * 
	 * @param po
	 *            : position current
	 * @return
	 */
	public static Fragment newInstance(int po)
	{
		StationFragment f = new StationFragment();
		Bundle b = new Bundle();
		b.putInt("POSITION", po);
		isCheck = true;

		f.setArguments(b);
		return f;
	}

	/**
	 * draw graph
	 * 
	 * @param position
	 *            : postion properties device
	 */
	public void drawGraph()
	{
		Log.e(TAG, "value: "+lastValue);
		value =  listProperties.get(mPostion).getValueProperties();
		if (graphView != null)
		{
			graphView.removeSeries(series);
		}

		series = new GraphViewSeries(new GraphViewData[] {
				new GraphViewData(1, value), new GraphViewData(2, value),
				new GraphViewData(3, value), new GraphViewData(4, value)
		});

		graphView = new LineGraphView(ac, "Trạng thái thiết bị");
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
					 graphView.redrawAll();
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
		

		super.onPause();
		Log.e(TAG, "onpause");
		if (!isCheckMove)
		{
			removeThread();
		}

	}

	

	@Override
	public void onResume()
	{
		isCheckMove = false;
		super.onResume();
	

	}

	@Override
	public void onAttach(Activity activity)
	{
		super.onAttach(activity);
		ac = activity;
	}

	@Override
	public void onDetach()
	{
		lastValue = 0;
		Log.d(TAG, "onDetach");

		super.onDetach();
	}

	@Override
	public void onDestroyView()
	{
		Log.e(TAG, "Destroyview");
		// removeThread();
		super.onDestroyView();

	}

	@Override
	public void onDestroy()
	{
		lastValue = 0d;
		Log.d(TAG, "Destroy");
		if(mConnection!=null)
		{
			mConnection.disconnect();
			mConnection = null;
		}
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
		/*if (graphView != null)
		{*/
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
		//}

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
		TextView text = new TextView(ac);
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
			Utils.CallManager(ac, "");
			break;
		case R.id.layout_email:
			Utils.ShowSMS(ac);

			break;

		
		case R.id.layout_account:
		
			 if(objAccount!=null){ 
				 Utils.ShowInfo(ac, objAccount);
				 }
			 
			

			break;

		default:
			break;
		}

	}
/**
 * Connect client-server by socket
 */
	private void connectWebSocket()
	{
		final String wsuri =RestConnector.IP_SOCKET;
		try
		{
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
						//connect device
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
						//Toast.makeText(ac, ""+strResponse, Toast.LENGTH_SHORT).show();
						Log.e(TAG, "response: " + strResponse);
						JSONObject response = new JSONObject(strResponse);
						onSocketResponse(response);

					}
					catch (Exception e)
					{
						e.printStackTrace();
						Toast.makeText(ac, e.getMessage(), Toast.LENGTH_SHORT)
								.show();
					}
				}

				@Override
				public void onClose(int code, String reason)
				{
					Toast.makeText(ac, "connect lost", Toast.LENGTH_SHORT)
							.show();
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
		 if (mConnection.isConnected()) 
			 try
			{
				JSONObject jsonObject = new JSONObject();
				jsonObject.put("device_id",""+ obj.getId());
				jsonObject.put("handle", "connect_device");
				//Log.e(TAG, "connect: "+obj.getId());
				mConnection.sendTextMessage(jsonObject.toString());
			}
			catch (JSONException e)
			{
				e.printStackTrace();
			}
	    else {
	       connectWebSocket();
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
			
			
		}
	}
}
