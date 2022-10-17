import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from "./components/Home"
import Player from "./components/Player"

import './App.css';

function App() {

  // const [name, setName] = useState("")
  // const [url, setUrl] = useState("")

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/player/:id" element={<Player />} />
      </Routes>
    </Router>

  );
}

export default App;
