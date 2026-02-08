//
// Chat Popup Persistence
//
document.addEventListener("DOMContentLoaded", function () {
  const dock = document.getElementById("chat_dock");
  if (!dock) return;

  const STORAGE_KEY = "grouper_open_chats";

  function getOpenRooms() {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch (e) {
      console.warn("Failed to parse chat storage", e);
      return [];
    }
  }

  function saveOpenRooms(rooms) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...new Set(rooms)]));
  }

  const roomsToRestore = getOpenRooms();
  roomsToRestore.forEach((roomId) => {
    if (!document.getElementById(`messages_room_${roomId}`)) {
      htmx.ajax("GET", `/chat/room/${roomId}`, {
        target: "#chat_dock",
        swap: "beforeend",
        headers: { "HX-Target": "chat_dock" }
      });
    }
  });

  // Observe the dock for changes
  const observer = new MutationObserver((mutations) => {
    let rooms = getOpenRooms();
    let changed = false;

    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === 1 && node.id && node.id.startsWith("messages_room_")) {
          const id = node.id.replace("messages_room_", "");
          if (!rooms.includes(id)) {
            rooms.push(id);
            changed = true;
          }
        }
      });

      mutation.removedNodes.forEach((node) => {
        if (node.nodeType === 1 && node.id && node.id.startsWith("messages_room_")) {
          const id = node.id.replace("messages_room_", "");
          rooms = rooms.filter((r) => r !== id);
          changed = true;
        }
      });
    });

    if (changed) {
      saveOpenRooms(rooms);
    }
  });

  observer.observe(dock, { childList: true });
});


//
// Silence unnecessary htmx:oobErrorNoTarget errors in production.
//
const originalConsoleError = console.error;

console.error = function (...args) {
  const debugElement = document.getElementById("debug-mode");
  let isDebug = false;
  if (debugElement) {
    try {
      isDebug = JSON.parse(debugElement.textContent);
    } catch (e) {
      console.warn("Failed to parse debug-mode content:", e);
    }
  } else {
    console.warn("debug-mode element not found during error handling");
  }

  if (!isDebug && args.length > 0 && args[0] === "htmx:oobErrorNoTarget") {
    return;
  }
  originalConsoleError.apply(console, args);
};

document.body.addEventListener("htmx:oobErrorNoTarget", function (evt) {
  const debugElement = document.getElementById("debug-mode");
  let isDebug = false;
  if (debugElement) {
    try {
      isDebug = JSON.parse(debugElement.textContent);
    } catch (e) {}
  }

  if (isDebug) {
    return;
  }

  const targetId = evt.detail.content.id;
  const isRoomCard = /^card_for_room_\d+$/.test(targetId);
  const isPopupHeader = /^chat_popup_header_content_\d+$/.test(targetId);
  const isSpecificPartial =
    targetId === "chat_button_container" ||
    targetId === "notification_button_indicator" ||
    targetId === "chat_button_indicator";

  if (isRoomCard || isPopupHeader || isSpecificPartial) {
    evt.preventDefault();
  } else {
    originalConsoleError.call(console, "htmx:oobErrorNoTarget", evt.detail);
  }
});


