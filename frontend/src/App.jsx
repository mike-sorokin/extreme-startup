import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { React } from 'react'
import Home from './components/Home'
import Game from './components/Game'
import Player from './components/Player'
import Players from './components/Players'
import Admin from './components/Admin'
import Leaderboard from './components/Leaderboard'
import GameReview from './components/GameReview'
import NotFound from './components/NotFound'

import AdminRoute from './utils/AdminRoute'
import ValidRoute from './utils/ValidRoute'

function App () {
  return (
    <Router >
      <Routes>
        <Route path="/" element={<Home />} />
        <Route element={<ValidRoute />}>
          <Route path="/:gameId" element={<Game />} >
            <Route path="players" element={<Players />} />
            <Route path="players/:id" element={<Player />} />
            <Route element={<AdminRoute />} >
              <Route path="admin" element={<Admin />} />
            </Route>
            <Route index element={<Leaderboard />} />
          </Route>
        </Route>
        <Route path="/review/:gameId" element={<GameReview />}/>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  )
}

export default App
