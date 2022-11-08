import React from 'react'
import { Outlet, useParams, useNavigate } from 'react-router-dom'
import { Menu, Button, Burger } from '@mantine/core'

import { isAdmin } from '../utils/requests'

function Game () {
  const params = useParams()
  const navigate = useNavigate()

  const admin = () => {
    const isMod = isAdmin(params.gameId)
    console.log(isMod)
    return isMod.authorized
  }

  const myPlayerUrl = '/admin'

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
          <Burger size="lg" style={{ position: 'relative', left: '1%', marginTop: '1%' }} data-cy='nav-menu'/>
        </Menu.Target>

        <Menu.Dropdown>
          <Menu.Label>Game Menu</Menu.Label>
          { admin
            ? <Menu.Item>{navButton('/admin', 'Admin Page', 'grape')}</Menu.Item>
            : <Menu.Item>{navButton(myPlayerUrl, 'My Player Page', 'grape')}</Menu.Item>
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
