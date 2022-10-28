import React from 'react'
import { Outlet, useParams, useNavigate } from 'react-router-dom'
import { Menu, Button, Burger } from '@mantine/core'

function Game () {
  const params = useParams()
  const navigate = useNavigate()

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
          <Burger size="lg" />
        </Menu.Target>

        <Menu.Dropdown>
          <Menu.Label>Game Menu</Menu.Label>
          <Menu.Item>{navButton('/admin', 'Host Page', 'grape')}</Menu.Item>
          <Menu.Item>{navButton('', 'Leaderboard', 'indigo')}</Menu.Item>
          <Menu.Item>{navButton('/players', 'Players', 'pink')}</Menu.Item>
        </Menu.Dropdown>
      </Menu>
      <Outlet />
    </>
  )
}

export default Game
