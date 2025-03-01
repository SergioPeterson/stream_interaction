
const user = "bearthecoder";
const channel = "watchocracy";

const socket = new WebSocket('wss://irc-ws.chat.twitch.tv:443');
const eventSubSocket = new WebSocket("wss://eventsub.wss.twitch.tv/ws");

// ✅ CONNECT TO TWITCH IRC (Chat)
socket.addEventListener('open', () => {
  console.log("✅ Connected to Twitch IRC");
  socket.send(`PASS ${oAuth}`);
  socket.send(`NICK ${user}`);
  socket.send(`JOIN #${channel}`);
});

// ✅ HANDLE MESSAGES FROM TWITCH CHAT
socket.addEventListener('message', (event) => {
  const messageData = event.data.trim();

  if (messageData.includes("PING")) {
    socket.send("PONG");
    return;
  }

  const chatMatch = messageData.match(/^:(\w+)!.*PRIVMSG #\w+ :(.*)$/);
  if (chatMatch) {
    const username = chatMatch[1];
    const message = chatMatch[2].trim();

    // ✅ Process commands
    if (message.startsWith("!")) {
      processChatCommand(username, message);
    } else {
      displayChatMessage(username, message);
    }
  }

  if (messageData.includes("USERNOTICE")) {
    displaySpecialEvent(messageData);
  }
});
const fs = require('fs');  // ✅ Import File System for writing to OBS

const voteCounts = {};  // ✅ Stores votes for each show/episode
const nextEpVoters = new Set();  // ✅ Stores unique voters for next episode

function processChatCommand(username, message) {
  const timestamp = new Date().toLocaleTimeString();
  const commandParts = message.slice(1).split(" "); // Remove "!" and split command
  const command = commandParts[0].toLowerCase();
  const args = commandParts.slice(1); // Arguments after the command

  let responseMessage = "";

  switch (command) {
    case "vote":
      if (args.length === 0) {
        responseMessage = `[${timestamp}] ⚠️ ${username}, please specify a show and episode number. Example: !vote Attack on Titan;12`;
      } else {
        const voteData = args.join(" ").split(";"); // Split by semicolon
        if (voteData.length !== 2) {
          responseMessage = `[${timestamp}] ⚠️ ${username}, incorrect format. Use !vote <animeName>;<Ep number>`;
        } else {
          const showName = voteData[0].trim();
          const episodeNumber = voteData[1].trim();
          const voteKey = `${showName} Ep ${episodeNumber}`; // Unique identifier

          if (!voteCounts[voteKey]) {
            voteCounts[voteKey] = new Set(); // Store unique voters
          }

          if (voteCounts[voteKey].has(username)) {
            responseMessage = `[${timestamp}] ⚠️ ${username}, you have already voted for ${showName} Ep ${episodeNumber}!`;
          } else {
            voteCounts[voteKey].add(username);  // ✅ Store unique vote
            updateVotesFile();  // ✅ Write to file
            responseMessage = `[${timestamp}] ✅ ${username} voted for "${showName}" Episode ${episodeNumber}! (${voteCounts[voteKey].size} votes)`;
          }
        }
      }
      break;

    case "next_episode":
      if (nextEpVoters.has(username)) {
        responseMessage = `[${timestamp}] ⚠️ ${username}, you have already voted for the next episode!`;
      } else {
        nextEpVoters.add(username); // ✅ Store unique vote
        updateNextEpFile();
        responseMessage = `[${timestamp}] 🎬 ${username} voted for the next episode! (${nextEpVoters.size} votes)`;
      }
      break;

    default:
      responseMessage = `[${timestamp}] ⚠️ Unknown command: ${command}`;
  }

  if (responseMessage) {
    const outputDiv = document.getElementById("chatOutput");
    outputDiv.innerHTML += `<span style="color: lightblue;">${responseMessage}</span><br>`;
    outputDiv.scrollTop = outputDiv.scrollHeight;
  }
}

// ✅ Function to update `results/output.txt` for show rankings
function updateVotesFile() {
  let voteText = "Vote Rankings\n";
  for (let [show, voters] of Object.entries(voteCounts)) {
    voteText += `${show} : ${voters.size}\n`;
  }

  // ✅ Write to `results/output.txt`
  fs.writeFileSync("results/output.txt", voteText, "utf8");
}

// ✅ Function to update `results/nextep.txt` for next episode votes
function updateNextEpFile() {
  let nextEpText = `Next Ep Voters : ${nextEpVoters.size}`;

  // ✅ Write to `results/nextep.txt`
  fs.writeFileSync("results/nextep.txt", nextEpText, "utf8");
}

function displayChatMessage(username, message) {
  const timestamp = new Date().toLocaleTimeString();
  const formattedMessage = `<span style="color: lightblue;">[${timestamp}]</span> 
                            <strong style="color: yellow;">${username}:</strong> 
                            <span style="color: white;">${message}</span><br>`;

  const outputDiv = document.getElementById("chatOutput");
  outputDiv.innerHTML += formattedMessage;
  outputDiv.scrollTop = outputDiv.scrollHeight;
}

// ✅ EVENTSUB SOCKET CONNECTION
eventSubSocket.onopen = () => {
  console.log("✅ Connected to Twitch EventSub");
};

// ✅ HANDLE EVENTSUB MESSAGES
eventSubSocket.onmessage = async (event) => {
  const eventData = JSON.parse(event.data);
  console.log("📩 EventSub Notification:", JSON.stringify(eventData, null, 2));

  // ✅ If Twitch sends a session ID, subscribe to events
  if (eventData.session && eventData.session.id) {
    console.log("✅ EventSub Session ID:", eventData.session.id);
    await subscribeToEventSub(eventData.session.id);
    return;
  }

  // ✅ If an actual event was received, process it
  if (eventData.payload && eventData.payload.event) {
    console.log("✅ Received Event:", JSON.stringify(eventData.payload.event, null, 2));
    handleEventSubNotification(eventData.payload.event);
  } else {
    console.warn("⚠️ Non-event message received:", JSON.stringify(eventData, null, 2));
  }
};

// ✅ HANDLE EVENTSUB EVENTS (Follows, Subs, Cheers, Raids)
function handleEventSubNotification(event) {
  if (!event || !event.type) {
    console.warn("❌ Invalid EventSub notification:", event);
    return;
  }

  const timestamp = new Date().toLocaleTimeString();
  let eventMessage = "";

  switch (event.type) {
    case "channel.follow":
      eventMessage = `<span style="color: cyan;">[${timestamp}] 👤 ${event.user_name} followed!</span><br>`;
      break;
    case "channel.subscribe":
      eventMessage = `<span style="color: pink;">[${timestamp}] 🎉 ${event.user_name} subscribed!</span><br>`;
      break;
    case "channel.subscription.gift":
      eventMessage = `<span style="color: gold;">[${timestamp}] 🎁 ${event.user_name} gifted ${event.total} subs!</span><br>`;
      break;
    case "channel.cheer":
      eventMessage = `<span style="color: purple;">[${timestamp}] 🏆 ${event.user_name} cheered ${event.bits} bits!</span><br>`;
      break;
    case "channel.raid":
      eventMessage = `<span style="color: orange;">[${timestamp}] 🚀 ${event.from_broadcaster_user_name} raided with ${event.viewers} viewers!</span><br>`;
      break;
    default:
      console.warn("⚠️ Unknown EventSub type received:", event);
  }

  if (eventMessage) {
    const specialOutputDiv = document.getElementById("specialOutput");
    specialOutputDiv.innerHTML += eventMessage;
    specialOutputDiv.scrollTop = specialOutputDiv.scrollHeight;
  }
}

// ✅ SUBSCRIBE TO TWITCH EVENTSUB EVENTS
async function subscribeToEventSub(session_id) {
  if (!session_id) {
    console.error("❌ No session_id received from WebSocket. Cannot subscribe.");
    return;
  }

  const topics = [
    "channel.follow",
    "channel.subscribe",
    "channel.subscription.gift",
    "channel.cheer",
    "channel.raid"
  ];

  for (const topic of topics) {
    try {
      const response = await fetch("https://api.twitch.tv/helix/eventsub/subscriptions", {
        method: "POST",
        headers: {
          "Client-ID": CLIENT_ID,
          "Authorization": `Bearer ${ACCESS_TOKEN_SUB}`, // ✅ Using correct access token
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          type: topic,
          version: "1",
          condition: {
            broadcaster_user_id: BROADCASTER_ID
          },
          transport: {
            method: "websocket",
            session_id: session_id
          }
        })
      });

      const data = await response.json();
      console.log(`✅ Subscription Response for ${topic}:`, JSON.stringify(data, null, 2));

      if (data.error) {
        console.error(`❌ Error subscribing to ${topic}:`, JSON.stringify(data, null, 2));
      }
    } catch (error) {
      console.error(`❌ Failed to subscribe to ${topic}:`, error);
    }
  }
}