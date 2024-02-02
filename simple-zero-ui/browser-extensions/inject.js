chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('sz received:', message)
  localStorage.setItem('sz-bbm', JSON.stringify(message))
})