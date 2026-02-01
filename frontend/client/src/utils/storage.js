const STORAGE_KEYS = {
  chats: "mindcare_chats",
  unsaved: "mindcare_unsaved",
  currentId: "mindcare_current_chat_id",
};

export function loadChatState() {
  try {
    const chatsRaw = localStorage.getItem(STORAGE_KEYS.chats);
    const unsavedRaw = localStorage.getItem(STORAGE_KEYS.unsaved);
    const currentIdRaw = localStorage.getItem(STORAGE_KEYS.currentId);
    const chats = chatsRaw ? JSON.parse(chatsRaw) : [];
    const unsaved = unsavedRaw ? JSON.parse(unsavedRaw) : [];
    const currentId = currentIdRaw !== null ? JSON.parse(currentIdRaw) : null;
    return { chats, unsavedMessages: unsaved, currentChatId: currentId };
  } catch {
    return { chats: [], unsavedMessages: [], currentChatId: null };
  }
}

export function saveChatState({ chats, unsavedMessages, currentChatId }) {
  try {
    localStorage.setItem(STORAGE_KEYS.chats, JSON.stringify(chats));
    localStorage.setItem(STORAGE_KEYS.unsaved, JSON.stringify(unsavedMessages));
    localStorage.setItem(STORAGE_KEYS.currentId, JSON.stringify(currentChatId));
  } catch (e) {
    console.warn("Failed to save chat state:", e);
  }
}
