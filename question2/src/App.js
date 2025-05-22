import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:9876/numbers/';

function App() {
  const [numberType, setNumberType] = useState('e');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleFetch = async () => {
    try {
      const res = await axios.get(`${API_BASE}${numberType}`);
      setResponse(res.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch data.');
      console.error(err);
    }
  };

  return (
    <div className="App">
      <h1>Average Calculator Microservice</h1>
      
      <div>
        <label>Select Number Type: </label>
        <select value={numberType} onChange={(e) => setNumberType(e.target.value)}>
          <option value="p">Prime</option>
          <option value="f">Fibonacci</option>
          <option value="e">Even</option>
          <option value="r">Random</option>
        </select>
        <button onClick={handleFetch}>Get Numbers</button>
      </div>

      {error && <p className="error">{error}</p>}

      {response && (
        <div className="response">
          <h3>Window Previous State:</h3>
          <pre>{JSON.stringify(response.windowPrevState, null, 2)}</pre>

          <h3>Window Current State:</h3>
          <pre>{JSON.stringify(response.windowCurrState, null, 2)}</pre>

          <h3>Numbers:</h3>
          <pre>{JSON.stringify(response.numbers, null, 2)}</pre>

          <h3>Average:</h3>
          <p>{response.avg}</p>
        </div>
      )}
    </div>
  );
}

export default App;
  