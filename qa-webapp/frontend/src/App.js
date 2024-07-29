import React, { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answers, setAnswers] = useState({ answer1: '', answer2: '' });
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!question.trim()) {
      setError('Please enter a question.');
      return;
    }
    setError('');
    try {
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      if (!response.ok) {
        throw new Error('Network response was not ok.');
      }
      const data = await response.json();
      setAnswers({ answer1: data[0].answer1, answer2: data[1].answer2 });
    } catch (error) {
      setError('An error occurred: ' + error.message);
    }
  };

  return (
    <div className="App">
      <h1>Question Answering System</h1>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Enter your question"
      />
      <button onClick={handleSubmit}>Submit</button>
      {error && <p className="error">{error}</p>}
      {answers.answer1 && (
        <div className="answer">
          <h2>Answer 1:</h2>
          <p>{answers.answer1}</p>
        </div>
      )}
      {answers.answer2 && (
        <div className="answer">
          <h2>Answer 2:</h2>
          <p>{answers.answer2}</p>
        </div>
      )}
    </div>
  );
}

export default App;
