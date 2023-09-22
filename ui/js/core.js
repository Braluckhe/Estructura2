function onClose() {
    eel.on_window_close();
}

window.addEventListener("beforeunload", onClose);
