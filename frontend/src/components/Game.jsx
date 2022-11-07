import React, { useState } from 'react'
import { Outlet, useParams, useNavigate } from 'react-router-dom'
import { Menu, Button, Burger } from '@mantine/core'

import { updateSessionData } from '../utils/utils'

function Game () {
  const [isAdmin, setIsAdmin] = useState(false)
  const [playerID, setPlayerID] = useState('')
  const params = useParams()
  const navigate = useNavigate()

  updateSessionData(params.gameId, setIsAdmin, setPlayerID)

  // Separate file for navButton?
  const navButton = (suffix, text, color) => {
    const url = '/' + params.gameId + suffix
    return (
      <Button variant="light" color={color} radius="md" size="md" onClick={() => navigate(url)}>{text}</Button>
    )
  }

  return (
    <>
      <Menu shadow="md" width={200}>
        <Menu.Target>
          <Burger size="lg" style={{ position: 'relative', left: '1%', marginTop: '1%' }}/>
        </Menu.Target>

        <Menu.Dropdown>
          <Menu.Label>Game Menu</Menu.Label>
          { isAdmin
            ? <Menu.Item>{navButton('/admin', 'Admin Page', 'grape')}</Menu.Item>
            : playerID
              ? <Menu.Item>{navButton(`/players/${playerID}`, 'My Player Page', 'grape')}</Menu.Item>
              : <></>
          }
          <Menu.Item>{navButton('', 'Leaderboard', 'indigo')}</Menu.Item>
          <Menu.Item>{navButton('/players', 'Players', 'pink')}</Menu.Item>
        </Menu.Dropdown>
      </Menu>
      <Outlet />
    </>
  )
}

export default Game
