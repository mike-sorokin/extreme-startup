import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { React } from 'react'
import Home from './components/Home'
import Game from './components/Game'
import Player from './components/Player'
import Players from './components/Players'
import Admin from './components/Admin'
import Leaderboard from './components/Leaderboard'

function App () {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/:gameId" element={<Game />} >
          <Route path="players" element={<Players />} />
          <Route path="players/:id" element={<Player />} />
          <Route path="admin" element={<Admin />} />
          <Route index element={<Leaderboard />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
