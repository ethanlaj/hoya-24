import React, { useState, useRef, useEffect } from "react";
import { Button, Input } from "antd";
import { MessageOutlined, ArrowDownOutlined, SendOutlined } from "@ant-design/icons";
import { motion, AnimatePresence } from "framer-motion";
import "./App.css";

function App() {
	const [isVisible, setIsVisible] = useState(false);
	const [currentMessage, setCurrentMessage] = useState("");
	const [chatBoxPosition, setChatBoxPosition] = useState({ x: 0, y: 0 });
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

	const toggleChatBox = () => {
		setIsVisible(!isVisible);
	};

	const handleMessageSend = () => {
		// Send message to server
		setCurrentMessage("");
		console.log(currentMessage);
	};

	const handleKeyDown = (e) => {
		if (e.key === "Enter") {
			handleMessageSend();
		}
	};

	const chatBoxVariants = {
		hidden: {
			opacity: 0,
			scale: 0.3,
			x: chatBoxPosition.x,
			y: chatBoxPosition.y,
		},
		visible: {
			opacity: 1,
			scale: 1,
			x: 0,
			y: 0,
		},
	};

	return (
		<div className="App fixed bottom-4 right-4">
			<Button
				ref={buttonRef}
				type="primary"
				shape="circle"
				style={{ width: "50px", height: "50px" }}
				icon={isVisible ? <ArrowDownOutlined /> : <MessageOutlined />}
				onClick={toggleChatBox}
				className="text-xl z-20 chat-btn"
			/>

			<AnimatePresence>
				{isVisible && (
					<motion.div
						initial="hidden"
						animate="visible"
						exit="hidden"
						variants={chatBoxVariants}
						transition={{ type: "spring", stiffness: 260, damping: 20 }}
						style={{ bottom: "60px" }}
						className="chat-box bg-white shadow-lg rounded p-4 absolute right-0 w-64 h-96 z-10 flex flex-col justify-between"
					>
						<div className="chat-window overflow-y-auto mb-2" style={{ height: "75%" }}>
							{/* Chat messages will go here */}
						</div>
						<div className="chat-input">
							<Input
								placeholder="Type your message here..."
								onKeyDown={handleKeyDown}
								value={currentMessage}
								onChange={(e) => setCurrentMessage(e.target.value)}
							/>
							<Button
								icon={<SendOutlined />}
								type="primary"
								className="mt-2 w-full"
								onClick={handleMessageSend}
							>
								Send
							</Button>
						</div>
					</motion.div>
				)}
			</AnimatePresence>
		</div>
	);
}

export default App;
