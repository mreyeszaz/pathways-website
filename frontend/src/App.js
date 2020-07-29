import React, { useEffect, useState } from "react";
import "./App.css";
import PathwaysList from "./PathwaysList";

function App() {
  // Takes the pathway objects and puts it in the state
  const [pathways, setPathways] = useState([]);
  // React hook that allows us to perform side effets in our App component
  useEffect(() => {
    fetch("/api/pathways").then((response) =>
      response.json().then((data) => {
        setPathways(data.pathways);
      })
    );
  }, []);

  return (
    <div className="App">
      <PathwaysList pathways={pathways} />
    </div>
  );
}

export default App;
