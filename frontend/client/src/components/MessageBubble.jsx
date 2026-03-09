function MessageBubble({ sender, text, emotion, confidence, mode }) {
  const isUser = sender === "user";
  
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} flex-col`}>
      <div
        className={`max-w-xs px-4 py-2 rounded-xl ${
          isUser ? "bg-purple-600 text-white" : "bg-gray-200 text-gray-800"
        }`}
      >
        {text}
      </div>
      
      {/* Display emotion detection info for bot messages */}
      {!isUser && emotion && (
        <div className="mt-1 text-xs text-gray-500 px-2">
          <span className="inline-block">
            😊 Emotion: <strong>{emotion}</strong> ({confidence?.toFixed(1)}%)
          </span>
          {mode && (
            <span className="ml-2 inline-block text-gray-400">
              [{mode}]
            </span>
          )}
        </div>
      )}
    </div>
  );
}

export default MessageBubble;
