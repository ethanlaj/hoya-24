import React, { useState, useRef, useEffect } from "react";
import { Button, Input, Typography } from "antd";
import { MessageOutlined, ArrowDownOutlined, SendOutlined } from "@ant-design/icons";
import { motion, AnimatePresence } from "framer-motion";
import "./App.css";
import { ConversationService } from "./services/conversationService";

const { Text } = Typography;

function App() {
	const [isVisible, setIsVisible] = useState(false);
	const [currentMessage, setCurrentMessage] = useState("");
	const [conversationId, setConversationId] = useState(null);
	const [chats, _setChats] = useState([
		{
			id: "1",
			message: "Hello",
			sender: "user",
			createdAt: "2021-08-01T00:00:00.000Z",
		},
		{
			id: "2",
			message: "Hi",
			sender: "bot",
			createdAt: "2021-08-01T00:00:00.000Z",
			link: "https://www.google.com",
		},
		{
			id: "3",
			message: "Hello",
			sender: "user",
			createdAt: "2021-08-01T00:00:00.000Z",
		},
		{
			id: "4",
			message: "Hi",
			sender: "bot",
			createdAt: "2021-08-01T00:00:00.000Z",
			link: "https://www.google.com",
		},
		{
			id: "5",
			message: "Hello",
			sender: "user",
			createdAt: "2021-08-01T00:00:00.000Z",
		},
		{
			id: "6",
			message: "Hi",
			sender: "bot",
			createdAt: "2021-08-01T00:00:00.000Z",
			link: "https://www.google.com",
		},
		{
			id: "7",
			message: "Hello",
			sender: "user",
			createdAt: "2021-08-01T00:00:00.000Z",
		},
		{
			id: "8",
			message: "Hi",
			sender: "bot",
			createdAt: "2021-08-01T00:00:00.000Z",
			link: "https://www.google.com",
		},
		{
			id: "9",
			message: "Hello",
			sender: "user",
			createdAt: "2021-08-01T00:00:00.000Z",
		},
		{
			id: "10",
			message: "Hi",
			sender: "bot",
			createdAt: "2021-08-01T00:00:00.000Z",
			link: "https://www.google.com",
		},
		{
			id: "11",
			message: "Hello",
			sender: "user",
			createdAt: "2021-08-01T00:00:00.000Z",
		},
		{
			id: "12",
			message: "Hi",
			sender: "bot",
			createdAt: "2021-08-01T00:00:00.000Z",
			link: "https://www.google.com",
		},
	]);

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

	useEffect(() => {
		async function createConversation() {
			try {
				const response = await ConversationService.createConversation();
				setConversationId(response.data.conversationId);
			} catch (error) {
				console.log(error);
			}
		}

		let currentConversationId = conversationId || localStorage.getItem("conversationId");
		if (currentConversationId) {
			setConversationId(currentConversationId);
		}
	}, [conversationId]);

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
		<div className="fixed bottom-4 right-4">
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
						style={{ bottom: "60px", height: "500px" }}
						className="chat-box bg-white shadow-lg rounded absolute right-0 w-96 z-10 flex flex-col justify-between"
					>
						<div className="bg-gray-800" style={{ height: "50px" }}>
							<Text className="text-white text-center">Admissions AI Chat</Text>
						</div>
						<div className="p-4 flex flex-col" style={{ height: "90%" }}>
							<div className="chat-window overflow-y-auto mb-2 flex-1">
								{chats.map((chat) => (
									<div
										key={chat.id}
										className={`chat-message ${
											chat.sender === "user"
												? "bg-gray-200"
												: "bg-blue-500 text-white"
										} p-2 rounded mb-2`}
									>
										{chat.message}
									</div>
								))}
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
						</div>
					</motion.div>
				)}
			</AnimatePresence>
		</div>
	);
}

export default App;
