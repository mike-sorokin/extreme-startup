import React from 'react';
import { useNavigate } from 'react-router-dom'
import { Button } from '@mantine/core';

import { gameUrl } from '../utils/urls'

// Do we need this component? Why don't we just redirect as soon as a game is made?
function GoToGame({ gameId }) {

  const navigate = useNavigate();

  return (
    <div>
      <p>Your game id is: {gameId}</p>
      <Button type="button" onClick={() => { navigate(gameUrl(gameId)) }}>To Game Page</Button>
    </div>
  )
}

// function GoToGame(gameIdGetter) {

//   const navigate = useNavigate();

//   const goToGamePage = () => {
//     navigate(gamePageUrl(gameIdGetter.getGameId()))
//   }

//   return (
//     <div>
//       <p>Your game id is: {gameIdGetter.getGameId()}</p>
//       <Button type="button" onClick={goToGamePage}>To Game Page</Button>
//     </div>
//   )
// }

export default GoToGame
