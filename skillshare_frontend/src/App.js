import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [mesajDjango, setMesajDjango] = useState(0);
  useEffect(() => {
  fetch('http://127.0.0.1:8000').then(res => res.json()).then(data => {
      setMesajDjango(data.mesaj_django)
    });
  }, []);
  return (
    <div className="App">
      <header className="App-header">
      <p>Salu2are {mesajDjango} </p>
      <h1>title</h1>
      </header>
    </div>
  );
}

export default App;
