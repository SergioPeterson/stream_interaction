const oAuth = "oauth:i9mb9w8mydpu0zpv0q4as9qkv5a82x";
const CLIENT_ID = "f48pwsj7gitmrcsx0ffl83msm8w6sm";  
const ACCESS_TOKEN_SUB = "28cncoxqye2ajwm1jilg14b11iht32";
const BROADCASTER_ID = "1268898855"; 

const user = "bearthecoder";
const channel = "watchocracy";

const socket = new WebSocket('wss://irc-ws.chat.twitch.tv:443');

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
function processChatCommand(username, message) {
  const timestamp = new Date().toLocaleTimeString();
  const commandParts = message.slice(1).split(" "); // Remove "!" and split command
  const command = commandParts[0].toLowerCase();
  const args = commandParts.slice(1); // Arguments after the command

  let responseMessage = "";

  switch (command) {
    case "vote":
      if (args.length === 0) {
        responseMessage = `[${timestamp}] ⚠️ ${username}, please specify a show and episode. Example: !vote Attack on Titan;12`;
      } else {
        const voteData = args.join(" ").split(";");
        if (voteData.length !== 2) {
          responseMessage = `[${timestamp}] ⚠️ ${username}, incorrect format. Use !vote <animeName>;<Ep number>`;
        } else {
          const showName = voteData[0].trim();
          const episodeNumber = voteData[1].trim();

          // ✅ Send vote to Node.js server
          fetch("http://localhost:3000/vote", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, showName, episodeNumber })
          })
          .then(response => response.json())
          .then(data => {
            if (data.error) {
              responseMessage = `[${timestamp}] ⚠️ ${data.error}`;
            } else {
              responseMessage = `[${timestamp}] ✅ ${data.message}`;
            }
            displayChatResponse(responseMessage);
          })
          .catch(error => console.error("❌ Vote request failed:", error));
        }
      }
      break;

    case "next_episode":
      // ✅ Send next episode vote to server
      fetch("http://localhost:3000/next-episode", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username })
      })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          responseMessage = `[${timestamp}] ⚠️ ${data.error}`;
        } else {
          responseMessage = `[${timestamp}] ✅ ${data.message}`;
        }
        displayChatResponse(responseMessage);
      })
      .catch(error => console.error("❌ Next episode vote request failed:", error));
      break;

    default:
      responseMessage = `[${timestamp}] ⚠️ Unknown command: ${command}`;
      displayChatResponse(responseMessage);
  }
}

// ✅ Display chat messages or command responses
function displayChatResponse(responseMessage) {
  const outputDiv = document.getElementById("chatOutput");
  outputDiv.innerHTML += `<span style="color: lightblue;">${responseMessage}</span><br>`;
  outputDiv.scrollTop = outputDiv.scrollHeight;
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



// const eventSubSocket = new WebSocket("wss://eventsub.wss.twitch.tv/ws");

// ✅ EVENTSUB SOCKET CONNECTION
// eventSubSocket.onopen = () => {
//   console.log("✅ Connected to Twitch EventSub");
// };

// ✅ HANDLE EVENTSUB MESSAGES
// eventSubSocket.onmessage = async (event) => {
//   const eventData = JSON.parse(event.data);
//   console.log("📩 EventSub Notification:", JSON.stringify(eventData, null, 2));

//   // ✅ If Twitch sends a session ID, subscribe to events
//   if (eventData.session && eventData.session.id) {
//     console.log("✅ EventSub Session ID:", eventData.session.id);
//     await subscribeToEventSub(eventData.session.id);
//     return;
//   }

//   // ✅ If an actual event was received, process it
//   if (eventData.payload && eventData.payload.event) {
//     console.log("✅ Received Event:", JSON.stringify(eventData.payload.event, null, 2));
//     handleEventSubNotification(eventData.payload.event);
//   } else {
//     console.warn("⚠️ Non-event message received:", JSON.stringify(eventData, null, 2));
//   }
// };

// ✅ HANDLE EVENTSUB EVENTS (Follows, Subs, Cheers, Raids)
// function handleEventSubNotification(event) {
//   if (!event || !event.type) {
//     console.warn("❌ Invalid EventSub notification:", event);
//     return;
//   }

//   const timestamp = new Date().toLocaleTimeString();
//   let eventMessage = "";

//   switch (event.type) {
//     case "channel.follow":
//       eventMessage = `<span style="color: cyan;">[${timestamp}] 👤 ${event.user_name} followed!</span><br>`;
//       break;
//     case "channel.subscribe":
//       eventMessage = `<span style="color: pink;">[${timestamp}] 🎉 ${event.user_name} subscribed!</span><br>`;
//       break;
//     case "channel.subscription.gift":
//       eventMessage = `<span style="color: gold;">[${timestamp}] 🎁 ${event.user_name} gifted ${event.total} subs!</span><br>`;
//       break;
//     case "channel.cheer":
//       eventMessage = `<span style="color: purple;">[${timestamp}] 🏆 ${event.user_name} cheered ${event.bits} bits!</span><br>`;
//       break;
//     case "channel.raid":
//       eventMessage = `<span style="color: orange;">[${timestamp}] 🚀 ${event.from_broadcaster_user_name} raided with ${event.viewers} viewers!</span><br>`;
//       break;
//     default:
//       console.warn("⚠️ Unknown EventSub type received:", event);
//   }

//   if (eventMessage) {
//     const specialOutputDiv = document.getElementById("specialOutput");
//     specialOutputDiv.innerHTML += eventMessage;
//     specialOutputDiv.scrollTop = specialOutputDiv.scrollHeight;
//   }
// }

// ✅ SUBSCRIBE TO TWITCH EVENTSUB EVENTS
// async function subscribeToEventSub(session_id) {
//   if (!session_id) {
//     console.error("❌ No session_id received from WebSocket. Cannot subscribe.");
//     return;
//   }

//   const topics = [
//     "channel.follow",
//     "channel.subscribe",
//     "channel.subscription.gift",
//     "channel.cheer",
//     "channel.raid"
//   ];

//   for (const topic of topics) {
//     try {
//       const response = await fetch("https://api.twitch.tv/helix/eventsub/subscriptions", {
//         method: "POST",
//         headers: {
//           "Client-ID": CLIENT_ID,
//           "Authorization": `Bearer ${ACCESS_TOKEN_SUB}`, // ✅ Using correct access token
//           "Content-Type": "application/json"
//         },
//         body: JSON.stringify({
//           type: topic,
//           version: "1",
//           condition: {
//             broadcaster_user_id: BROADCASTER_ID
//           },
//           transport: {
//             method: "websocket",
//             session_id: session_id
//           }
//         })
//       });

//       const data = await response.json();
//       console.log(`✅ Subscription Response for ${topic}:`, JSON.stringify(data, null, 2));

//       if (data.error) {
//         console.error(`❌ Error subscribing to ${topic}:`, JSON.stringify(data, null, 2));
//       }
//     } catch (error) {
//       console.error(`❌ Failed to subscribe to ${topic}:`, error);
//     }
//   }
// }

