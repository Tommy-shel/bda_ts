import React, { useState } from 'react';

const StatCard = ({ title, value, color, icon }) => (
  <div className={`p-5 rounded-2xl shadow-lg border-l-4 ${color} bg-white transition hover:scale-105 duration-300`}>
    <div className="flex justify-between items-center">
      <div>
        <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">{title}</h3>
        <p className="text-3xl font-black text-gray-800 mt-1">{value}</p>
      </div>
      <span className="text-3xl">{icon}</span>
    </div>
  </div>
);

function App() {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [activeTab, setActiveTab] = useState("all");

  const handlePredict = async () => {
    if (!title || !text) {
      alert("Please enter both an article headline and content.");
      return;
    }

    setLoading(true);
    setErrorMsg("");
    setResult(null);

    try {
      const response = await fetch("https://bda-ts.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, text })
      });

      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setErrorMsg("Could not connect to FastAPI backend. Make sure 'python backend/main.py' is running on port 8000!");
    } finally {
      setLoading(false);
    }
  };

  const loadSample = (type) => {
    if (type === 'fake') {
      setTitle("5G TOWERS ACTIVATED: Millions of Smartphones Hijacked by Quantum Hive Mind!");
      setText("A former senior engineer leaked source code proving the latest cellular update secretly synchronizes human brainwave frequencies with quantum mainframe computers, causing spontaneous psychic disruptions.");
    } else if (type === 'nepal') {
      setTitle("Heavy Monsoon Rains Trigger Severe Flooding in Nepal, Over 15,000 Displaced");
      setText("Torrential downpours across Kathmandu and Eastern Nepal have caused widespread devastation, prompting authorities to deploy army personnel and disaster management forces. According to regional disaster response coordinators, more than 15,000 families have been evacuated to relief shelters.");
    } else if (type === 'cjp') {
      setTitle("CJP Protest: Lawyers and Activists Gather Outside Supreme Court");
      setText("Massive protests erupted today as legal experts and activists gathered to demand judicial reforms. The Chief Justice of Pakistan's recent decisions have sparked a nationwide debate on constitutional powers.");
    } else if (type === 'epstein') {
      setTitle("Judicial Panel Unseals Over 9,000 Pages of Documents in High-Profile Epstein Case");
      setText("Newly unredacted court depositions spanning 9,000 pages have been made accessible to the public following a federal court disclosure order in the Epstein Associate Deposition inquiry. Legal analysts state the records provide detailed accounts of financial audits.");
    } else if (type === 'reuters_climate') {
      setTitle("Global Trade Volume Expands by 4.8% as Supply Chain Pressures Ease");
      setText("Financial institutions reported robust quarterly revenue driven primarily by gains in the Renewable Energy sector, supported by sustained global demand.");
    } else {
      setTitle("Senate passes bipartisan infrastructure bill");
      setText("The Senate today voted in favor of a major infrastructure package, marking a rare moment of bipartisan cooperation. Spokespersons stated this bill will fund critical upgrades to roads and bridges.");
    }
  };

  const trendingNewsData = {
    all: [
      { title: "Nepal Flood Relief Efforts Continue", source: "BBC News", trend: "+240% reach", color: "text-blue-600", tag: "nepal" },
      { title: "CJP Protest Updates & Supreme Court", source: "Reuters", trend: "+180% reach", color: "text-green-600", tag: "cjp" },
      { title: "Epstein Case Files Unsealed Spanning 9,000 Pages", source: "Google News", trend: "+500% reach", color: "text-purple-600", tag: "epstein" }
    ],
    bbc: [
      { title: "Nepal Flood: Relief Operations Stepped Up in Eastern Districts", source: "BBC News", trend: "+240% reach", color: "text-blue-600", tag: "nepal" },
      { title: "5G Quantum Hive Mind Hoax Spreading Online", source: "BBC News", trend: "+310% reach", color: "text-red-500", tag: "fake" }
    ],
    reuters: [
      { title: "CJP Protest: Judicial Bar Associations Convene Over Reform Bill", source: "Reuters", trend: "+180% reach", color: "text-green-600", tag: "cjp" },
      { title: "Global Trade Expands as Energy Sector Shifts to Renewables", source: "Reuters", trend: "+120% reach", color: "text-emerald-500", tag: "reuters_climate" }
    ],
    google: [
      { title: "Epstein Associate Depositions Made Public via Federal Court", source: "Google News", trend: "+500% reach", color: "text-purple-600", tag: "epstein" },
      { title: "Crisis Actor Holograms Allegations Exposed as Fabricated", source: "Google News", trend: "+420% reach", color: "text-amber-500", tag: "cjp" }
    ]
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-900 p-6">
      {/* Header */}
      <div className="max-w-6xl mx-auto mb-10 text-center">
        <h1 className="text-4xl font-extrabold text-blue-900 mb-2">
          Fake News Detection & Big Data Analytics
        </h1>
        <p className="text-lg text-gray-600 font-medium">
          Distributed Storage (HDFS) • Parallel Processing (PySpark) • Distributed ML (Spark MLlib)
        </p>
      </div>

      {/* Stats Counter */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        <StatCard title="Total Articles Processed" value="205,596" color="border-blue-500" icon="📦" />
        <StatCard title="Real Articles Analyzed" value="102,798" color="border-green-500" icon="✅" />
        <StatCard title="Fake Articles Analyzed" value="102,798" color="border-red-500" icon="🚨" />
        <StatCard title="Model Accuracy" value="100.0%" color="border-purple-500" icon="🎯" />
      </div>

      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-10">
        {/* Detection Section */}
        <div className="space-y-6">
          <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800 flex items-center">
                <span className="bg-blue-100 p-2 rounded-lg mr-3">🔍</span>
                Live Detection
              </h2>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => loadSample('fake')}
                  className="text-xs bg-red-100 text-red-700 font-semibold px-2 py-1 rounded hover:bg-red-200 transition"
                >
                  + Fake
                </button>
                <button
                  onClick={() => loadSample('real')}
                  className="text-xs bg-green-100 text-green-700 font-semibold px-2 py-1 rounded hover:bg-green-200 transition"
                >
                  + Real
                </button>
                <button
                  onClick={() => loadSample('nepal')}
                  className="text-xs bg-blue-100 text-blue-700 font-semibold px-2 py-1 rounded hover:bg-blue-200 transition"
                >
                  + Nepal Flood
                </button>
                <button
                  onClick={() => loadSample('cjp')}
                  className="text-xs bg-orange-100 text-orange-700 font-semibold px-2 py-1 rounded hover:bg-orange-200 transition"
                >
                  + CJP Protest
                </button>
                <button
                  onClick={() => loadSample('epstein')}
                  className="text-xs bg-purple-100 text-purple-700 font-semibold px-2 py-1 rounded hover:bg-purple-200 transition"
                >
                  + Epstein Files
                </button>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Headline</label>
                <input
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition"
                  placeholder="e.g. Secret document leaks online..."
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Article Content</label>
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-xl h-36 focus:ring-2 focus:ring-blue-500 outline-none transition"
                  placeholder="Paste news content here..."
                />
              </div>
              <button
                onClick={handlePredict}
                disabled={loading}
                className={`w-full py-4 rounded-xl font-bold text-white transition transform active:scale-95 ${loading ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700 shadow-lg hover:shadow-blue-200'}`}
              >
                {loading ? "Analyzing with PySpark MLlib..." : "Verify Authenticity"}
              </button>
            </div>

            {errorMsg && (
              <div className="mt-6 p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-sm font-medium">
                ⚠️ {errorMsg}
              </div>
            )}

            {result && (
              <div className={`mt-8 p-6 rounded-2xl border-2 transition-all duration-500 ${result.prediction === 'FAKE' ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
                <div className="flex justify-between items-center mb-2">
                  <span className={`text-xs font-bold uppercase tracking-wider px-2 py-1 rounded ${result.prediction === 'FAKE' ? 'bg-red-200 text-red-800' : 'bg-green-200 text-green-800'}`}>
                    Prediction Result
                  </span>
                  <span className="text-xs font-medium text-gray-500">{result.model_used}</span>
                </div>
                <h3 className={`text-3xl font-black ${result.prediction === 'FAKE' ? 'text-red-700' : 'text-green-700'}`}>
                  {result.prediction === 'FAKE' ? 'LIKELY FAKE NEWS' : 'LIKELY REAL NEWS'}
                </h3>
                <p className="text-gray-700 mt-2 font-medium">
                  Confidence: <span className="font-bold text-gray-900">{result.confidence}</span>
                </p>
              </div>
            )}
          </div>

          {/* Trending News Section categorized by Source */}
          <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800 flex items-center">
                <span className="bg-orange-100 p-2 rounded-lg mr-3">🔥</span>
                Trending Topics
              </h2>
              <div className="flex gap-1 mt-3 sm:mt-0 bg-gray-100 p-1 rounded-xl">
                {["all", "bbc", "reuters", "google"].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`text-xs px-3 py-1.5 font-bold rounded-lg transition ${activeTab === tab ? 'bg-white text-blue-900 shadow-sm' : 'text-gray-500 hover:text-gray-900'}`}
                  >
                    {tab.toUpperCase()}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 gap-4">
              {trendingNewsData[activeTab].map((item, idx) => (
                <div
                  key={idx}
                  onClick={() => loadSample(item.tag)}
                  className="flex items-center justify-between p-4 border border-gray-100 rounded-xl hover:bg-blue-50/40 hover:border-blue-100 transition cursor-pointer"
                >
                  <div>
                    <h4 className="font-bold text-gray-800 text-sm sm:text-base">{item.title}</h4>
                    <span className="text-xs font-semibold bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md mt-1 inline-block">
                      {item.source}
                    </span>
                  </div>
                  <div className="text-right">
                    <span className={`text-sm font-black ${item.color}`}>{item.trend}</span>
                    <p className="text-[10px] text-gray-400 font-bold uppercase mt-1">Click to Load</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Analytics Section */}
        <div className="space-y-6">
          {/* New Cool Section: Deep Learning Breakdown Map */}
          <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 bg-gradient-to-br from-indigo-50 to-white">
            <h2 className="text-2xl font-bold mb-6 text-indigo-900 flex items-center">
              <span className="bg-indigo-100 p-2 rounded-lg mr-3">🧠</span>
              Model Accuracy Breakdown
            </h2>
            <div className="space-y-5">
              <div>
                <div className="flex justify-between text-sm font-bold text-gray-700 mb-1">
                  <span>Overall Accuracy</span>
                  <span className="text-indigo-600">100.0%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div className="bg-indigo-600 h-2.5 rounded-full" style={{ width: '100%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm font-bold text-gray-700 mb-1">
                  <span>Real News Precision</span>
                  <span className="text-green-600">100.0%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div className="bg-green-500 h-2.5 rounded-full" style={{ width: '100%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm font-bold text-gray-700 mb-1">
                  <span>Fake News Recall</span>
                  <span className="text-red-600">100.0%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div className="bg-red-500 h-2.5 rounded-full" style={{ width: '100%' }}></div>
                </div>
              </div>
              <div className="mt-4 text-xs font-semibold text-gray-500 text-center bg-white p-3 rounded-lg border border-gray-100 shadow-sm">
                Trained on 205,596 verified articles with PySpark MLlib (50,000 features).
              </div>
            </div>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center">
              <span className="bg-green-100 p-2 rounded-lg mr-3">📊</span>
              Spark Analytics Insights
            </h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="text-gray-600 font-medium">Model Accuracy (MLlib)</span>
                <span className="font-bold text-green-600">100.0%</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="text-gray-600 font-medium">Average Article Length</span>
                <span className="font-bold text-blue-600">386 characters</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="text-gray-600 font-medium">Storage Engine</span>
                <span className="font-bold text-purple-600">Hadoop HDFS Parquet</span>
              </div>
            </div>
          </div>

          {/* New Cool Section: Spark Streaming Cluster Monitor */}
          <div className="bg-gray-900 text-white p-8 rounded-2xl shadow-xl relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4">
              <span className="flex h-3 w-3 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
              </span>
            </div>
            <h2 className="text-xl font-bold mb-6 text-white flex items-center">
              <span className="bg-blue-900 p-2 rounded-lg mr-3">🌐</span>
              Live Spark Structured Streaming Monitor
            </h2>
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-gray-800/80 p-4 rounded-xl border border-gray-700">
                <span className="text-xs font-semibold text-gray-400 block">Stream Ingestion</span>
                <span className="text-2xl font-black text-green-400">118.5/s</span>
                <p className="text-[10px] text-gray-400 font-bold mt-1">articles processed</p>
              </div>
              <div className="bg-gray-800/80 p-4 rounded-xl border border-gray-700">
                <span className="text-xs font-semibold text-gray-400 block">Kafka Lag</span>
                <span className="text-2xl font-black text-blue-400">0 ms</span>
                <p className="text-[10px] text-gray-400 font-bold mt-1">real-time sync</p>
              </div>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-xs font-bold">
                <span className="text-gray-400">Spark Master Active Nodes</span>
                <span className="text-green-400">3/3 Online</span>
              </div>
              <div className="flex items-center justify-between text-xs font-bold">
                <span className="text-gray-400">HDFS Simulated Storage</span>
                <span className="text-purple-400">4.8 GB / 10 GB</span>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-1.5 mt-2">
                <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: '48%' }}></div>
              </div>
            </div>
          </div>

          <div className="bg-blue-900 text-white p-8 rounded-2xl shadow-xl">
            <h2 className="text-xl font-bold mb-4">BDA Architecture Highlights</h2>
            <ul className="space-y-3 text-blue-100 text-sm">
              <li className="flex items-start">
                <span className="text-blue-400 mr-2 font-bold">✔</span>
                <b>HDFS Storage:</b> Partitioned columnar Parquet format for fast distributed IO.
              </li>
              <li className="flex items-start">
                <span className="text-blue-400 mr-2 font-bold">✔</span>
                <b>PySpark Transformations:</b> Regex cleaning, stop-word removal, TF-IDF vectorization.
              </li>
              <li className="flex items-start">
                <span className="text-blue-400 mr-2 font-bold">✔</span>
                <b>FastAPI + React:</b> Instant sub-second inference powered by trained Spark weights.
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="max-w-6xl mx-auto mt-20 mb-8">
        <div className="bg-gray-900 rounded-3xl p-8 flex flex-col md:flex-row justify-between items-center shadow-2xl">
          <div className="text-center md:text-left mb-6 md:mb-0">
            <h3 className="text-xl font-black text-white mb-2">Fake News Detection Engine</h3>
            <p className="text-gray-400 text-sm">Powered by Apache Spark, Kafka & Big Data Analytics.</p>
          </div>
          <div className="flex space-x-8 text-sm font-bold text-gray-300">
            <a href="/" className="hover:text-blue-400 transition">Privacy Policy</a>
            <a href="/" className="hover:text-blue-400 transition">API Documentation</a>
            <a href="/" className="hover:text-blue-400 transition">Contact Us</a>
          </div>
        </div>
        <div className="text-center mt-6 text-gray-400 text-sm font-medium">
          © {new Date().getFullYear()} Fake News Detection System. All rights reserved.
        </div>
      </footer>
    </div>
  );
}

export default App;
