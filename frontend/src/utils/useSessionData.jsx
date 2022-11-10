import { useState, useEffect } from 'react'

import { checkAuth } from './requests'

function useSessionData (gameId) {
  const [isAdmin, setIsAdmin] = useState(false)
  const [playerID, setPlayerID] = useState('')

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
