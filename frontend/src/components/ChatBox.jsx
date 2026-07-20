import { useState } from "react";
import api from "../services/api";
import Message from "./Message";
import Loader from "./Loader";

function ChatBox() {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    const sendQuestion = async () => {
        if (!question.trim()) return;

        const userMessage = {
            sender: "user",
            text: question,
        };

        setMessages((prev) => [...prev, userMessage]);
        setLoading(true);

        try {
            const response = await api.post("/ask", {
                question: question,
            });

            const aiMessage = {
                sender: "ai",
                text: response.data.answer,
            };

            setMessages((prev) => [...prev, aiMessage]);
        } catch (err) {
            setMessages((prev) => [
                ...prev,
                {
                    sender: "ai",
                    text: "Something went wrong.",
                },
            ]);
        }

        setLoading(false);
        setQuestion("");
    };

    return (
        <div className="bg-slate-900 rounded-xl p-6 h-[80vh] flex flex-col">

            <h2 className="text-xl font-semibold mb-4">
                Ask Questions
            </h2>

            <div className="flex-1 overflow-y-auto mb-4">

                {messages.map((msg, index) => (
                    <Message
                        key={index}
                        sender={msg.sender}
                        text={msg.text}
                    />
                ))}

                {loading && <Loader />}

            </div>

            <div className="flex gap-2">

                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            sendQuestion();
                        }
                    }}
                    placeholder="Ask anything..."
                    className="flex-1 p-3 rounded-lg bg-slate-800 text-white border border-slate-700"
                />

                <button
                    onClick={sendQuestion}
                    className="bg-cyan-500 hover:bg-cyan-600 px-5 rounded-lg text-white"
                >
                    Send
                </button>

            </div>

        </div>
    );
}

export default ChatBox;