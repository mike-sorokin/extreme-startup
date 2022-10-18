import React from 'react'
import { Outlet, useParams } from "react-router-dom"

function Game() {

  const params = useParams()

  return (
    <div>
      <div> Extreme Restartup Game {params.gameid} </div>
      <Outlet />
    </div>
  )
}

export default Game