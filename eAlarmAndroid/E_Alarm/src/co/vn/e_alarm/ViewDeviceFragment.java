package co.vn.e_alarm;

import java.util.ArrayList;
import org.holoeverywhere.LayoutInflater;
import org.holoeverywhere.app.Fragment;
import org.holoeverywhere.app.TabSwipeFragment;
import co.vn.e_alarm.adapter.ViewDeviceAdapter;
import co.vn.e_alarm.bean.ObjStation;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;

public class ViewDeviceFragment extends TabSwipeFragment {
	public static ArrayList<ObjStation> listDevice;
	String TAG = "ViewDeviceFragment";
	static ArrayList<ObjStation> listGoodDevice;
	static ArrayList<ObjStation> listBadDevice;
	static ArrayList<ObjStation> listWarningDevice;

	public static class TabFragment1 extends Fragment {

		@SuppressWarnings("unchecked")
		@Override
		public View onCreateView(LayoutInflater inflater, ViewGroup container,
				Bundle savedInstanceState) {

			ListView lv = new ListView(getSupportActivity());
			ArrayList<ObjStation> arrStation=(ArrayList<ObjStation>) getArguments().getSerializable("DATA");
			if (arrStation != null && arrStation.size() > 0) {
				ViewDeviceAdapter adapter = new ViewDeviceAdapter(
						getSupportActivity(), arrStation,getArguments().getInt("TYPE"));
				lv.setAdapter(adapter);
				adapter.notifyDataSetChanged();
				lv.invalidateViews();
			}
			
			return lv;
		}
	}

	

	public Bundle make(int i) {
		Bundle bundle = new Bundle();
		ArrayList<ObjStation> listDeviceFilter=new ArrayList<ObjStation>();
		switch (i) {
		case 1:
			listDeviceFilter=listGoodDevice;
			break;
		case 2:
			listDeviceFilter=listBadDevice;
			break;
		case 3:
			listDeviceFilter=listWarningDevice;
			break;
		default:
			return null;
		}
		
		bundle.putSerializable("DATA", listDeviceFilter);
		bundle.putInt("TYPE", i);
		return bundle;
	}

	@SuppressWarnings("unchecked")
	@Override
	public void onHandleTabs() {
		
		listDevice = (ArrayList<ObjStation>) getArguments().getSerializable(
				"ARRAY_DATA");
		FilterData();
		Log.e(TAG, "status: "+MainActivity.status);
		switch (MainActivity.status) {
		case 0:
			addTab("Mất Kết Nối ("+(listWarningDevice.size()+")"), TabFragment1.class,make(3));
			break;
		case 1:
			addTab("Tốt ("+(listGoodDevice.size()+")"), TabFragment1.class,make(1));
			
			break;
		
		case 2:
			addTab("Sự Cố ("+(listBadDevice.size()+")"), TabFragment1.class,make(2));
			break;

		default:
			addTab("Tốt("+(listGoodDevice.size()+")"), TabFragment1.class,make(1));
			addTab("Sự Cố("+(listBadDevice.size()+")"), TabFragment1.class,make(2));
			addTab("Mất Kết Nối("+(listWarningDevice.size()+")"), TabFragment1.class,make(3));
			break;
		}
		

	}
	/**
	 * filter data bad or good
	 */
	public void FilterData(){
		listGoodDevice = new ArrayList<ObjStation>();
		listBadDevice = new ArrayList<ObjStation>();
		listWarningDevice=new ArrayList<ObjStation>();
		if (listDevice != null && listDevice.size() > 0) {
			
			for (int j = 0; j < listDevice.size(); j++) {
				int status=listDevice.get(j).getStatus();
				switch (status) {
				
				case 1:
					listGoodDevice.add(listDevice.get(j));
					break;
				case 2:
					listBadDevice.add(listDevice.get(j));
					break;
				default:
					listWarningDevice.add(listDevice.get(j));
					break;
				}
				
			}
		}
	}

}
