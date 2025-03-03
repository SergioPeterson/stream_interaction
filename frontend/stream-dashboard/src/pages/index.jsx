import { useState, useEffect } from "react";
import SessionTable from "../components/SessionTable";
import StreamStats from "../components/StreamStats";
import ViewerChart from "../components/ViewerChart";



export default function StreamDashboard() {
    const [selectedSession, setSelectedSession] = useState(null);
    const [sessions, setSessions] = useState([]);
    const [stats, setStats] = useState({});
    const [viewerData, setViewerData] = useState({});


    // Fetch session data
    useEffect(() => {
        fetch("http://127.0.0.1:5000/api/sessions")
            .then(res => res.json())
            .then(data => setSessions(data))
            .catch(err => console.error("Error fetching sessions:", err));
    }, []);

    // Fetch stats
    useEffect(() => {
        fetch("http://127.0.0.1:5000/api/stats")
            .then(res => res.json())
            .then(data => {
                let statsDict = {};
                data.forEach(stat => statsDict[stat.session_id] = stat);
                setStats(statsDict);
            })
            .catch(err => console.error("Error fetching stats:", err));
    }, []);

    // Fetch viewer data when session is selected
    useEffect(() => {
        if (!selectedSession) return;

        fetch(`http://127.0.0.1:5000/api/viewers/${selectedSession}`)
            .then(res => res.json())
            .then(data => setViewerData(prev => ({ ...prev, [selectedSession]: data })))
            .catch(err => console.error("Error fetching viewers:", err));
    }, [selectedSession]);

        
    return (
        <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Session */}
            <SessionTable sessions={sessions} setSelectedSession={setSelectedSession} />
            {/* Stats */}
            <StreamStats stats={stats} selectedSession={selectedSession} />
            {/* Viewer */}
            <ViewerChart viewerData={viewerData} selectedSession={selectedSession} />
        </div>
    );
}