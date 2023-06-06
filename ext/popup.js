document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("submit-button").addEventListener("click", (e) => {
        hash = document.getElementById("hash").value
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {type:"addCart", content: hash});
        });
    })
})