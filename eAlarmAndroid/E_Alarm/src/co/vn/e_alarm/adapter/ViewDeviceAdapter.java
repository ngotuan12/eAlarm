package co.vn.e_alarm.adapter;

import java.util.ArrayList;
import org.achartengine.GraphicalView;
import co.vn.e_alarm.DetailDeviceActivity;
import co.vn.e_alarm.R;
import co.vn.e_alarm.bean.ObjProperties;
import co.vn.e_alarm.bean.ObjStation;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.BaseAdapter;
import android.widget.LinearLayout;
import android.widget.TextView;

public class ViewDeviceAdapter extends BaseAdapter {
	Context context;
	 ArrayList<ObjStation> arrStation;
	LayoutInflater inflater;
	GraphicalView mChart;
	ArrayList<ObjProperties> listProperties;
	int mType;

	public ViewDeviceAdapter(Context ctx, ArrayList<ObjStation> listStation,int type) {
		this.context = ctx;
		arrStation = listStation;
		inflater = (LayoutInflater) context
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		listProperties = new ArrayList<ObjProperties>();
	}

	@Override
	public int getCount() {
		// TODO Auto-generated method stub
		return arrStation.size();
	}

	@Override
	public Object getItem(int arg0) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public long getItemId(int arg0) {
		// TODO Auto-generated method stub
		return arg0;
	}

	@Override
	public View getView(int position, View v, ViewGroup arg2) {
		View view = v;
		final ObjStation obj = arrStation.get(position);
		ViewHolder holder;
		if (view == null) {
			view = inflater.inflate(R.layout.row_view_device, null);
			holder = new ViewHolder();
			holder.tvNameStation = (TextView) view
					.findViewById(R.id.tvNameStation);
			holder.tvAddress = (TextView) view.findViewById(R.id.tvAddress);
			holder.layout_call=(LinearLayout) view.findViewById(R.id.layout_call);
			view.setTag(holder);
		} else {
			holder = (ViewHolder) view.getTag();
		}
		mType=obj.getStatus();
		if (mType == 1) {
			view.setBackgroundColor(context.getResources().getColor(R.color.green));
		} else if(mType==2) {
			view.setBackgroundColor(context.getResources().getColor(R.color.red2));
		}
		else if(mType==3){
			view.setBackgroundColor(context.getResources().getColor(R.color.color_warning));
		}
		else{
			view.setBackgroundColor(context.getResources().getColor(R.color.color_warning));
		}
		
		
		holder.tvNameStation.setText("" + obj.getCode());
		holder.tvAddress.setText("" + obj.getAddress());
		view.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {

				Intent i=new Intent(context,DetailDeviceActivity.class);
				Bundle bundle = new Bundle();
				bundle.putSerializable("DATA", obj);
				i.putExtras(bundle);
				context.startActivity(i);

			}
		});
		holder.layout_call.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View arg0) {
				Intent intent = new Intent(Intent.ACTION_CALL, Uri.parse("tel:0977955485"));
				context.startActivity(intent);
				
			}
		});
		return view;
	}

	

	class ViewHolder {
		TextView tvNameStation, tvAddress;
		LinearLayout layout_call;
	}
}
