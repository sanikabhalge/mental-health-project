import { useState } from "react";

const DATE_ORDER = ["Today", "Yesterday"];

function Sidebar({ chatsByDate = {}, currentChatId, onNewChat, onSelectChat }) {
  const [open, setOpen] = useState(true);

  const dateKeys = Object.keys(chatsByDate).filter((k) => chatsByDate[k]?.length > 0);
  const orderedKeys = ["Today", "Yesterday", ...dateKeys.filter((k) => !["Today", "Yesterday"].includes(k))].filter(
    (k) => chatsByDate[k]?.length > 0
  );

  return (
    <aside
      className={`flex flex-col bg-white/95 backdrop-blur border-r border-gray-200/80 shadow-xl transition-all duration-300 overflow-hidden ${
        open ? "w-64" : "w-14"
      }`}
    >
      <div className={`flex items-center min-h-[52px] border-b border-gray-100 ${open ? "justify-between px-3" : "justify-center px-1 flex-col gap-1 py-2"}`}>
        {open ? (
          <>
            <button
              onClick={onNewChat}
              className="flex items-center gap-2 flex-1 my-2 py-2.5 px-3 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white text-sm font-medium hover:from-indigo-700 hover:to-violet-700 shadow-md hover:shadow transition-all"
            >
              <span className="text-lg">+</span>
              New Chat
            </button>
            <button
              type="button"
              onClick={() => setOpen(!open)}
              className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors"
              aria-label="Close sidebar"
            >
              ◀
            </button>
          </>
        ) : (
          <>
            <button
              onClick={onNewChat}
              className="p-2 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white hover:from-indigo-700 hover:to-violet-700 shadow transition-colors"
              aria-label="New chat"
            >
              +
            </button>
            <button
              type="button"
              onClick={() => setOpen(!open)}
              className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors"
              aria-label="Open sidebar"
            >
              ▶
            </button>
          </>
        )}
      </div>

      {open && (
        <nav className="flex-1 overflow-y-auto py-3 px-2">
          {orderedKeys.map((dateKey) => {
            const list = chatsByDate[dateKey];
            if (!list || list.length === 0) return null;
            return (
              <div key={dateKey} className="mb-4">
                <div className="px-2 py-1 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  {dateKey}
                </div>
                <ul className="space-y-0.5">
                  {list.map((chat) => (
                    <li key={chat.id}>
                      <button
                        type="button"
                        onClick={() => onSelectChat(chat.id)}
                        className={`w-full text-left px-3 py-2.5 rounded-lg text-sm transition-colors truncate ${
                          currentChatId === chat.id
                            ? "bg-indigo-50 text-indigo-700 font-medium"
                            : "text-gray-700 hover:bg-gray-100"
                        }`}
                      >
                        {chat.title || "New Chat"}
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            );
          })}
          {Object.keys(chatsByDate).length === 0 && (
            <p className="px-3 py-2 text-sm text-gray-400">No chat history yet.</p>
          )}
        </nav>
      )}
    </aside>
  );
}

export default Sidebar;
