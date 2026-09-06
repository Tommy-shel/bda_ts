import React, { useState } from 'react';

const StatCard = ({ title, value, color }) => (
  <div className={`p-4 rounded-lg shadow-md border-l-4 ${color} bg-white`}>
    <h3 className="text-sm font-medium text-gray-500 uppercase">{title}</h3>
    <p className="text-2xl font-bold text-gray-800">{value}</p>
  </div>
);

function App() {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

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
      setTitle("SHOCKING: Aliens landed in Washington DC last night!");
      setText("A shocking new video circulating online shows an alien spacecraft hovering directly over the Capitol. Conspiracy theorists claim a massive government cover-up!");
    } else {
      setTitle("Senate passes bipartisan infrastructure bill");
      setText("The Senate today voted in favor of a major infrastructure package, marking a rare moment of bipartisan cooperation. Spokespersons stated this bill will fund critical upgrades to roads and bridges.");
    }
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
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <StatCard title="Total Articles Processed" value="550" color="border-blue-500" />
        <StatCard title="Real Articles Analyzed" value="275" color="border-green-500" />
        <StatCard title="Fake Articles Analyzed" value="275" color="border-red-500" />
      </div>

      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-10">
        {/* Detection Section */}
        <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800 flex items-center">
              <span className="bg-blue-100 p-2 rounded-lg mr-3">🔍</span>
              Live Detection
            </h2>
            <div className="space-x-2">
              <button
                onClick={() => loadSample('fake')}
                className="text-xs bg-red-100 text-red-700 font-semibold px-2 py-1 rounded hover:bg-red-200 transition"
              >
                + Sample Fake
              </button>
              <button
                onClick={() => loadSample('real')}
                className="text-xs bg-green-100 text-green-700 font-semibold px-2 py-1 rounded hover:bg-green-200 transition"
              >
                + Sample Real
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

        {/* Analytics Section */}
        <div className="space-y-6">
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
    </div>
  );
}

export default App;
