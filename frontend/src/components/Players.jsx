import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Button, Container, Table, Title } from '@mantine/core'

import { deleteAllPlayers, deletePlayer, fetchAllPlayers } from '../utils/requests'
import { gameUrl } from '../utils/urls'
import { withCurrentPlayerLiftedIfPresent } from '../utils/utils'
import ConfirmationModal from '../utils/ConfirmationModal'
import useSessionData from '../utils/hooks/useSessionData'

function Players () {
  const params = useParams()
  const navigate = useNavigate()

  const [players, setPlayers] = useState([])
  const [isAdmin, playerID] = useSessionData(params.gameId)
  const [openedWithdrawAll, setOpenedWithdrawAll] = useState(false)

  // Fetches player data every 2 seconds
  useEffect(() => {
    const getPlayers = async () => {
      try {
        const players = await fetchAllPlayers(params.gameId)
        const ordered = withCurrentPlayerLiftedIfPresent(playerID, players)
        setPlayers(ordered)
      } catch (error) {
        console.error(error)
      }
    }

    getPlayers()
    const timer = setInterval(getPlayers, 2000)

    return () => {
      clearInterval(timer)
    }
  }, [params.gameId, playerID])

  const withdrawPlayer = async (event, playerId) => {
    event.stopPropagation()
    try {
      await deletePlayer(params.gameId, playerId)
      navigate(gameUrl(params.gameId))
    } catch (error) {
      console.error(error)
      if (error.response && error.response.status === 401) {
        alert('401 - Unauthenticated request')
      }
    }
  }

  const withdrawAllPlayers = async () => {
    try {
      await deleteAllPlayers(params.gameId)
    } catch (error) {
      console.error(error)
      if (error.response && error.response.status === 401) {
        alert('401 - Unauthenticated request')
      }
    } finally {
      setOpenedWithdrawAll(false)
    }
  }

  return (
    <div>
      <ConfirmationModal opened={openedWithdrawAll} setOpened={setOpenedWithdrawAll}
        title='Withdraw All Players' body='Are you sure you want to withdraw everyone from the game?'
        func={withdrawAllPlayers} />
      <Container size="xl" px="sm">
        <Title order={1} color="white" weight={1000}>Players</Title>
        {
          isAdmin
            ? <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button variant="outline" color="red" radius="md" size="md"
                onClick={() => setOpenedWithdrawAll(true)}
                data-cy="withdraw-all">Withdraw All
              </Button>
            </div>
            : <></>
        }

        <hr />

        <Table highlightOnHover>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>API</th>
              {isAdmin || playerID ? <th>ACTION</th> : <></>}
            </tr>
          </thead>
          <tbody>
            {players.map(player => (
              <tr key={player.id} onClick={() => navigate(player.id)}
                style={(player.id === playerID) ? { background: 'rgb(255,255,255,0.1)' } : {}}>
                <td>{player.id}</td>
                <td>{player.name}</td>
                <td>{player.api}</td>
                {
                  isAdmin || (player.id === playerID)
                    ? <td>
                      <Button variant="outline" color="red" radius="md" size="md"
                        onClick={(event) => withdrawPlayer(event, player.id)}>
                        Withdraw
                      </Button>
                    </td>
                    : <></>
                }
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>
    </div>
  )
}

export default Players
