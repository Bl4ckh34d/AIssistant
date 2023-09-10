const wss = new WebSocketServer({ port: 3000 });

console.log('WebSocket server running on port 3000.');

// Store a reference to the connected WebSocket clients
const connectedClients = new Set();

wss.on('connection', (ws) => {
    console.log('Python connected to WebSocket server.');

    // Add the connected WebSocket client to the set
    connectedClients.add(ws);

    ws.on('message', async (message) => {
        try {
            const command = JSON.parse(message);
            if (command.command === "find_tab") {
                browser.tabs.query({}, async function (tabs) {
                    const searchQuery = command.query.toLowerCase();
                    const matchingTabs = tabs.filter((tab) =>
                        tab.title.toLowerCase().includes(searchQuery)
                    );

                    if (matchingTabs.length > 0) {
                        // Get the first matching tab and bring it into the foreground
                        const firstMatchingTab = matchingTabs[0];
                        await browser.tabs.update(firstMatchingTab.id, { active: true });
                        console.log("Tab updated: " + firstMatchingTab.title);
                        
                        // Send the matching tab titles back to all connected clients
                        const matchingTabTitles = matchingTabs.map((tab) => tab.title);
                        const responseData = {
                            response: matchingTabTitles
                        };

                        // Send the response to all connected clients
                        for (const client of connectedClients) {
                            client.send(JSON.stringify(responseData));
                        }
                    } else {
                        console.log("No matching tabs found.");
                        ws.send(JSON.stringify([])); // Send an empty response to Python
                    }
                });
                console.log('Executing custom command:', command.data);
            }
        } catch (error) {
            console.error('Error parsing JSON:', error);
        }
    });

    ws.on('close', () => {
        console.log('Python disconnected from WebSocket server.');
        // Remove the disconnected WebSocket client from the set
        connectedClients.delete(ws);
    });
});
