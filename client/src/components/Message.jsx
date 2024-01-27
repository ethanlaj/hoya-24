import React from "react";

const Message = ({ message }) => {
	return (
		<div
			className={`chat-message ${
				message.sender === "bot" ? "bg-gray-200 text-black" : "bg-blue-500 text-white"
			} p-2 rounded mb-2 flex items-center`}
			style={{
				marginLeft: message.sender === "bot" ? "0" : "auto",
				marginRight: message.sender === "bot" ? "auto" : "0",
				maxWidth: "80%",
				boxShadow: "0 2px 2px rgba(0,0,0,0.2)",
			}}
		>
			<div style={{ maxWidth: "100%" }}>{message.message}</div>
		</div>
	);
};

export default Message;
