# ==============================================================================
# DoubleHelix Neural Agent Engine (DoubleHelix.Go Edition)
# Real-Time Agent IPC Bridge (TCP Socket on Port 9250)
# Cosmic Souls of Sovereignty Inc. • arkade.new-world-arkitech.dev
# ==============================================================================
@tool
extends Node

const DEFAULT_PORT: int = 9250

var tcp_server: TCPServer
var clients: Array[StreamPeerTCP] = []

func _ready() -> void:
	start_server()

func start_server(port: int = DEFAULT_PORT) -> void:
	tcp_server = TCPServer.new()
	var err = tcp_server.listen(port, "127.0.0.1")
	if err == OK:
		print("[DoubleHelix AgentBridge] Listening on 127.0.0.1:" + str(port))
	else:
		print("[DoubleHelix AgentBridge] Warning: Could not bind port " + str(port))

func _process(_delta: float) -> void:
	if not tcp_server or not tcp_server.is_listening():
		return

	# Accept incoming connections
	if tcp_server.is_connection_available():
		var peer = tcp_server.take_connection()
		if peer:
			clients.append(peer)

	# Process client messages
	var to_remove = []
	for client in clients:
		if client.get_status() == StreamPeerTCP.STATUS_CONNECTED:
			var bytes_avail = client.get_available_bytes()
			if bytes_avail > 0:
				var raw = client.get_utf8_string(bytes_avail)
				for line in raw.split("\n"):
					line = line.strip_edges()
					if line != "":
						var response = process_agent_message(line)
						client.put_utf8_string(JSON.stringify(response) + "\n")
		elif client.get_status() != StreamPeerTCP.STATUS_CONNECTING:
			to_remove.append(client)

	for rem in to_remove:
		clients.erase(rem)

func process_agent_message(json_str: String) -> Dictionary:
	var parsed = JSON.parse_string(json_str)
	if not parsed is Dictionary:
		return {"error": "Invalid JSON format"}

	var cmd = parsed.get("command", "")
	var params = parsed.get("params", {})

	match cmd:
		"ping":
			return {"status": "PONG", "time": Time.get_unix_time_from_system()}
		"status":
			return {
				"status": "ONLINE",
				"engine": "DoubleHelix.Go 2.4",
				"domain": "arkade.new-world-arkitech.dev",
				"clients_connected": clients.size()
			}
		_:
			return {"error": "Unknown bridge command: " + cmd}

func _exit_tree() -> void:
	if tcp_server:
		tcp_server.stop()
