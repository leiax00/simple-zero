chrome.webNavigation.onDOMContentLoaded.addListener(async ({ tabId, url }) => {
  chrome.scripting.executeScript({
    target: { tabId },
    files: ["inject.js"]
  }).then(() => {
    console.log("script injected");
    syncBookmark2Web(tabId);
  });
});

function syncBookmark2Web(tabId) {
  chrome.bookmarks.getTree((tree) => {
    if (tree.length > 0) {
      for (let i = 0; i < tree[0].children.length; i++) {
        const item = tree[0].children[i];
        if (item.index === 0) {
          chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            if (tabs.length > 0) {
              chrome.tabs.sendMessage(tabId, item);
            }
          });
          break;
        }
      }
    }
  });
}