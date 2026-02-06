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
  const isSpecificPartial =
    targetId === "chat_button_container" ||
    targetId === "notification_button_indicator" ||
    targetId === "chat_button_indicator";

  if (isRoomCard || isSpecificPartial) {
    evt.preventDefault();
  } else {
    originalConsoleError.call(console, "htmx:oobErrorNoTarget", evt.detail);
  }
});
