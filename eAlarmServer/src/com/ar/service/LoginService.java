package com.ar.service;

import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.codehaus.jettison.json.JSONException;

import com.ar.util.Util;


public class LoginService extends HttpServlet
{

	/**
	 * 
	 */
	private static final long serialVersionUID = 7878413241889898974L;

	/**
	 * Service handler from application
	 * 
	 * @param request
	 *            with input stream is JSON string
	 * @param response
	 *            return JSON string
	 * @exception JSONException
	 * @since 18/11/2013
	 * @version 1.0
	 */
	@Override
	protected void service(HttpServletRequest request,
			HttpServletResponse response) throws ServletException, IOException
	{
		// super
		super.service(request, response);
		//
		try
		{
			// print some parameter
			System.out.println(request.getCharacterEncoding());
			System.out
					.println(request.getHeader("Access-Control-Allow-Origin"));
			// process request
			Util.processRequest(request,response);
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
		}
	}

	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws ServletException, IOException
	{
	}

	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp)
			throws ServletException, IOException
	{
	}
}
