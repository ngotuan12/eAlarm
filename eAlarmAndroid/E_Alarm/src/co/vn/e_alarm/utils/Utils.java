package co.vn.e_alarm.utils;

import java.text.Format;
import org.achartengine.GraphicalView;
import org.holoeverywhere.app.AlertDialog;
import org.holoeverywhere.widget.Toast;
import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.net.Uri;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.view.View.OnClickListener;
import android.widget.TextView;
import co.vn.e_alarm.PopupLoginActitvity;
import co.vn.e_alarm.R;
import co.vn.e_alarm.bean.ObjAccount;
import co.vn.e_alarm.db.MyPreference;

public class Utils {
	static Format formatter;
	 static GraphicalView mChart ;
	public static void SaveCitySelect(Context ctx,int city){
		MyPreference.getInstance().Initialize(ctx);
		MyPreference.getInstance().writeInteger("CITY", city);
	}
	public static void SaveDistrictSelect(Context ctx,String district){
		MyPreference.getInstance().Initialize(ctx);
		MyPreference.getInstance().writeString("DISTRICT",district);
	}
	public static void SaveNationalSelect(Context ctx,String national){
		MyPreference.getInstance().Initialize(ctx);
		MyPreference.getInstance().writeString("NATIONAL", national);
	}
	public static void SaveWoodSelect(Context ctx,String woodenleg){
		MyPreference.getInstance().Initialize(ctx);
		MyPreference.getInstance().writeString("WOODENLEG",woodenleg);
	}
	public static void SaveLanguageSelect(Context ctx,int language){
		MyPreference.getInstance().Initialize(ctx);
		MyPreference.getInstance().writeInteger("LANGUAGE",language);
	}
	
	/**
	 * Show sms
	 */
	public static void ShowSMS(Context ctx){
		try {
			/*Intent sendIntent = new Intent(Intent.ACTION_VIEW);
			sendIntent.setType("vnd.android-dir/mms-sms");
			ctx.startActivity(sendIntent);*/
			ctx.startActivity(new Intent(Intent.ACTION_VIEW, Uri.fromParts("sms", "0977955485", null)));
		} catch (Exception e) {
			Toast.makeText(ctx,
					"SMS faild, please try again later!",
					Toast.LENGTH_LONG).show();
			e.printStackTrace();
		}
	}
	/**
	 * call manager
	 */
	public static void CallManager(Context ctx,String phone){
		Intent intent = new Intent(Intent.ACTION_CALL,
				Uri.parse("tel:0977955485"));
		ctx.startActivity(intent);
	}
	/**
	 * Dialog authenticate again
	 */
	public static void DiaLogAuthenticate(final Activity ac){
		AlertDialog.Builder dialog=new AlertDialog.Builder(ac);
		dialog.setTitle("Thông Báo !");
		dialog.setMessage("Please login again !");
		dialog.setCancelable(false);
		dialog.setPositiveButton("OK",new DialogInterface.OnClickListener() {
			
			@Override
			public void onClick(DialogInterface dialog, int which) {
				Intent intent=new Intent(ac,PopupLoginActitvity.class);
				ac.startActivity(intent);
				ac.finish();
				
			}
		});
		dialog.show();
	}
	/**
	 * Dialog Show info account
	 */
	public static void ShowInfo(Context ctx,ObjAccount objAccount){
		
		final Dialog dialog = new Dialog(ctx);
		dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
		dialog.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
				WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN);
		dialog.getWindow().setBackgroundDrawable(
				new ColorDrawable(Color.TRANSPARENT));
		dialog.setContentView(R.layout.popup_info);
		android.widget.Button btnOK=(android.widget.Button) dialog.findViewById(R.id.btnOk);
		TextView tvUserName=(TextView) dialog.findViewById(R.id.tvName);
		TextView tvFullName=(TextView) dialog.findViewById(R.id.tvFullName);
		TextView tvGender=(TextView) dialog.findViewById(R.id.tvGender);
		TextView tvCreateDate=(TextView) dialog.findViewById(R.id.tvCreate_Date);
		
		if(objAccount!=null){
			tvUserName.setText(""+objAccount.getUserName());
			tvFullName.setText(""+objAccount.getFullName());
			tvCreateDate.setText(""+objAccount.getCreateDate());
			if(objAccount.getGender()==1){
				tvGender.setText("Nam");
			}
			else{
				tvGender.setText("Nữ");
			}
		}
		btnOK.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View arg0) {
				dialog.dismiss();
				
			}
		});
		
		dialog.show();
	}
}
