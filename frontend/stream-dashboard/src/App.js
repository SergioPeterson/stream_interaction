import StreamDashboard from "./pages/index";
// import "./styles/globals.css";

export default function App() {
  return (
    <div className="bg-gray-100 min-h-screen flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold mb-4">📊 Live Stream Analytics</h1>
      <StreamDashboard />
    </div>
  );
}