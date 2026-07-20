import Navbar from "./components/Navbar";
import UploadBox from "./components/UploadBox";
import ChatBox from "./components/ChatBox";

function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />

      <div className="grid grid-cols-12 gap-6 p-6">

        <div className="col-span-4">
          <UploadBox />
        </div>

        <div className="col-span-8">
          <ChatBox />
        </div>

      </div>
    </div>
  );
}

export default App;