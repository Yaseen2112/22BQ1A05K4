import React, { useState } from "react";
import { Log } from "./middleware";

function App() {
  const [logStatus, setLogStatus] = useState(null);

  const handleLogClick = async () => {
    try {
      await Log('frontend', 'info', 'api', 'User clicked test button');
      setLogStatus("Log sent successfully.");
    } catch (error) {
      setLogStatus("Failed to send log.");
      console.error("Logging error:", error);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Frontend Test</h1>
      <button onClick={handleLogClick}>Test Log</button>
      {logStatus && <p>{logStatus}</p>}
    </div>
  );
}

export default App;
