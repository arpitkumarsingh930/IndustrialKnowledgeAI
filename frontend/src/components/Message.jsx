function Message({ sender, text }) {
    const isUser = sender === "user";

    return (
        <div
            className={`flex mb-4 ${
                isUser ? "justify-end" : "justify-start"
            }`}
        >
            <div
                className={`max-w-[75%] px-4 py-3 rounded-xl whitespace-pre-wrap ${
                    isUser
                        ? "bg-cyan-500 text-white"
                        : "bg-slate-700 text-gray-100"
                }`}
            >
                {text}
            </div>
        </div>
    );
}

export default Message;