import { MapPin, Search, Hash } from 'lucide-react';

const MOCK_REPORTS = [
  { id: 1, type: 'Harassment', location: 'Yaba Tech, Lagos', time: '2 hrs ago', status: 'Verified', score: 98, hash: '0x7a...891' },
  { id: 2, type: 'Corruption', location: 'Lekki Toll Gate', time: '5 hrs ago', status: 'Pending', score: 45, hash: '0x8b...123' },
  { id: 3, type: 'Violence', location: 'Agege Motor Rd', time: '1 day ago', status: 'Verified', score: 92, hash: '0x1c...555' },
];

export default function Dashboard() {
  return (
    <div className="max-w-7xl mx-auto pt-6 px-4 pb-20">
      
      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
          <h3 className="text-slate-400 text-sm font-bold uppercase tracking-wider">Active Reports</h3>
          <p className="text-4xl font-bold text-slate-900 mt-2">1,284</p>
        </div>
        <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
          <h3 className="text-slate-400 text-sm font-bold uppercase tracking-wider">Verified by Web3</h3>
          <p className="text-4xl font-bold text-brand-600 mt-2">94%</p>
        </div>
        <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
          <h3 className="text-slate-400 text-sm font-bold uppercase tracking-wider">Avg Trust Score</h3>
          <p className="text-4xl font-bold text-slate-900 mt-2">8.2/10</p>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="p-6 border-b border-slate-100 flex justify-between items-center">
          <h2 className="text-xl font-bold text-slate-800">Live Incident Feed</h2>
          <div className="relative">
            <Search className="absolute left-3 top-2.5 w-4 h-4 text-slate-400" />
            <input type="text" placeholder="Search..." className="pl-10 pr-4 py-2 rounded-xl border border-slate-200 text-sm" />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-slate-50 text-slate-500 text-xs uppercase font-bold tracking-wider">
              <tr>
                <th className="px-6 py-4">Incident Type</th>
                <th className="px-6 py-4">Location</th>
                <th className="px-6 py-4">Trust Score</th>
                <th className="px-6 py-4">Proof (Hash)</th>
                <th className="px-6 py-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {MOCK_REPORTS.map((report) => (
                <tr key={report.id} className="hover:bg-slate-50 transition">
                  <td className="px-6 py-4 font-bold text-slate-800">{report.type}</td>
                  <td className="px-6 py-4 flex items-center gap-1 text-slate-600"><MapPin className="w-3 h-3"/> {report.location}</td>
                  <td className="px-6 py-4 text-slate-600 font-bold">{report.score}%</td>
                  <td className="px-6 py-4">
                    <span className="flex items-center gap-1 text-xs font-mono text-brand-700 bg-brand-50 px-2 py-1 rounded w-fit">
                      <Hash className="w-3 h-3" /> {report.hash}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                     <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                      report.status === 'Verified' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                    }`}>
                      {report.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}