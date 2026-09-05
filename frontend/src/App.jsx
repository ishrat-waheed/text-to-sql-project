import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [clarification, setClarification] = useState(null);
  const [error, setError] = useState("");

  const askQuestion = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setResponse(null);
    setClarification(null);

    try {
      // First check whether clarification is needed
      const clarifyRes = await fetch(
        `http://127.0.0.1:8000/clarify?question=${encodeURIComponent(
          question
        )}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
          },
        }
      );

      const clarifyData = await clarifyRes.json();

      if (!clarifyRes.ok) {
        throw new Error(
          clarifyData.detail || "Clarification request failed."
        );
      }

      // If clarification is needed, show options
      if (clarifyData.needs_clarification) {
        setClarification(clarifyData);
        setLoading(false);
        return;
      }

      // Otherwise directly generate SQL
      await executeNormalQuery();
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const executeNormalQuery = async () => {
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/query?question=${encodeURIComponent(
          question
        )}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
          },
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      setResponse(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const selectClarification = async (optionId) => {
    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/clarify/execute?clarification_type=${encodeURIComponent(
          clarification.type
        )}&option_id=${optionId}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
          },
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(
          data.detail || "Could not execute selected option."
        );
      }

      setResponse({
        question: question,
        sql: data.sql,
        columns: data.columns,
        results: data.results,
        row_count: data.row_count,
      });

      setClarification(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      <header className="header">
        <div className="logo">🤖</div>

        <div>
          <h1>Text-to-SQL Assistant</h1>
          <p>Ask your PostgreSQL database anything</p>
        </div>
      </header>

      <main className="container">

        <div className="search-card">

          <label>Ask your question</label>

          <div className="input-row">

            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  askQuestion();
                }
              }}
              placeholder="Example: Show me all customers from Karachi"
            />

            <button onClick={askQuestion} disabled={loading}>
              {loading ? "Thinking..." : "Ask 🔍"}
            </button>

          </div>

          <div className="examples">

            <span>Try:</span>

            <button
              onClick={() =>
                setQuestion("Show me all customers from Karachi")
              }
            >
              Customers from Karachi
            </button>

            <button
              onClick={() =>
                setQuestion("Which products have been ordered the most?")
              }
            >
              Popular products
            </button>

            <button
              onClick={() =>
                setQuestion("Show me the orders")
              }
            >
              Show orders
            </button>

          </div>

        </div>

        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}

        {clarification && (
          <div className="result-card">

            <h2>🤔 Please clarify</h2>

            <div className="question-box">
              <strong>Your question:</strong>
              <p>{clarification.question}</p>
            </div>

            <p>
              I found multiple possible meanings. Please select one:
            </p>

            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "12px",
                marginTop: "20px",
              }}
            >

              {clarification.options.map((option) => (
                <button
                  key={option.id}
                  onClick={() => selectClarification(option.id)}
                  disabled={loading}
                  style={{
                    padding: "16px",
                    border: "2px solid #e0e7ff",
                    borderRadius: "12px",
                    background: "#eef2ff",
                    color: "#3730a3",
                    cursor: "pointer",
                    textAlign: "left",
                    fontSize: "16px",
                    fontWeight: "bold",
                  }}
                >
                  {option.id}.{" "}
                  {option.text ||
                    option.label ||
                    option.description ||
                    `Option ${option.id}`}
                </button>
              ))}

            </div>

          </div>
        )}

        {response && (
          <div className="result-card">

            <h2>📊 Query Result</h2>

            <div className="question-box">
              <strong>Question:</strong>
              <p>{response.question}</p>
            </div>

            <div className="sql-box">

              <div className="sql-header">
                <strong>Generated SQL</strong>
              </div>

              <pre>{response.sql}</pre>

            </div>

            <div className="result-info">
              <strong>Results:</strong> {response.row_count} rows
            </div>

            {response.results && response.results.length > 0 && (
              <div className="table-container">

                <table>

                  <thead>
                    <tr>
                      {response.columns.map((column) => (
                        <th key={column}>{column}</th>
                      ))}
                    </tr>
                  </thead>

                  <tbody>

                    {response.results.map((row, index) => (
                      <tr key={index}>

                        {response.columns.map((column) => (
                          <td key={column}>
                            {String(row[column] ?? "")}
                          </td>
                        ))}

                      </tr>
                    ))}

                  </tbody>

                </table>

              </div>
            )}

            {response.results &&
              response.results.length === 0 && (
                <p>No results found.</p>
              )}

          </div>
        )}

      </main>

      <footer>
        Built with React + FastAPI + Groq + PostgreSQL
      </footer>

    </div>
  );
}

export default App;





