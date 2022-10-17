import axios from 'axios';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { MantineProvider } from '@mantine/core';
import { NotificationsProvider } from '@mantine/notifications';
import Home from "./components/Home"
import Player from "./components/Player"

import './App.css';

function App() {

  return (
    <MantineProvider withGlobalStyles withNormalizeCSS>
      <NotificationsProvider position='top-right'>
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/player/:id" element={<Player />} />
          </Routes>
        </Router>
      </NotificationsProvider>
    </MantineProvider>
  );
}

export default App;
