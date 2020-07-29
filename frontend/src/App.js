import React, { useEffect } from "react";
import "./App.css";

function App() {
  // React hook that allows us to perform side effets in our App component
  useEffect(() => {
    fetch("/api/pathways").then((response) =>
      response.json().then((data) => {
        console.log(data);
      })
    );
  }, []);
  return <div className="App" />;
}

export default App;
