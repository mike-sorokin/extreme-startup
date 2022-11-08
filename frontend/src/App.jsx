import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { React } from 'react'
import Home from './components/Home'
import Game from './components/Game'
import Player from './components/Player'
import Players from './components/Players'
import Admin from './components/Admin'
import Leaderboard from './components/Leaderboard'
import NotFound from './components/NotFound'

import AdminRoute from './utils/AdminRoute'
import CheckRoute from './utils/CheckRoute'

function App () {
  return (
    <Router >
      <Routes>
        <Route path="/" element={<Home />} />
        <Route element={<CheckRoute />}>
          <Route path="/:gameId" element={<Game />} >
            <Route path="players" element={<Players />} />
            <Route path="players/:id" element={<Player />} />
            <Route element={<AdminRoute />} >
              <Route path="admin" element={<Admin />} />
            </Route>
            <Route index element={<Leaderboard />} />
          </Route>
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  )
}

export default App
