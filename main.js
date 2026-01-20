/**
 * Hieu An Website Security Script
 * Prevents Right Click, F12, and Source View shortcuts
 */

// Disable Right Click
document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
}, false);

// Disable Keyboard Shortcuts
document.onkeydown = function(e) {
    // Disable F12
    if (e.keyCode == 123) {
        return false;
    }
    // Disable Ctrl+Shift+I (Inspect)
    if (e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)) {
        return false;
    }
    // Disable Ctrl+Shift+J (Console)
    if (e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)) {
        return false;
    }
    // Disable Ctrl+U (View Source)
    if (e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)) {
        return false;
    }
    // Disable Ctrl+S (Save Page)
    if (e.ctrlKey && e.keyCode == 'S'.charCodeAt(0)) {
        return false;
    }
};

console.log("%cDừng lại!", "color: red; font-family: sans-serif; font-size: 4.5em; font-weight: bolder; text-shadow: #000 1px 1px;");
console.log("%cĐây là tính năng dành cho nhà phát triển. Việc sao chép mã nguồn khi chưa được phép là vi phạm quyền sở hữu trí tuệ của Hiếu An.", "font-family: sans-serif; font-size: 1.5em; font-weight: bold;");
