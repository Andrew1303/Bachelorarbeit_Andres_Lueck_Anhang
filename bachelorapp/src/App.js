import { Routes, Route } from "react-router-dom";
import { Dataoverwatch } from "./pages";
import './App.css'

function App() {
  return (
    <div>
        <Routes>
            <Route path="/" element={<Dataoverwatch/>}/>
        </Routes>
    </div>
  );
}

export default App;
