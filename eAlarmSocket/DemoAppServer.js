/*******************************************************************************
 * DEFINE parameter
 ******************************************************************************/
var mysql = require("mysql");
var connection;
/*
 * connDB = mysql.createConnection({ host: '127.0.0.1', port: '9999', user:
 * 'root', password: '113322', database: 'alarm' });
 */
function handleDisconnect()
{
	connection = mysql.createConnection({
		host : '127.0.0.1',
		port : '9999',
		user : 'root',
		password : '113322',
		database : 'ealarm_evn'
	}); // Recreate the connection, since
	// the old one cannot be reused.

	connection.connect(function(err)
	{ // The server is either down
		if (err)
		{ // or restarting (takes a while sometimes).
			console.log('error when connecting to db:', err);
			setTimeout(handleDisconnect, 2000); // We introduce a delay before
												// attempting to reconnect,
		}// to avoid a hot loop, and to allow our node script to
		console.log('Connected to database...');
	}); // process asynchronous requests in the meantime.
	// If you're also serving http, display a 503 error.
	connection.on('error', function(err)
	{
		console.log('db error', err);
		if (err.code === 'PROTOCOL_CONNECTION_LOST')
		{ // Connection to the MySQL server is usually
			handleDisconnect(); // lost due to either server restart, or a
		} else
		{ // connnection idle timeout (the wait_timeout
			throw err; // server variable configures this)
		}
	});
}

handleDisconnect();
/*******************************************************************************
 * Export Parammeter
 ******************************************************************************/
exports.connDB = connection;
