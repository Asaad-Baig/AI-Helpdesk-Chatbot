import React, { useEffect, useState } from 'react';

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    total_conversations: 0,
    total_messages: 0,
    error_logs: [],
    feedback: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5000/api/admin/stats')
      .then((res) => res.json())
      .then((data) => {
        setStats(data);
        setLoading(false);
      })
      .catch((err) => console.error("Admin dashboard fetch error:", err));
  }, []);

  if (loading) {
    return <div className="p-8 text-slate-300">Loading system metrics...</div>;
  }

  return (
    <div className="p-6 bg-slate-900 min-h-screen text-slate-100 font-sans">
      <h1 className="text-2xl font-bold mb-6 text-indigo-400">System Admin & Health Dashboard</h1>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-slate-800 p-5 rounded-xl border border-slate-700">
          <p className="text-xs font-semibold text-slate-400 uppercase">Total Conversations</p>
          <p className="text-3xl font-bold text-white mt-2">{stats.total_conversations}</p>
        </div>
        <div className="bg-slate-800 p-5 rounded-xl border border-slate-700">
          <p className="text-xs font-semibold text-slate-400 uppercase">Total Messages Processed</p>
          <p className="text-3xl font-bold text-white mt-2">{stats.total_messages}</p>
        </div>
        <div className="bg-slate-800 p-5 rounded-xl border border-slate-700">
          <p className="text-xs font-semibold text-slate-400 uppercase">Logged Errors / Warnings</p>
          <p className="text-3xl font-bold text-rose-400 mt-2">{stats.error_logs.length}</p>
        </div>
      </div>

      {/* Error Logs Table */}
      <div className="bg-slate-800 rounded-xl border border-slate-700 p-5">
        <h2 className="text-lg font-semibold mb-4 text-slate-200">System Error & Fallback Audit Logs</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase text-xs">
              <tr>
                <th className="py-3 px-4">Type</th>
                <th className="py-3 px-4">Message</th>
                <th className="py-3 px-4">User Query</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700">
              {stats.error_logs.map((log, index) => (
                <tr key={index} className="hover:bg-slate-750">
                  <td className="py-3 px-4 font-mono text-rose-400">{log.error_type}</td>
                  <td className="py-3 px-4">{log.message}</td>
                  <td className="py-3 px-4 text-slate-400 italic">"{log.query}"</td>
                </tr>
              ))}
              {stats.error_logs.length === 0 && (
                <tr>
                  <td colSpan="3" className="py-4 text-center text-slate-500">No runtime errors logged.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;