import React, { useState, useRef, useEffect } from "react";
import { Button, Input, Typography } from "antd";
import { MessageOutlined, ArrowDownOutlined, SendOutlined } from "@ant-design/icons";
import { motion, AnimatePresence } from "framer-motion";
import "./App.css";
import { ChatService } from "./services/chatService";

const { Text } = Typography;

function App() {
	const [isVisible, setIsVisible] = useState(false);
	const [currentMessage, setCurrentMessage] = useState("");
	const [chatId, setChatId] = useState(null);
	const [isLoading, setIsLoading] = useState(true);
	const [messages, setMessages] = useState([]);
	const chatboxRef = useRef(null);

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
		async function createChat() {
			try {
				const response = await ChatService.createChat();
				return response._id;
			} catch (error) {
				console.log(error);
			}
		}

		let currentChatId = chatId || localStorage.getItem("chatId");
		if (currentChatId) {
			setChatId(currentChatId);
		} else {
			createChat().then((id) => {
				setChatId(id);
				localStorage.setItem("chatId", id);
			});
		}
	}, [chatId]);

	useEffect(() => {
		async function getMessages() {
			try {
				const response = await ChatService.getChat(chatId);
				setMessages(response.messages);
				scrollToBottom();
			} catch (error) {
				console.log(error);
			}
		}

		if (chatId) {
			getMessages();
			setIsLoading(false);
		}
	}, [chatId]);

	const toggleChatBox = () => {
		setIsVisible(!isVisible);
	};

	const scrollToBottom = () => {
		if (chatboxRef.current) chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
	};

	const handleMessageSend = async () => {
		setCurrentMessage("");
		const currentMessages = messages;
		const mockUserMessage = {
			message: currentMessage,
			sender: "user",
			createdAt: new Date(),
		};

		setMessages((prev) => [...prev, mockUserMessage]);
		scrollToBottom();

		try {
			const response = await ChatService.addMessage({ _id: chatId, message: currentMessage });
			const userMessage = response.user_message;
			const botMessage = response.bot_message;

			setMessages([...currentMessages, userMessage, botMessage]);
			scrollToBottom();
		} catch (error) {
			console.log(error);
		}
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
						<div className="bg-gray-800" style={{ height: "60px" }}>
							<div className="text-white text-lg text-center leading-10">
								Admissions AI Chat
							</div>
						</div>
						<div className="p-4 flex flex-col" style={{ height: "90%" }}>
							<div
								ref={chatboxRef}
								className="chat-window overflow-y-auto mb-2 flex-1"
							>
								{messages.map((message, index) => (
									<div
										key={index}
										className={`chat-message ${
											message.sender === "bot"
												? "bg-gray-200 text-black"
												: "bg-blue-500 text-white"
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
