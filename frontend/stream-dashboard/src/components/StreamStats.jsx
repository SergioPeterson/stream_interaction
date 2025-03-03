import { Card, CardContent, CardHeader } from "./ui/card/Card";

export default function StreamStats({ stats, selectedSession }) {
    if (!selectedSession || !stats[selectedSession]) return null;
    
    const sessionStats = stats[selectedSession];

    return (
        <Card className="bg-white p-4 shadow rounded-lg">
            <CardHeader className="text-lg font-bold">Stream Statistics</CardHeader>
            <CardContent>
                <p><strong>Followers Gained:</strong> {sessionStats.followers_gained}</p>
                <p><strong>Top Commenter:</strong> {sessionStats.top_commenter}</p>
                <p><strong>Top Gifter:</strong> {sessionStats.top_gifter || 'None'}</p>
                <p><strong>Gifts:</strong> {JSON.stringify(sessionStats.gifts)}</p>
                <p><strong>Total Comments:</strong> {sessionStats.comment_count}</p>
            </CardContent>
        </Card>
    );
}