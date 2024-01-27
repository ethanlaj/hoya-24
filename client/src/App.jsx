import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import "./App.css";
import { ChatService } from "./services/chatService";
import TypingIndicator from "./components/TypingIndicator";
import Message from "./components/Message";
import ChatHeader from "./components/ChatHeader";
import ChatToggleButton from "./components/ChatToggleButton";
import ChatInput from "./components/ChatInput";
import useInterceptor from "./hooks/useInterceptor";

function App() {
	const [isVisible, setIsVisible] = useState(false);
	const [currentMessage, setCurrentMessage] = useState("");
	const [chatId, setChatId] = useState(null);
	const [isLoading, setIsLoading] = useState(true);
	const [isIniting, setIsIniting] = useState(true);
	const [isTyping, setIsTyping] = useState(false);
	const [messages, setMessages] = useState([]);
	const chatboxRef = useRef(null);
	const [chatBoxPosition, setChatBoxPosition] = useState({ x: 0, y: 0 });

	useInterceptor(setIsIniting);

	useEffect(() => {
		async function createChat() {
			try {
				const response = await ChatService.createChat();
				localStorage.setItem("accessToken", response.access_token);
				localStorage.setItem("refreshToken", response.refresh_token);
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
				if (id) {
					setChatId(id);
					localStorage.setItem("chatId", id);
				}
			});
		}
	}, [chatId]);

	useEffect(() => {
		async function getMessages() {
			try {
				const response = await ChatService.getChat(chatId);
				setMessages(response.messages);

				if (response.messages.length === 0) {
					const botMessage = {
						sender: "bot",
						message:
							"Thanks for reaching out! I'm JayBot, an admissions AI bot, and you can ask me anything about Elizabethtown College!",
					};

					setMessages([botMessage]);
				}
			} catch (error) {
				console.log(error);
				setChatId(null);
				localStorage.removeItem("chatId");
			}
		}

		if (chatId) {
			getMessages();
			setIsLoading(false);
		}
	}, [chatId]);

	const toggleChatBox = () => {
		setIsVisible(!isVisible);
		setTimeout(() => {
			scrollToBottom();
		}, 100);
	};

	const scrollToBottom = () => {
		if (chatboxRef.current) chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
	};

	useEffect(() => {
		scrollToBottom();
	}, [messages]);

	const handleMessageSend = async () => {
		if (currentMessage.trim() === "") return;

		setCurrentMessage("");
		const currentMessages = messages;
		const mockUserMessage = {
			message: currentMessage,
			sender: "user",
			createdAt: new Date(),
		};

		setMessages((prev) => [...prev, mockUserMessage]);

		try {
			setIsTyping(true);

			const response = await ChatService.addMessage({ _id: chatId, message: currentMessage });
			const userMessage = response.user_message;
			const botMessage = response.bot_message;

			setMessages([...currentMessages, userMessage, botMessage]);
		} catch (error) {
			console.log(error);
		} finally {
			setIsTyping(false);
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

	if (isIniting) return null;

	return (
		<>
			{/* For demo purposes only */}
			<iframe
				src="https://etown.edu"
				width="100%"
				height="100%"
				className="absolute border-none"
			/>
			<div className="fixed bottom-4 right-4">
				<ChatToggleButton
					isLoading={isLoading}
					isVisible={isVisible}
					toggleChatBox={toggleChatBox}
					setChatBoxPosition={setChatBoxPosition}
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
							<ChatHeader />
							<div className="p-4 flex flex-col" style={{ height: "85%" }}>
								<div
									ref={chatboxRef}
									className="chat-window overflow-y-auto mb-2 flex-1"
								>
									{messages.map((message, index) => (
										<Message key={index} message={message} />
									))}

									{isTyping && <TypingIndicator />}
								</div>
								<ChatInput
									handleMessageSend={handleMessageSend}
									currentMessage={currentMessage}
									setCurrentMessage={setCurrentMessage}
									isDisabled={isTyping}
								/>
							</div>
						</motion.div>
					)}
				</AnimatePresence>
			</div>
		</>
	);
}

export default App;
