import React from "react";
import { motion } from "framer-motion";

const TypingIndicator = () => {
	return (
		<motion.div
			initial={{ opacity: 0 }}
			animate={{ opacity: 1 }}
			exit={{ opacity: 0 }}
			transition={{ duration: 0.5 }}
			className="chat-message bg-gray-200 text-black p-2 rounded mb-2 flex items-center"
			style={{
				marginLeft: "0",
				marginRight: "auto",
				maxWidth: "80%",
				boxShadow: "0 2px 2px rgba(0,0,0,0.2)",
			}}
		>
			<div style={{ maxWidth: "100%" }}>
				<div className="typing-indicator">
					<span></span>
					<span></span>
					<span></span>
				</div>
			</div>
		</motion.div>
	);
};

export default TypingIndicator;
