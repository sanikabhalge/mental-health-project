import { useState, useMemo, useEffect, useCallback, useRef } from "react";
import { useMediaDevices } from "../hooks/useMediaDevices";
import { MediaDevicesContext } from "../context/MediaDevicesContext";
import { loadChatState, saveChatState } from "../utils/storage";
import { checkRiskPhrases } from "../utils/riskDetection";
import Sidebar from "../components/Sidebar";
import ChatHeader from "../components/ChatHeader";
import ChatInput from "../components/ChatInput";
import MessageBubble from "../components/MessageBubble";
import CameraView from "../components/CameraView";
import RiskAlertBanner from "../components/RiskAlertBanner";

function formatDateKey(dateStr) {
  const d = new Date(dateStr);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  d.setHours(0, 0, 0, 0);
  if (d.getTime() === today.getTime()) return "Today";
  if (d.getTime() === yesterday.getTime()) return "Yesterday";
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function getTodayISO() {
  return new Date().toISOString().slice(0, 10);
}

function Chat() {
  const mediaDevices = useMediaDevices();
  const { cameraOn, getCameraStream } = mediaDevices;

  const [chats, setChats] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [unsavedMessages, setUnsavedMessages] = useState([]);
  const [cameraViewMode, setCameraViewMode] = useState("floating");
  const [floatingPosition, setFloatingPosition] = useState({ x: 24, y: 24 });
  const [dragging, setDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [riskAlert, setRiskAlert] = useState(false);
  const [isBotTyping, setIsBotTyping] = useState(false);

  const didLoadRef = useRef(false);
  const scrollAnchorRef = useRef(null);

  useEffect(() => {
    const s = loadChatState();
    setChats(s.chats);
    setUnsavedMessages(s.unsavedMessages);
    setCurrentChatId(s.currentChatId);
    didLoadRef.current = true;
  }, []);

  useEffect(() => {
    if (!didLoadRef.current) return;
    saveChatState({ chats, unsavedMessages, currentChatId });
  }, [chats, unsavedMessages, currentChatId]);

  const cameraStream = getCameraStream();

  const handleDragStart = useCallback(
    (e) => {
      setDragOffset({
        x: e.clientX - floatingPosition.x,
        y: e.clientY - floatingPosition.y,
      });
      setDragging(true);
    },
    [floatingPosition]
  );

  useEffect(() => {
    if (!dragging) return;
    const getCoords = (e) => {
      if (e.clientX != null) return { x: e.clientX, y: e.clientY };
      const t = e.touches?.[0] ?? e.changedTouches?.[0];
      return t ? { x: t.clientX, y: t.clientY } : { x: 0, y: 0 };
    };
    const onMove = (e) => {
      const { x, y } = getCoords(e);
      setFloatingPosition({ x: x - dragOffset.x, y: y - dragOffset.y });
    };
    const onEnd = () => setDragging(false);
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onEnd);
    window.addEventListener("touchmove", onMove, { passive: true });
    window.addEventListener("touchend", onEnd);
    return () => {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onEnd);
      window.removeEventListener("touchmove", onMove);
      window.removeEventListener("touchend", onEnd);
    };
  }, [dragging, dragOffset]);

  const messages = currentChatId !== null
    ? (chats.find((c) => c.id === currentChatId)?.messages ?? [])
    : unsavedMessages;

  useEffect(() => {
    scrollAnchorRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isBotTyping]);

  const chatsByDate = useMemo(() => {
    const map = {};
    [...chats].sort((a, b) => new Date(b.date) - new Date(a.date)).forEach((chat) => {
      const key = formatDateKey(chat.date);
      if (!map[key]) map[key] = [];
      map[key].push(chat);
    });
    return map;
  }, [chats]);

  const handleNewChat = () => {
    if (unsavedMessages.length > 0) {
      const title = unsavedMessages[0]?.text?.slice(0, 36) || "New Chat";
      setChats((prev) => [
        ...prev,
        { id: Date.now(), title, date: getTodayISO(), messages: [...unsavedMessages] },
      ]);
      setUnsavedMessages([]);
    }
    setCurrentChatId(null);
    setUnsavedMessages([]);
  };

  const handleSelectChat = (id) => setCurrentChatId(id);

  const handleSend = (text) => {
    if (!text) return;
    if (checkRiskPhrases(text)) {
      setRiskAlert(true);
      console.log("ALERT TRIGGERED");
    }
    const userMsg = { id: Date.now(), sender: "user", text };
    const botMsg = { id: Date.now() + 1, sender: "bot", text: "Thanks for sharing!" };
    setIsBotTyping(true);

    if (currentChatId !== null) {
      setChats((prev) =>
        prev.map((c) =>
          c.id === currentChatId
            ? { ...c, messages: [...c.messages, userMsg] }
            : c
        )
      );
      setTimeout(() => {
        setChats((prev) =>
          prev.map((c) =>
            c.id === currentChatId
              ? { ...c, messages: [...c.messages, botMsg] }
              : c
          )
        );
        setIsBotTyping(false);
      }, 1000);
    } else {
      setUnsavedMessages((prev) => [...prev, userMsg]);
      setTimeout(() => {
        setUnsavedMessages((prev) => [...prev, botMsg]);
        setIsBotTyping(false);
      }, 1000);
    }
  };

  const toggleCameraViewMode = () => {
    setCameraViewMode((m) => (m === "floating" ? "full" : "floating"));
  };

  return (
    <MediaDevicesContext.Provider value={mediaDevices}>
      <div className="flex h-screen bg-gray-100">
        <Sidebar
          chatsByDate={chatsByDate}
          currentChatId={currentChatId}
          onNewChat={handleNewChat}
          onSelectChat={handleSelectChat}
        />
        <div className="flex-1 flex flex-col min-w-0">
          <ChatHeader />
          <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
            {cameraOn && cameraStream && (
              <CameraView
                stream={cameraStream}
                mode={cameraViewMode}
                onModeToggle={toggleCameraViewMode}
                position={floatingPosition}
                onDragStart={handleDragStart}
                onDragMove={() => {}}
                onDragEnd={() => {}}
                isDragging={dragging}
              />
            )}
            <div className={`flex-1 overflow-y-auto p-4 space-y-4 flex flex-col ${cameraOn && cameraViewMode === "full" ? "hidden" : ""}`}>
              {riskAlert && (
                <RiskAlertBanner onDismiss={() => setRiskAlert(false)} />
              )}
              {messages.map((msg) => (
                <MessageBubble key={msg.id} sender={msg.sender} text={msg.text} />
              ))}
              {isBotTyping && (
                <div className="flex justify-start">
                  <span className="text-sm text-gray-500 italic">Bot is typing…</span>
                </div>
              )}
              <div ref={scrollAnchorRef} />
            </div>
          </div>
          <ChatInput onSend={handleSend} />
        </div>
      </div>
    </MediaDevicesContext.Provider>
  );
}

export default Chat;
