import React from 'react';
import { Outlet, useParams } from "react-router-dom";
import { Menu, Button, Burger } from "@mantine/core";
import { useNavigate } from "react-router-dom";

function Game() {

  const params = useParams()
  const navigate = useNavigate()

  const navButton = (suffix, text, color) => {
    let url = '/' + params.gameid + suffix
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
        <Menu.Item>{navButton('/admin', "Host Page", "grape")}</Menu.Item>
        <Menu.Item>{navButton('', "Leaderboard", "indigo")}</Menu.Item>
        <Menu.Item>{navButton('/players', "Players", "teal")}</Menu.Item>
      </Menu.Dropdown>
    </Menu>
    <Outlet />
    </>
  )
}

export default Game