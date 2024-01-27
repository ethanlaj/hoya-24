import React, { useRef, useEffect } from "react";
import { MessageOutlined, ArrowDownOutlined } from "@ant-design/icons";
import { Button } from "antd";

const ChatToggleButton = ({ isLoading, isVisible, toggleChatBox, setChatBoxPosition }) => {
	const buttonRef = useRef(null);

	useEffect(() => {
		if (buttonRef.current) {
			const rect = buttonRef.current.getBoundingClientRect();
			setChatBoxPosition({
				x: rect.left + window.scrollX,
				y: rect.top + window.scrollY,
			});
		}
	}, [isVisible]);

	return (
		<Button
			ref={buttonRef}
			type="primary"
			loading={isLoading}
			disabled={isLoading}
			shape="circle"
			style={{ width: "50px", height: "50px" }}
			icon={isVisible ? <ArrowDownOutlined /> : <MessageOutlined />}
			onClick={toggleChatBox}
			className="text-xl z-20 chat-btn"
		/>
	);
};

export default ChatToggleButton;
