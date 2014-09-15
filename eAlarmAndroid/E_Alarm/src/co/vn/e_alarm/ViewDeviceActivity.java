package co.vn.e_alarm;

import java.util.ArrayList;
import org.holoeverywhere.app.Activity;
import org.holoeverywhere.app.TabSwipeFragment;
import co.vn.e_alarm.bean.ObjStation;
import android.os.Bundle;
import android.support.v4.app.FragmentManager;

public class ViewDeviceActivity extends Activity {
	ArrayList<ObjStation> listDevice;
	int status=0;
	public static Activity activity;

	@SuppressWarnings("unchecked")
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onCreate(savedInstanceState);
		activity=this;
		setContentView(R.layout.activity_view_device);
		hideBar();
		listDevice = (ArrayList<ObjStation>) getIntent().getExtras()
				.getSerializable("ARRAY_OBJECT");
		TabSwipeFragment fragment = new ViewDeviceFragment();
		Bundle bundle = new Bundle();
		bundle.putSerializable("ARRAY_DATA", listDevice);
		fragment.setArguments(bundle);
		FragmentManager fm = getSupportFragmentManager();
		fm.beginTransaction().replace(R.id.layout_view, fragment).commit();
	}
	public  void hideBar(){
		getSupportActionBar().setDisplayShowTitleEnabled(false);
		getSupportActionBar().setDisplayShowHomeEnabled(false);
	}
}
