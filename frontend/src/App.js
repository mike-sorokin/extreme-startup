import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { MantineProvider } from '@mantine/core';
import { NotificationsProvider } from '@mantine/notifications';
import Home from "./components/Home"
import Game from "./components/Game"
import Player from "./components/Player"
import Players from "./components/Players"
import Admin from "./components/Admin"
import Leaderboard from "./components/Leaderboard"

import './App.css';

function App() {

  return (
    // <MantineProvider withGlobalStyles withNormalizeCSS>
    //   <NotificationsProvider position='top-right'>
    //     <Router>
    //       <Routes>
    //         <Route path="/" element={<Home />} />
    //         <Route path="/:gameid" element={<Game />} >
    //           <Route path="player/:id" element={<Player />} />
    //           <Route path="admin" element={<Admin />} />
    //           <Route index element={<Leaderboard />} />
    //         </Route>
    //       </Routes>
    //     </Router>
    //   </NotificationsProvider>
    // </MantineProvider>

    <MantineProvider withGlobalStyles withNormalizeCSS>
      <NotificationsProvider position='top-right'>
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/:gameid" element={<Game />} >
              <Route path="players" element={<Players />} />
              <Route path="players/:id" element={<Player />} />
              <Route path="admin" element={<Admin />} />
              <Route index element={<Leaderboard />} />
            </Route>
          </Routes>
        </Router>
      </NotificationsProvider>
    </MantineProvider>
    
  );
}

export default App;
