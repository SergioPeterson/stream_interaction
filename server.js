const express = require('express');
const fs = require('fs');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(cors());

let voteCounts = {};  // ✅ Stores votes for each show/episode
let nextEpVoters = new Set();  // ✅ Stores unique voters for next episode

// ✅ Handle show/episode voting
app.post('/vote', (req, res) => {
    const { username, showName, episodeNumber } = req.body;

    if (!showName || !episodeNumber) {
        return res.status(400).json({ error: "Show name and episode number required." });
    }

    const voteKey = `${showName} Ep ${episodeNumber}`;

    if (!voteCounts[voteKey]) {
        voteCounts[voteKey] = new Set();
    }

    if (voteCounts[voteKey].has(username)) {
        return res.status(400).json({ error: `${username} has already voted for ${voteKey}` });
    }

    voteCounts[voteKey].add(username);
    updateVotesFile();
    
    res.json({ message: `${username} voted for ${voteKey}!`, votes: voteCounts[voteKey].size });
});

// ✅ Handle next episode voting
app.post('/next-episode', (req, res) => {
    const { username } = req.body;

    if (nextEpVoters.has(username)) {
        return res.status(400).json({ error: `${username} has already voted for the next episode.` });
    }

    nextEpVoters.add(username);
    updateNextEpFile();
    
    res.json({ message: `${username} voted for the next episode!`, votes: nextEpVoters.size });
});

// ✅ Update `results/output.txt`
function updateVotesFile() {
    let voteText = "Vote Rankings\n";
    for (let [show, voters] of Object.entries(voteCounts)) {
        voteText += `${show} : ${voters.size} votes\n`;
    }
    fs.writeFileSync("results/output.txt", voteText, "utf8");
}

// ✅ Update `results/nextep.txt`
function updateNextEpFile() {
    let nextEpText = `Next Ep Voters : ${nextEpVoters.size} votes`;
    fs.writeFileSync("results/nextep.txt", nextEpText, "utf8");
}

// ✅ Start the server
app.listen(PORT, () => {
    console.log(`✅ Server running on http://localhost:${PORT}`);
});