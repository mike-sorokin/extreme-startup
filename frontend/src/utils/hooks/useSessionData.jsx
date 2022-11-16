import { useState, useEffect } from 'react'

import { checkAuth } from '../requests'

function useSessionData (gameId) {
  const [isAdmin, setIsAdmin] = useState(false)
  const [playerID, setPlayerID] = useState('')

  // Checks session cookie and returns if a player is an admin, and their player id (if they have one)
  // playerID should equal an empty string if the player is a spectator (or if they are an admin)
  useEffect(() => {
    const checkCookie = async () => {
      try {
        const response = await checkAuth(gameId)
        setIsAdmin(response.authorized)
        setPlayerID(response.player)
      } catch (error) {
        console.error(error)
      }
    }

    checkCookie()
  }, [])

  return [isAdmin, playerID]
}

export default useSessionData
