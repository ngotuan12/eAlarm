package co.vn.e_alarm.bean;

import java.io.Serializable;

public class ObjProperties implements Serializable{
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	public int idDevice;
	public int idDeviceProperties;
	public String nameProperties;
	public double valueProperties;
	public int valueMaxProperties;
	public int valueMinProperties;
	public int typeProperties;
	public String symbolProperties;
	public String codeProperties;
	public int maxValue;
	public int minValue;
	public int getIdDevice() {
		return idDevice;
	}
	public void setIdDevice(int idDevice) {
		this.idDevice = idDevice;
	}
	public int getIdDeviceProperties() {
		return idDeviceProperties;
	}
	public void setIdDeviceProperties(int idDeviceProperties) {
		this.idDeviceProperties = idDeviceProperties;
	}
	public String getNameProperties() {
		return nameProperties;
	}
	public void setNameProperties(String nameProperties) {
		this.nameProperties = nameProperties;
	}
	
	public int getTypeProperties() {
		return typeProperties;
	}
	public void setTypeProperties(int typeProperties) {
		this.typeProperties = typeProperties;
	}
	public int getValueMaxProperties() {
		return valueMaxProperties;
	}
	public void setValueMaxProperties(int valueMaxProperties) {
		this.valueMaxProperties = valueMaxProperties;
	}
	public int getValueMinProperties() {
		return valueMinProperties;
	}
	public void setValueMinProperties(int valueMinProperties) {
		this.valueMinProperties = valueMinProperties;
	}
	public double getValueProperties() {
		return valueProperties;
	}
	public void setValueProperties(double valueProperties) {
		this.valueProperties = valueProperties;
	}
	public String getSymbolProperties() {
		return symbolProperties;
	}
	public void setSymbolProperties(String symbolProperties) {
		this.symbolProperties = symbolProperties;
	}
	public String getCodeProperties()
	{
		return codeProperties;
	}
	public void setCodeProperties(String codeProperties)
	{
		this.codeProperties = codeProperties;
	}
	public int getMaxValue()
	{
		return maxValue;
	}
	public void setMaxValue(int maxValue)
	{
		this.maxValue = maxValue;
	}
	public int getMinValue()
	{
		return minValue;
	}
	public void setMinValue(int minValue)
	{
		this.minValue = minValue;
	}
	
	
}
