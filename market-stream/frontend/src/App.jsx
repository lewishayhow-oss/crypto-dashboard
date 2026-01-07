import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './App.css'

function App() {
  const [price, setPrice] = useState(0)
  const [timestamp, setTimestamp] = useState("Never")
  const [history, setHistory] = useState([])

  const updatePrice = () => {
    fetch("http://localhost:5000/price/BTC")
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          console.error("API Error:", data.error);
          return;
        }
        setPrice(data.price);
        setTimestamp(data.timestamp);
        
        setHistory(prevHistory => {
          // Keep only the last 20 data points for performance and readability
          const newHistory = [...prevHistory, { time: data.timestamp, value: data.price }];
          return newHistory.slice(-20);
        });
      })
      .catch(error => {
        console.error("Error fetching price:", error);
      });
  }

  // Auto-refresh logic
  useEffect(() => {
    // Fetch immediately on load
    updatePrice();

    // Set up a timer to fetch every 3 seconds
    const interval = setInterval(updatePrice, 3000);

    // Clean up the timer when the component unmounts
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <h1>Bitcoin Live Tracker</h1>
      
      <div className="dashboard-container">
        <div className="price-card">
          <h2>BTC/USD</h2>
          <p className="price-display">
            ${price.toLocaleString()}
          </p>
          <p>Last updated: {timestamp}</p>
          <button onClick={updatePrice} className="refresh-button">
            Manual Refresh
          </button>
        </div>

        <div className="chart-container">
          <h3>Session Trend (Live)</h3>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={history}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis 
                dataKey="time" 
                tick={{ fill: '#888', fontSize: 12 }}
                interval="preserveStartEnd"
              />
              <YAxis 
                domain={['auto', 'auto']} 
                tick={{ fill: '#888', fontSize: 12 }}
              />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1a1a1a', borderColor: '#333', color: '#fff' }}
                itemStyle={{ color: '#3498db' }}
              />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#3498db" 
                strokeWidth={3} 
                dot={false}
                activeDot={{ r: 6 }}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
          {history.length === 0 && <p className="no-data">Connecting to market engine...</p>}
        </div>
      </div>
    </div>
  )
}

export default App
