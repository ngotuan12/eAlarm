package co.vn.e_alarm.adapter;

import java.util.ArrayList;
import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;
import co.vn.e_alarm.R;
import co.vn.e_alarm.bean.ObjProperties;


public class CustomGridViewAdapter extends ArrayAdapter<ObjProperties> {
	Context context;
	int layoutResourceId;
	ArrayList<ObjProperties> data = new ArrayList<ObjProperties>();

	public CustomGridViewAdapter(Context context, int layoutResourceId,
			ArrayList<ObjProperties> data) {
		super(context, layoutResourceId, data);
		this.layoutResourceId = layoutResourceId;
		this.context = context;
		this.data = data;
		
		
	}
	

	@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		View row = convertView;
		RecordHolder holder = null;

		if (row == null) {
			LayoutInflater inflater = ((Activity) context).getLayoutInflater();
			row = inflater.inflate(layoutResourceId, parent, false);

			holder = new RecordHolder();
			holder.txtTitle = (TextView) row.findViewById(R.id.tvStatus);
			holder.imageItem = (ImageView) row.findViewById(R.id.imgStatus);
			row.setTag(holder);
		} else {
			holder = (RecordHolder) row.getTag();
		}

		ObjProperties item = data.get(position);
			holder.txtTitle.setText(item.getNameProperties());
			if(item.getValueProperties()==1){
				holder.imageItem.setBackgroundResource(R.drawable.ic_green);
			}
			else{
				holder.imageItem.setBackgroundResource(R.drawable.ic_red);
			}
				
			
		
		return row;

	}

	static class RecordHolder {
		TextView txtTitle;
		ImageView imageItem;

	}
}