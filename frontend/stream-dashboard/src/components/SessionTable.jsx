import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table/Table";

export default function SessionTable({ sessions, setSelectedSession }) {
    return (
        <div className="overflow-auto bg-white p-4 rounded-lg shadow">
            <h2 className="text-lg font-bold mb-2">Live Stream Sessions</h2>
            <Table>
                <TableHeader>
                    <TableHead>ID</TableHead>
                    <TableHead>Platform</TableHead>
                    <TableHead>Streamer</TableHead>
                    <TableHead>Start Time</TableHead>
                </TableHeader>
                <TableBody>
                    {sessions.map((session) => (
                        <TableRow
                            key={session.session_id}
                            className="cursor-pointer hover:bg-gray-100 background-color: coral padding:100px"
                            onClick={() => setSelectedSession(session.session_id)}
                        >
                            <TableCell>{session.session_id}</TableCell>
                            <TableCell>{session.platform}</TableCell>
                            <TableCell>{session.streamer_name}</TableCell>
                            <TableCell>{session.start_time}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
            <h2 className="text-lg font-bold mb-2">Live Stream Sessions</h2>
            <select
                className="w-full p-2 border rounded-lg"
                onChange={(e) => setSelectedSession(Number(e.target.value))}
                defaultValue=""
            >
                <option value="" disabled>Select a session</option>
                {sessions.map((session) => (
                    <option key={session.session_id} value={session.session_id}>
                        {session.streamer_name} - {session.platform} ({session.start_time})
                    </option>
                ))}
            </select>

        </div>
    );
}