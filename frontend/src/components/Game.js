import React from 'react';
import { Outlet, useParams, useNavigate } from "react-router-dom";
import { Menu, Button, Burger } from "@mantine/core";

import { playersUrl, adminUrl } from "../utils/urls"

function Game() {

  const params = useParams()
  const navigate = useNavigate()

  // Separate file for navButton?
  const navButton = (url, text) => {
    return (
      <Button variant="outline" color="dark" radius="md" size="md" onClick={() => navigate(url)}>{text}</Button>
    )
  }

  return (
    <>
      <Menu shadow="md" width={200}>
        <Menu.Target>
          <Burger size="lg" />
        </Menu.Target>

        <Menu.Dropdown>
          <Menu.Label>Menu</Menu.Label>
          <Menu.Item>{navButton(adminUrl(params.gameid), "Host Page")}</Menu.Item>
          <Menu.Item>{navButton('', "Leaderboard")}</Menu.Item>
          <Menu.Item>{navButton(playersUrl(params.gameid), "Players")}</Menu.Item>
        </Menu.Dropdown>
      </Menu>
      <Outlet />
    </>
  )
}

export default Game