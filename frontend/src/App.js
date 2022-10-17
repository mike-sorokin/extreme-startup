import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from "./components/Home"
import Game from "./components/Game"
import Player from "./components/Player"
import AddPlayer from "./components/AddPlayer"
import Admin from "./components/Admin"
import Leaderboard from "./components/Leaderboard"

import './App.css';

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/:gameid" element={<Game />} >
          <Route path="addplayer" element={<AddPlayer />} />
          <Route path="player/:id" element={<Player />} />
          <Route path="admin" element={<Admin />} />
          <Route index element={<Leaderboard />} />
        </Route>
      </Routes>
    </Router>

  );
}

export default App;
