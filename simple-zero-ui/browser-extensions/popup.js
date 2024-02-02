function syncBookmark2Web() {
  var domainEle = document.querySelector('input[name="syncDomain"]');

  chrome.bookmarks.getTree((tree) => {
    if (tree.length > 0) {
      for (let i = 0; i < tree[0].children.length; i++) {
        const item = tree[0].children[i];
        if (item.index === 0) {
          chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            if (tabs.length > 0) {
              chrome.tabs.sendMessage(tabs[0].id, item)
              document.getElementById('sync-rst').innerText = `已同步: ${extractDomain(tabs[0].url)}`
            }
          });
          break;
        }
      }
    }
  });
}

function extractDomain(url) {
  let domain;
  try {
    domain = new URL(url).hostname;
  } catch (error) {
    domain = 'Invalid URL';
  }
  return domain;
}

document.getElementById("syncBtn").addEventListener("click", syncBookmark2Web);