import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Web3Provider } from './Web3Provider';
import Navbar from './components/Navbar';
import Landing from './pages/Landing';
import ReportPage from './pages/Report';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat'; // <--- Import Chat
import SOSButton from './components/SOSButton';

function App() {
  return (
    <Web3Provider>
      <BrowserRouter>
        <div className="min-h-screen relative font-sans text-slate-900 bg-brand-50/50 selection:bg-brand-200">
          <Navbar />
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/report" element={<ReportPage />} />
            <Route path="/chat" element={<Chat />} /> {/* <--- New Route */}
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
          <SOSButton />
        </div>
      </BrowserRouter>
    </Web3Provider>
  );
}

export default App;