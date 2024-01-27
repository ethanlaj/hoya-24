import React from "react";
import { Button, Input } from "antd";
import { SendOutlined } from "@ant-design/icons";

const ChatInput = ({ currentMessage, setCurrentMessage, handleMessageSend, isDisabled }) => {
	const handleKeyDown = (e) => {
		if (isDisabled) return;
		if (currentMessage.trim() === "") return;

		if (e.key === "Enter") {
			handleMessageSend();
		}
	};

	return (
		<div className="chat-input">
			<Input
				placeholder="Type your message here..."
				onKeyDown={handleKeyDown}
				value={currentMessage}
				onChange={(e) => setCurrentMessage(e.target.value)}
			/>
			<Button
				loading={isDisabled}
				icon={<SendOutlined />}
				type="primary"
				className="mt-2 w-full"
				onClick={handleMessageSend}
			>
				Send
			</Button>
		</div>
	);
};

export default ChatInput;
